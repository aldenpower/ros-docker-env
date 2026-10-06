"""
ros-docker-env
"""
import argparse

from .builder import handle_build
from .runner import handle_run, handle_run_nvidia
from .settings import CONFIG_MAP, RUN_EPILOG


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
      "run", help="Run the ROS container",
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=RUN_EPILOG,)

    run_parser.add_argument(
      "--nvidia", action="store_true", help="Use nvidia images")
    run_parser.add_argument(
      "--docker-arg", dest="extra_args", action="append",
      default=[], help="Extra argument passed to docker run",
    )
    run_parser.add_argument("image_name", help="Name of the image to run")
    run_parser.add_argument(
        "container_command",
        nargs=argparse.REMAINDER,
        metavar="COMMAND",
        help="Command to execute inside the container",
    )
    run_parser.set_defaults(func=route_run_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
