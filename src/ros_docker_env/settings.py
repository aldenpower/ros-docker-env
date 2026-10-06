"""
ros-docker-env
"""
from importlib import resources

resources_path = resources.files("ros_docker_env.resources")

# Mapping configuration
# good to know: https://gazebosim.org/docs/latest/ros_installation/
CONFIG_MAP = {
    "humble": {
        "base": "ubuntu:jammy",
        "gz": "ignition-fortress"
    },
    "jazzy": {
        "base": "ubuntu:noble",
        "gz": "gz-harmonic"
    },
    "kilted": {
        "base": "ubuntu:noble",
        "gz": "gz-ionic"
    },
    "lyrical": {
        "base": "ubuntu:resolute",
        "gz": "gz-jetty"
    }
}


RUN_EPILOG = """
examples:
  Run an image:
    rosdocker run ros:jazzy

  Run with NVIDIA support:
    rosdocker run --nvidia ubuntu/ros_lyrical_gazebo:resolute

  Execute a command inside the container:
    rosdocker run ubuntu/ros_lyrical_gazebo:resolute ros2 topic list

  Execute a shell command:
    rosdocker run ubuntu/ros_lyrical_gazebo:resolute bash -c "echo hello"

  Pass extra arguments to docker run:
    rosdocker run --docker-arg=--rm ubuntu/ros_lyrical_gazebo:resolute

  Pass multiple Docker arguments:
    rosdocker run \\
      --docker-arg=--rm \\
      --docker-arg=--privileged \\
      ubuntu/ros_lyrical_gazebo:resolute

  Pass Docker arguments and execute a command:
    rosdocker run \\
      --docker-arg=--rm \\
      --docker-arg="--volume=/dev:/dev" \\
      ubuntu/ros_lyrical_gazebo:resolute \\
      ros2 topic list
"""
