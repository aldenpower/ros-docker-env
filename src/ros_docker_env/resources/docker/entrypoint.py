#!/usr/bin/env python3

import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    logger.info("USERNAME=%s", os.getenv("USERNAME"))
    logger.info("ROS_DISTRO=%s", os.getenv("ROS_DISTRO"))
    logger.info("GZ_DISTRO=%s", os.getenv("GZ_DISTRO"))

    logger.info("Executing: %s", " ".join(sys.argv[1:]))

    os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == "__main__":
    main()
