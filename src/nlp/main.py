import asyncio
# import time

from loguru import logger
# from functools import partial
# from concurrent.futures import ProcessPoolExecutor

# from nlp.sockets.subscriber import Subscriber
from nlp.crud.title import get_day_url_frequency
from nlp.db.session import AsyncSessionFactory
from nlp.processing.processing import Processor
from nlp.processing.settings import SUPPORTED_COUNTRIES


async def main():
    logger.debug('NLP Start serving')
    # subscriber = Subscriber()

    while True:
        # await subscriber.synchronize()
        async with AsyncSessionFactory() as db:
            # await subscriber.receive_json_to_db(db=db)
            res = await get_day_url_frequency(db=db)
            logger.info(res)
            # loop = asyncio.get_running_loop()
            # tasks = []
            result = {}
            # start = time.time()

            # with ProcessPoolExecutor() as pool:

            # logger.debug(f'Start multiprocessing with {pool._max_workers} workers')
        for country in SUPPORTED_COUNTRIES[1:]:
            logger.debug(f"Start for {country}")
            prc = Processor(country)
            logger.debug("Object Processor created")
            async with AsyncSessionFactory() as db:
                data = await prc.get_data(db=db)
            logger.debug(data)
            res = prc.process_daily_data(data)
            result.update(res)
            # tasks.append(loop.run_in_executor(pool, partial(prc.process_daily_data, data)))
            logger.debug("Result updated")
        # logger.debug(len(tasks))
        # done, pending = await asyncio.wait(tasks)
        # for done_task in done:
        #     res = await done_task
        #     result.update(res)
        logger.debug("Inserting")
        async with AsyncSessionFactory() as db:
            await Processor.insert_data(db=db, result=result)
        # end = time.time() - start

            # logger.debug(f'End multiprocessing, with {end}')


if __name__ == "__main__":
    asyncio.run(main())
