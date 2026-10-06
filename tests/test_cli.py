from argparse import Namespace
from unittest.mock import patch

import pytest

from ros_docker_env import CONFIG_MAP, handle_build, handle_run, handle_run_nvidia


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


@pytest.mark.parametrize("nvidia", [False, True])
@pytest.mark.parametrize("gazebo", [False, True])
@pytest.mark.parametrize(
    "distro,config",
    CONFIG_MAP.items(),
)
def test_run_distribution(distro, config, gazebo, nvidia, capsys):
    image_tag = config["base"].split(":")[-1]

    image_name = f"ubuntu/ros_{distro}"
    if gazebo:
        image_name += "_gazebo"

    image_name = f"{image_name}:{image_tag}"

    args = Namespace(
        image_name=image_name,
        extra_args=[],
        container_command=[],
    )

    with patch("ros_docker_env.runner.subprocess.run"):
        if nvidia:
            handle_run_nvidia(args)
        else:
            handle_run(args)

    output = capsys.readouterr().out.strip()

    # Common assertions
    assert "docker run" in output
    assert "--net=host" in output
    assert image_name in output

    # NVIDIA assertions
    if nvidia:
        assert "--gpus all" in output
        assert "NVIDIA_VISIBLE_DEVICES=all" in output
        assert "NVIDIA_DRIVER_CAPABILITIES=all" in output
    else:
        assert "--device /dev/dri" in output
