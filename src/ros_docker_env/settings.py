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
