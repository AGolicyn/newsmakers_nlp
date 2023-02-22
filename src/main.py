import asyncio
from nlp.sockets.subscriber import Subscriber
from nlp.db.connection import DatabaseSession
from nlp.processing.processing import process
from loguru import logger

async def main():
    logger.debug('NLP Start serving')
    subscriber = Subscriber()
    while True:
        await subscriber.synchronize()
        with DatabaseSession() as db:
            await subscriber.receive_json_to_db(db=db)
            process(db=db)
            # loop = asyncio.get_running_loop()
            # await loop.run_in_executor(None, )


if __name__ == "__main__":
    asyncio.run(main())