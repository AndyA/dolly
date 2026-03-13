import asyncio
import locale
import logging
import os

import gphoto2 as gp
from pb_ble.vhub import get_virtual_ble

FRAMES = "tmp/frames"


async def main():
    last_image_num: int = -1
    os.makedirs(FRAMES, exist_ok=True)
    locale.setlocale(locale.LC_ALL, "")
    logging.basicConfig(
        format="%(levelname)s: %(name)s: %(message)s", level=logging.WARNING
    )

    camera = gp.Camera()  # ty:ignore[unresolved-attribute]
    camera.init()

    async with await get_virtual_ble(
        broadcast_channel=101,
        observe_channels=[100],
        scanning_mode="active",
    ) as vble:
        print("Listening...")
        while True:
            # print("Tick!")
            img_num = vble.observe(channel=100)
            if img_num is not None and img_num != last_image_num:
                file_path = camera.capture(gp.GP_CAPTURE_IMAGE)  # ty:ignore[unresolved-attribute]
                target = os.path.join(FRAMES, f"frame{img_num:06d}.jpg")
                print(f"frame: {target}")
                img_file = camera.file_get(
                    file_path.folder,
                    file_path.name,
                    gp.GP_FILE_TYPE_NORMAL,  # ty:ignore[unresolved-attribute]
                )
                img_file.save(target)
                last_image_num = img_num

            await asyncio.sleep(0.05)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
