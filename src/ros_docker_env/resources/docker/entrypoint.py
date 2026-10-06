#!/usr/bin/env python3

import logging
import os
import subprocess
import sys

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def source_ros_environment():
    """Source the ROS setup file and import its environment."""
    ros_distro = os.getenv("ROS_DISTRO")

    if not ros_distro:
        logger.error("ROS_DISTRO is not set")
        sys.exit(1)

    setup_file = f"/opt/ros/{ros_distro}/setup.bash"

    if not os.path.isfile(setup_file):
        logger.error("ROS setup file not found: %s", setup_file)
        sys.exit(1)

    command = [
        "bash",
        "-c",
        f"source {setup_file} && env",
    ]

    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    for line in result.stdout.splitlines():
        key, separator, value = line.partition("=")

        if separator:
            os.environ[key] = value


def main():
    """Configure the ROS environment and execute the container command."""
    logger.info("USERNAME=%s", os.getenv("USERNAME"))
    logger.info("ROS_DISTRO=%s", os.getenv("ROS_DISTRO"))
    logger.info("GZ_DISTRO=%s", os.getenv("GZ_DISTRO"))

    source_ros_environment()

    if len(sys.argv) < 2:
        logger.error("No command provided")
        sys.exit(1)

    logger.info("Executing: %s", " ".join(sys.argv[1:]))

    os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == "__main__":
    main()
