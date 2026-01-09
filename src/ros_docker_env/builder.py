import os
import sys
import argparse
from importlib import resources
from ros_docker_env.utils import eprint


def main():
    parser = argparse.ArgumentParser(prog="rosdocker")
    parser.add_argument("rosdistro", choices=["humble", "jazzy", "kilted"])
    parser.add_argument(
      "--gazebo", action="store_true", help="Install gazebo to image")
    args = parser.parse_args()

    image_name = f"ubuntu/ros_{args.rosdistro}"

    docker_files_dir = resources.files(
      "ros_docker_env.resources").joinpath("docker")

    base_docker_file_path = docker_files_dir.joinpath("base.Dockerfile")

    try:
        user_id = os.getuid()
        username = os.environ.get("USER", "user")

        build_cmd = [
          "docker", "build",
          "--progress",
          "tty",
          "--build-arg",
          f"user_id={user_id}",
          "--build-arg",
          f"username={username}",
        ]
        if args.rosdistro == "humble":
            base_image = "ubuntu:jammy"
        else:
            base_image = "ubuntu:noble"

        build_cmd += [
          "--build-arg",
          f"base_image={base_image}",
          "--build-arg",
          f"ros_distribution={args.rosdistro}",
          "--target",
          "ros",
        ]

        if args.gazebo:
            image_name += "_gazebo"
            idx = build_cmd.index("--target")
            build_cmd[idx + 1] = "gazebo"

            gz_map = {
                "humble": "ignition-fortress",
                "jazzy": "gz-harmonic",
                "kilted": "gz-jetty",
            }
            build_cmd += ["--build-arg",
                          f"gz_distribution={gz_map[args.rosdistro]}"]

        image_name += f":{base_image.split(":")[1]}"

        build_cmd += [
          "--tag",
          image_name,
          "--file", str(base_docker_file_path),
          ".",
        ]

    except Exception as e:
        eprint(f"line {sys.exc_info()[-1].tb_lineno}: {e}")
        print(f"[UNEXPECTED ERROR] {type(e).__name__}: {e}")
        sys.exit(1)

    print(" ".join(build_cmd))


if __name__ == '__main__':
    main()
