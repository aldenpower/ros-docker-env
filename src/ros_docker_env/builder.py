"""
ROS Docker Environment Builder

This module provides logic for generating Docker build commands and
Docker Compose configurations for ROS development environments.

Supported ROS distributions:
    - humble
    - jazzy
    - kilted

Features:
    - Select Ubuntu base images
    - Optional Gazebo installation support
    - Docker build command generation
    - Automatic user UID and username propagation

Main entrypoints:
    - handle_build(args)

The generated environments are intended for development containers
with Gazebo simulation support.
"""

from ros_docker_env import resources_path
from os import getuid


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

    base_image = config_map[distro]["base"]

    image_tag = base_image.split(":")[-1]
    image_name = f"ubuntu/ros_{distro}"
    if args.gazebo:
        image_name += "_gazebo"

    docker = str(resources_path.joinpath("docker"))
    tmux_config = str(resources_path.joinpath("tmux"))
    bash = str(resources_path.joinpath("bash"))
    scripts = str(resources_path.joinpath("scripts"))

    # Build command construction
    build_cmd = [
        "docker", "build",
        "--progress", "tty",
        "--target", "dev",
        "--build-context", f"tmux={tmux_config}",
        "--build-context", f"bash={bash}",
        "--build-context", f"docker={docker}",
        "--build-context", f"scripts={scripts}",
        "--build-arg", f"USER_UID={getuid()}",
        "--build-arg", f"BASE_IMAGE={base_image}",
        "--build-arg", f"ros_distribution={distro}"
    ]

    if args.gazebo:
        gz_version = config_map[distro]["gz"]
        build_cmd += [
          "--build-arg", f"gz_distribution={gz_version}"
        ]

    build_cmd += [
        "--tag", f"{image_name}:{image_tag}",
        *args.extra_args,
        "--file", str(resources_path.joinpath("docker/base.Dockerfile")),
        "."
    ]

    print(" ".join(build_cmd))
