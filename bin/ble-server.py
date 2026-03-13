import asyncio

from pb_ble.vhub import get_virtual_ble


async def main():
    async with await get_virtual_ble(
        broadcast_channel=101,
        observe_channels=[100],
    ) as vble:
        print("Listening...")
        while True:
            if msg := vble.observe():
                print("Received message:", msg)
            await asyncio.sleep(10)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
