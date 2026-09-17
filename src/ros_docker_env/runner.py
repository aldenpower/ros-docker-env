"""TODO"""
import os
import sys
import subprocess
from ros_docker_env.utils import eprint


def get_base_run_args(args):
    """Common arguments for both standard and NVIDIA runs."""
    return [
        "docker", "run", "-it",
        "--net=host",
        "--ipc=host",  # Crucial for ROS 2 DDS communication
        "--env", f"DISPLAY={os.environ.get('DISPLAY')}",
        "--volume", "/tmp/.X11-unix:/tmp/.X11-unix:rw",
        "--user", f"{os.getuid()}:{os.getgid()}",
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
