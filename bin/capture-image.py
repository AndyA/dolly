#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2015-22  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This file is part of python-gphoto2.
#
# python-gphoto2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# python-gphoto2 is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with python-gphoto2.  If not, see
# <https://www.gnu.org/licenses/>.
import locale
import logging
import math
import os
import sys
import time

import gphoto2 as gp

FRAMES = "tmp/frames"
RATE = 2


def main():
    os.makedirs(FRAMES, exist_ok=True)
    locale.setlocale(locale.LC_ALL, "")
    logging.basicConfig(
        format="%(levelname)s: %(name)s: %(message)s", level=logging.WARNING
    )
    # callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.Camera()
    camera.init()
    next_wake = math.ceil(time.time() / RATE) * RATE
    while True:
        sleep_time = next_wake - time.time()
        if sleep_time > 0:
            print("Sleeping for", sleep_time)
            time.sleep(sleep_time)
        print("Capturing image")
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print("Camera file path: {0}/{1}".format(file_path.folder, file_path.name))
        target = os.path.join(FRAMES, file_path.name)
        print("Copying image to", target)
        img_file = camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
        )
        img_file.save(target)
        next_wake += RATE
    camera.exit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
