import asyncio
from src.sockets.subscriber import Subscriber
from src.db.connection import DatabaseSession
from src.processing.processing import process
from loguru import logger

async def main():
    logger.debug('Start serving')
    subscriber = Subscriber()
    while True:
        await subscriber.synchronize()
        with DatabaseSession() as db:
            await subscriber.receive_json_to_db(db=db)
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, process(db=db))


if __name__ == "__main__":
    asyncio.run(main())