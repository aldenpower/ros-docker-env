from os import environ
import subprocess


def handle_run(args):
    run_cmd = [
        "docker", "run", "-it", "--rm",
        "--net=host",
        "--env", f"DISPLAY={environ.get('DISPLAY')}",
        "--volume", "/tmp/.X11-unix:/tmp/.X11-unix",
        "--device", "/dev/dri",
        args.image_name
    ]
    print(f"{' '.join(run_cmd)}")
    subprocess.run(run_cmd)
