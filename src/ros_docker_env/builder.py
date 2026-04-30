import sys
from os import getuid, environ
from importlib import resources
from ros_docker_env.utils import eprint

import sys
from os import getuid, environ
from importlib import resources
from ros_docker_env.utils import eprint

def handle_build(args):
    # Mapping configuration
    config_map = {
        "humble": {
            "base": "ubuntu:jammy",
            "nvidia": "nvidia/opengl:1.0-glvnd-devel-ubuntu22.04",
            "gz": "ignition-fortress"
        },
        "jazzy": {
            "base": "ubuntu:noble",
            "nvidia": "nvidia/cuda:12.9.1-cudnn-devel-ubuntu24.04",
            "gz": "gz-harmonic"
        },
        "kilted": {
            "base": "ubuntu:noble",
            "nvidia": "nvidia/cuda:12.9.1-cudnn-devel-ubuntu24.04",
            "gz": "gz-ionic"
        }
    }

    distro = args.rosdistro
    if distro not in config_map:
        eprint(f"Unsupported ROS distribution: {distro}")
        sys.exit(1)

    try:
        # Determine base image and Gazebo version
        base_image = config_map[distro]["nvidia"] if args.nvidia else config_map[distro]["base"]
        gz_version = config_map[distro]["gz"] if args.gazebo else ""

        image_tag = base_image.split(":")[-1]
        image_name = f"ubuntu/ros_{distro}"
        if args.gazebo:
            image_name += "_gazebo"

        # Build command construction
        build_cmd = [
            "docker", "build",
            "--progress", "tty",
            "--target", "dev",
            "--build-arg", f"user_id={getuid()}",
            "--build-arg", f"username={environ.get('USER', 'user')}",
            "--build-arg", f"base_image={base_image}",
            "--build-arg", f"ros_distribution={distro}",
            "--build-arg", f"gz_distribution={gz_version}",
            "--tag", f"{image_name}:{image_tag}",
            "--file", str(resources.files("ros_docker_env.resources").joinpath("docker/base.Dockerfile")),
            "."
        ]

        print(" ".join(build_cmd))
        # Optional: subprocess.run(build_cmd)

    except Exception as e:
        eprint(f"Build setup failed: {e}")
        sys.exit(1)
