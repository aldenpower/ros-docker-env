import argparse
from ros_docker_env.builder import handle_build
from ros_docker_env.runner import handle_run_nvidia


def main():
    parser = argparse.ArgumentParser(prog="rosdocker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser(
      "build", help="Generate ROS image build command")

    build_parser.add_argument("rosdistro", choices=["humble", "jazzy", "kilted"])
    build_parser.add_argument(
      "--gazebo", action="store_true", help="Install gazebo to image")
    build_parser.add_argument(
      "--nvidia", action="store_true", help="Use nvidia images")
    build_parser.set_defaults(func=handle_build)

    # Run Subcommand
    run_parser = subparsers.add_parser(
      "run", help="Run the ROS container")

    run_parser.add_argument("image_name", help="Name of the image to run")
    run_parser.add_argument("extra_args", nargs=argparse.REMAINDER)
    run_parser.set_defaults(func=handle_run_nvidia)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
