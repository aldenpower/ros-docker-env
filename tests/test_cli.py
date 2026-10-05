from argparse import Namespace

import pytest

from ros_docker_env import CONFIG_MAP, handle_build


@pytest.mark.parametrize(
    "distro,config",
    CONFIG_MAP.items(),
)
def test_build_distribution(distro, config, capsys):
    args = Namespace(
        rosdistro=distro,
        gazebo=False,
        extra_args=[],
    )

    handle_build(args)

    output = capsys.readouterr().out.strip()

    assert f"--build-arg ROS_DISTRO={distro}" in output
    assert f"BASE_IMAGE={config['base']}" in output


# @pytest.mark.parametrize("distro", CONFIG_MAP)
# def test_build_command(distro):
#     args = Namespace(
#         rosdistro=distro,
#         gazebo=False,
#         extra_args=[],
#     )

#     command = handle_build(args)

#     assert "docker build" in command
#     assert f"BASE_IMAGE={CONFIG_MAP[distro]['base']}" in command
#     assert f"ROS_DISTRO={distro}" in command
#     assert "--target dev" in command


# @pytest.mark.parametrize("distro", CONFIG_MAP)
# def test_build_command_with_gazebo(distro):
#     args = Namespace(
#         rosdistro=distro,
#         gazebo=True,
#         extra_args=[],
#     )

#     command = handle_build(args)

#     assert f"GZ_DISTRO={CONFIG_MAP[distro]['gz']}" in command
#     assert f"ubuntu/ros_{distro}_gazebo" in command


# # @pytest.mark.integration
# @pytest.mark.parametrize("distro", CONFIG_MAP)
# def test_docker_build(distro):
#     args = Namespace(
#         rosdistro=distro,
#         gazebo=False,
#         extra_args=[],
#     )

#     command = handle_build(args)

#     print(command)

#     result = subprocess.run(
#         ["/usr/bin/bash"],
#         input=command,
#         text=True,
#         check=False,
#     )

#     # assert result.returncode == 0
