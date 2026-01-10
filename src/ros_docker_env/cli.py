import argparse
from ros_docker_env.builder import handle_build


def main():
    parser = argparse.ArgumentParser(prog="rosdocker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser(
      "build", help="Generate ROS image build command")

    parser.add_argument("rosdistro", choices=["humble", "jazzy", "kilted"])
    parser.add_argument(
      "--gazebo", action="store_true", help="Install gazebo to image")
    build_parser.set_defaults(func=handle_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
