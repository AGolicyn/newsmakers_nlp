"""Receiving data from Spider-service"""
import json
import asyncio
import zmq
from loguru import logger
from zmq.asyncio import Context
from contextlib import suppress
from src.crud.title import insert_title
from sqlalchemy.orm import Session

from src.sockets.settings.settings import *

context = Context()


class Subscriber:
    def __init__(self):
        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect(SPIDER_PUBLISHER_ADDRESS)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')

        self.syncservice = context.socket(zmq.REP)
        self.syncservice.bind("tcp://*:5562")

    async def synchronize(self):
        logger.debug('Subscriber waiting for synchronizing request on 5562..')
        await self.syncservice.recv()
        await self.syncservice.send(b'')
        logger.debug('Subscriber and publisher successfully synchronized')

    async def receive_json_to_db(self, db: Session):
        logger.debug('Receiving data..')
        with suppress(asyncio.CancelledError):
            while True:
                try:
                    msg = await self.subscriber.recv_json()
                    if 'END' in msg:
                        break
                    insert_title(db, msg)
                except json.decoder.JSONDecodeError as e:
                    logger.error(e)
        logger.debug('All data was received')
