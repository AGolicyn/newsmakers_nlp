import asyncio
from src.sockets.socket_subscriber import do_nlp_subscribe
from src.sockets.socket_publisher import do_nlp_publish
from src.processing.processing import process

async def main():
    while True:
        raw_data = await do_nlp_subscribe()
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, process(raw_data))
        await do_nlp_publish(data)

if __name__ == "__main__":
    asyncio.start_server()
    asyncio.run(main())