from argparse import Namespace

import pytest

from ros_docker_env import CONFIG_MAP, handle_build


@pytest.mark.parametrize("gazebo", [False, True])
@pytest.mark.parametrize(
    "distro,config",
    CONFIG_MAP.items(),
)
def test_build_distribution(distro, config, gazebo, capsys):
    args = Namespace(
        rosdistro=distro,
        gazebo=gazebo,
        extra_args=[],
    )

    handle_build(args)

    output = capsys.readouterr().out.strip()

    # Common assertions
    assert "docker build" in output
    assert f"--build-arg ROS_DISTRO={distro}" in output
    assert f"BASE_IMAGE={config['base']}" in output

    # Gazebo assertions
    if gazebo:
        assert f"--build-arg GZ_DISTRO={config['gz']}" in output
