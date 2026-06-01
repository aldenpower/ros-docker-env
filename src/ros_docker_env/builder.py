"""
ROS Docker Environment Builder

This module provides logic for generating Docker build commands and
Docker Compose configurations for ROS development environments.

Supported ROS distributions:
    - humble
    - jazzy
    - kilted

Features:
    - Select Ubuntu or NVIDIA CUDA/OpenGL base images
    - Optional Gazebo installation support
    - Docker build command generation
    - Automatic user UID and username propagation

Main entrypoints:
    - handle_build(args)

The generated environments are intended for development containers
with optional GPU acceleration and Gazebo simulation support.
"""

import sys
from ros_docker_env import resources_path
from os import getuid
from ros_docker_env.utils import eprint


def handle_build(args) -> None:
    """
    Generate a Docker build command for a ROS development environment.

    The build configuration is derived from the selected ROS distribution
    and optional features such as NVIDIA GPU support and Gazebo integration.

    Supported ROS distributions:
        - humble
        - jazzy
        - kilted
    Args:
        args:
            Parsed argparse namespace containing:
                - rosdistro (str):
                    ROS distribution name.
                - gazebo (bool):
                    Enable Gazebo installation.
                - nvidia (bool):
                    Use NVIDIA-compatible base image.
    Raises:
        SystemExit:
            Raised when an unsupported ROS distribution is selected
            or when build configuration generation fails.
    """
    # Mapping configuration
    # good to know: https://gazebosim.org/docs/latest/ros_installation/
    config_map = {
        "humble": {
            "base": "ubuntu:jammy",
            "gz": "ignition-fortress"
        },
        "jazzy": {
            "base": "ubuntu:noble",
            "gz": "gz-harmonic"
        },
        "kilted": {
            "base": "ubuntu:noble",
            "gz": "gz-ionic"
        }
    }

    distro = args.rosdistro
    if distro not in config_map:
        eprint(f"Unsupported ROS distribution: {distro}")
        sys.exit(1)

    try:
        # Determine base image and Gazebo version
        # base_image = config_map[distro]["nvidia"] if args.nvidia else config_map[distro]["base"]
        base_image = config_map[distro]["base"]
        gz_version = config_map[distro]["gz"] if args.gazebo else ""

        image_tag = base_image.split(":")[-1]
        image_name = f"ubuntu/ros_{distro}"
        if args.gazebo:
            image_name += "_gazebo"

        docker = str(resources_path.joinpath("docker"))
        tmux_config = str(resources_path.joinpath("tmux"))
        bash = str(resources_path.joinpath("bash"))

        # Build command construction
        build_cmd = [
            "docker", "build",
            "--progress", "tty",
            "--target", "dev",
            "--build-context", f"tmux_config={tmux_config}",
            "--build-context", f"bash={bash}",
            "--build-context", f"docker={docker}",
            "--build-arg", f"USER_UID={getuid()}",
            "--build-arg", f"BASE_IMAGE={base_image}",
            "--build-arg", f"ros_distribution={distro}",
            "--build-arg", f"gz_distribution={gz_version}",
            "--tag", f"{image_name}:{image_tag}",
            "--file", str(resources_path.joinpath("docker/base.Dockerfile")),
            "."
        ]

        print(" ".join(build_cmd))

    except OSError as e:
        eprint(f"Build setup failed: {e}")
        sys.exit(1)
