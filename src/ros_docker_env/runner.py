import sys
from os import environ
import subprocess
from ros_docker_env.utils import eprint


def get_base_run_args(args):
    """Common arguments for both standard and NVIDIA runs."""
    return [
        "docker", "run", "-it",
        "--net=host",
        "--ipc=host",  # Crucial for ROS 2 DDS communication
        "--env", f"DISPLAY={environ.get('DISPLAY')}",
        "--volume", "/tmp/.X11-unix:/tmp/.X11-unix:rw",
    ]

def handle_run(args):
    run_cmd = get_base_run_args(args) + [
        "--device", "/dev/dri",
        *args.extra_args,
        args.image_name
    ]
    print(f"Running (Standard): {' '.join(run_cmd)}")
    subprocess.run(run_cmd)


def handle_run_nvidia(args):
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
