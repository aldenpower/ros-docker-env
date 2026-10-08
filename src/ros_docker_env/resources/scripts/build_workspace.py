#!/usr/bin/env python3

import os
import subprocess


def run(cmd, shell=False, capture_output=False):
    """Run a command and exit on failure."""
    command = cmd if isinstance(cmd, str) else " ".join(cmd)
    print(f"\033[1;32m$\033[0m \033[36m{command}\033[0m", flush=True)


    result = subprocess.run(
        cmd,
        shell=shell,
        check=True,
        text=True,
        capture_output=capture_output,
    )

    return result.stdout.strip() if capture_output else None


def main():
    os.chdir("/home/ros2user/ros2_ws")

    ros_distro = os.environ.get("ROS_DISTRO")

    run(["sudo", "apt-get", "update"])
    run(["rosdep", "update"])

    os.environ["PIP_BREAK_SYSTEM_PACKAGES"] = "1"

    run([
        "rosdep",
        "install",
        "-r",
        "--from-paths",
        "src",
        "--ignore-src",
        "-y",
        "--rosdistro",
        ros_distro,
    ])

    print("\n==> Building")

    run([
        "colcon",
        "build",
        "--merge-install",
        "--cmake-args", "-DCMAKE_BUILD_TYPE=Release",
        "--event-handlers",
        "console_direct+",
    ])


if __name__ == "__main__":
    main()
