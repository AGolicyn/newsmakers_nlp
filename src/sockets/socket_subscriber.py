"""Receiving data from Spider-service"""
import json
import asyncio
import zmq
from loguru import logger
from zmq.asyncio import Context
from contextlib import suppress

from settings.settings import *
from src.processing.processing import process

context = Context()

class Subscriber:
    def __init__(self):
        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect(SPIDER_PUBLISHER_ADDRESS)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')

        self.syncservice = context.socket(zmq.REP)
        self.syncservice.bind("tcp://*:5562")

    async def _synchronize(self):
        logger.debug('Subscriber waiting for synchronizing request..')
        await self.syncservice.recv()
        await self.syncservice.send(b'')
        logger.debug('Subscriber and publisher successfully synchronized')

    async def receive_json(self):
        await self._synchronize()
        logger.debug('Receiving data..')
        received_data = []
        with suppress(asyncio.CancelledError):
            try:
                msg = await self.subscriber.recv_json()
                received_data.append(msg)
            except json.decoder.JSONDecodeError as e:
                logger.error(e)
        logger.debug('All data was received')
class Publisher:
    def __init__(self):
        self.publisher = context.socket(zmq.PUB)
        self.publisher.sndhwm = 110000
        self.publisher.bind(NLP_PUBLISHER_ADDRESS)

    async def _synchronize(self):
        logger.debug('Synchronizing with receiver')
        self.syncclient = context.socket(zmq.REQ)
        self.syncclient.connect(NLP_SYNCSERVER_ADDRESS)
        await self.syncclient.send(b'')
        await self.syncclient.recv()
        logger.debug('Server accept synchronization')

    async def send_json(self, value):
        await self._synchronize()
        logger.debug('Sending data..')
        await self.publisher.send_json(value)
        logger.debug('Data was sent')

async def main():
    subscriber, publisher = Subscriber(), Publisher()
    while True:
        data = await subscriber.receive_json()
        new_data = process(data)
        await publisher.send_json(new_data)


if __name__ == "__main__":
    asyncio.run(main())
