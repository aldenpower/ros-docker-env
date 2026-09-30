import subprocess

from ros_docker_env.settings import CONFIG_MAP


def test_build_ros_distros():
    """
    test_build_ros_distros
    """
    for rosdistro in CONFIG_MAP:

        result = subprocess.run(
          ["rosdocker", "build", rosdistro],
            capture_output=True,
            text=True,
            check=False
        )
        print(result.stdout)

        assert result.returncode == 0
        assert rosdistro in result.stdout
