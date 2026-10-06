"""Docker container runner."""

import os
import subprocess
import sys

from .utils import eprint


def get_base_run_args():
    """Return common arguments for Docker runs."""
    return [
        "docker",
        "run",
        "-it",
        "--net=host",
        "--ipc=host",
        "--env",
        f"DISPLAY={os.environ.get('DISPLAY', '')}",
        "--volume",
        "/tmp/.X11-unix:/tmp/.X11-unix:rw",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
    ]


def build_run_command(args, nvidia=False):
    """Build the Docker run command."""
    run_cmd = get_base_run_args()

    if nvidia:
        run_cmd.extend([
            "--gpus",
            "all",
            "--env",
            "NVIDIA_VISIBLE_DEVICES=all",
            "--env",
            "NVIDIA_DRIVER_CAPABILITIES=all",
            "--device",
            "/dev/dri:/dev/dri",
            "--shm-size=1g",
        ])
    else:
        run_cmd.extend([
            "--device",
            "/dev/dri",
        ])

    run_cmd.extend(args.extra_args)

    run_cmd.append(args.image_name)

    run_cmd.extend(args.container_command)

    return run_cmd


def run_container(args, nvidia=False):
    """Run the Docker container."""
    run_cmd = build_run_command(args, nvidia=nvidia)

    mode = "NVIDIA" if nvidia else "Standard"
    print(f"Running ({mode}): {' '.join(run_cmd)}")

    try:
        subprocess.run(run_cmd, check=True)
    except subprocess.CalledProcessError as e:
        eprint(f"Docker run failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def handle_run(args):
    """Run a standard Docker container."""
    run_container(args)


def handle_run_nvidia(args):
    """Run a Docker container with NVIDIA support."""
    run_container(args, nvidia=True)
