"""
ros-docker-env
"""
import argparse

from .builder import handle_build
from .runner import handle_run, handle_run_nvidia
from .settings import CONFIG_MAP


def route_run_command(args):
    """Routes the run command to function based on the --nvidia flag."""
    if args.nvidia:
        handle_run_nvidia(args)
    else:
        handle_run(args)


def main():
    """
    cli main
    """
    parser = argparse.ArgumentParser(prog="rosdocker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser(
      "build", help="Generate ROS image build command")

    build_parser.add_argument("rosdistro", choices=list(CONFIG_MAP.keys()))
    build_parser.add_argument(
      "--gazebo", action="store_true", help="Install gazebo to image")
    build_parser.add_argument("extra_args", nargs=argparse.REMAINDER)
    build_parser.set_defaults(func=handle_build)

    # Run Subcommand
    run_parser = subparsers.add_parser(
      "run", help="Run the ROS container")

    run_parser.add_argument(
      "--nvidia", action="store_true", help="Use nvidia images")
    run_parser.add_argument("image_name", help="Name of the image to run")
    run_parser.add_argument("extra_args", nargs=argparse.REMAINDER)
    run_parser.set_defaults(func=route_run_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
