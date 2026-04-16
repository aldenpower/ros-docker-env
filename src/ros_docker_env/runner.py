from os import environ
import subprocess


def handle_run(args):
    run_cmd = [
        "docker", "run", "-it", "--rm",
        "--net=host",
        "--env", f"DISPLAY={environ.get('DISPLAY')}",
        "--volume", "/tmp/.X11-unix:/tmp/.X11-unix",
        "--device", "/dev/dri",
        *args.extra_args,
        args.image_name
    ]
    print(f"{' '.join(run_cmd)}")
    subprocess.run(run_cmd)


def handle_run_nvidia(args):
    run_cmd = [
        "docker", "run", "-it",
        "--net=host",
        "--gpus", "all",
        "--env", "NVIDIA_VISIBLE_DEVICES=all",
        "--env", "NVIDIA_DRIVER_CAPABILITIES=all",
        "--env", f"DISPLAY={environ.get('DISPLAY')}",
        "--volume", "/tmp/.X11-unix:/tmp/.X11-unix",
        # optional shared memory improvement for Gazebo
        "--shm-size=1g",
        *args.extra_args,
        args.image_name
    ]

    print(" ".join(run_cmd))
    subprocess.run(run_cmd)
