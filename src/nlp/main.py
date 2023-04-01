import asyncio

from loguru import logger

from nlp.sockets.subscriber import Subscriber
from nlp.crud.title import get_day_url_frequency
from nlp.db.session import AsyncSessionFactory
from nlp.processing.processing import Processor
from nlp.processing.settings import SUPPORTED_COUNTRIES


async def main():
    logger.debug('NLP Start serving')
    subscriber = Subscriber()
    await subscriber.synchronize()
    async with AsyncSessionFactory() as db:
        await subscriber.receive_json_to_db(db=db)
        parsed = await get_day_url_frequency(db=db)
        logger.info(parsed)
        for country in SUPPORTED_COUNTRIES:
            prc = Processor(country)
            data = await prc.get_data(db=db)
            result = prc.process_daily_data(data)
            await prc.insert_data(db=db, result=result)


if __name__ == "__main__":
    asyncio.run(main())
