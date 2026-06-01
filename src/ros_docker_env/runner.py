"""TODO"""
import os
import sys
import subprocess
from ros_docker_env.utils import eprint
from ros_docker_env import resources_path


def ensure_volume_exists(volume_name):
    """Create Docker named volume if it does not exist."""

    try:
        result = subprocess.run(
          ["docker", "volume", "inspect", volume_name],
          stdout=subprocess.DEVNULL,
          stderr=subprocess.DEVNULL,
          check=True
        )
        if result.returncode != 0:
            print(f"Creating Docker volume: {volume_name}")

            subprocess.run(
                ["docker", "volume", "create", volume_name],
                check=True
            )
    except subprocess.CalledProcessError as e:
        eprint(f"Docker build failed with exit code {e.returncode}")
        sys.exit(e.returncode)



def get_base_run_args(args):
    """Common arguments for both standard and NVIDIA runs."""

    ensure_volume_exists("ros2_ws")

    entrypoint = str(resources_path.joinpath("docker/entrypoint.sh"))
    print(entrypoint)

    return [
        "docker", "run", "-it",
        "--net=host",
        "--ipc=host",  # Crucial for ROS 2 DDS communication
        "--env", f"DISPLAY={os.environ.get('DISPLAY')}",
        "--volume", "/tmp/.X11-unix:/tmp/.X11-unix:rw",
        "--user", f"{os.getuid()}:{os.getgid()}",
        # Persistent ROS 2 workspace cache
        "--volume", "ros2_ws:/home/ros2user/ros2_ws",
    ]

def handle_run(args):
    """TODO"""
    run_cmd = get_base_run_args(args) + [
        "--device", "/dev/dri",
        *args.extra_args,
        args.image_name
    ]
    print(f"Running (Standard): {' '.join(run_cmd)}")
    try:
        subprocess.run(run_cmd, check=True)
    except subprocess.CalledProcessError as e:
        eprint(f"Docker build failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def handle_run_nvidia(args):
    """TODO"""
    run_cmd = get_base_run_args(args) + [
        "--gpus", "all",
        "--env", "NVIDIA_VISIBLE_DEVICES=all",
        "--env", "NVIDIA_DRIVER_CAPABILITIES=all",
        "--device", "/dev/dri:/dev/dri",
        "--shm-size=1g",
        *args.extra_args,
        args.image_name
    ]
    print(f"Running (NVIDIA): {' '.join(run_cmd)}")
    try:
        subprocess.run(run_cmd, check=True)
    except subprocess.CalledProcessError as e:
        eprint(f"Docker build failed with exit code {e.returncode}")
        sys.exit(e.returncode)
