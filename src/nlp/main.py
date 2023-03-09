import asyncio

from nlp.sockets.subscriber import Subscriber
from nlp.db.connection import DatabaseSession
from nlp.processing.processing import process_multi
from nlp.crud.title import get_day_url_frequency
from loguru import logger



async def main():
    logger.debug('NLP Start serving')
    subscriber = Subscriber()
    while True:
        await subscriber.synchronize()
        with DatabaseSession() as db:
            await subscriber.receive_json_to_db(db=db)
            res = get_day_url_frequency(db=db)  # todo blocking shit
            logger.info(res)
            await process_multi(db=db)
            # break


if __name__ == "__main__":
    asyncio.run(main())
