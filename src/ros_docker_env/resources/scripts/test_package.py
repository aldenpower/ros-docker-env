#!/usr/bin/env python3

import os
import subprocess
import sys


def run(cmd, shell=False, capture_output=False):
    """Run a command and exit on failure."""
    print(f"$ {cmd if isinstance(cmd, str) else ' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        shell=shell,
        check=True,
        text=True,
        capture_output=capture_output,
    )

    return result.stdout.strip() if capture_output else None


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <package>")
        sys.exit(1)

    package = sys.argv[1]
    ros_distro = os.environ.get("ROS_DISTRO")

    if not package:
        print("PACKAGE environment variable is not set")
        sys.exit(1)

    os.chdir("/home/ros2user/ros2_ws")

    print("==> Finding build dependencies")

    result = run(
        f"colcon list --packages-up-to {package}",
        shell=True,
        capture_output=True,
    )

    package_paths = []
    for line in result.splitlines():
        fields = line.split()
        if len(fields) >= 2:
            package_paths.append(fields[1])

    if not package_paths:
        print(f"Package not found: {package}")
        sys.exit(1)

    package_paths_str = " ".join(package_paths)
    print(package_paths_str)

    print("\n==> Installing dependencies")

    run(["sudo", "apt-get", "update"])
    run(["rosdep", "update"])

    run(
        [
            "rosdep",
            "install",
            "--from-paths",
            *package_paths,
            "--ignore-src",
            "-r",
            "-y",
            "--rosdistro",
            ros_distro,
        ]
    )

    print("\n==> Building")

    run(
        [
            "colcon",
            "build",
            "--packages-up-to",
            package,
            "--event-handlers",
            "console_direct+",
        ]
    )

    print(f"\n==> Testing {package}")

    run(
        [
            "colcon",
            "test",
            "--packages-select",
            package,
            "--event-handlers",
            "console_direct+",
        ]
    )

    print("\n==> Test results")

    run(
        [
            "colcon",
            "test-result",
            "--verbose",
        ]
    )


if __name__ == "__main__":
    main()
