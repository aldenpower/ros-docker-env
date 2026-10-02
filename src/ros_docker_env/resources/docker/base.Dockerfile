ARG BASE_IMAGE=ubuntu:jammy
# Stage 1
FROM ${BASE_IMAGE} AS base

ARG USER_UID
# ARG username
ENV USERNAME=ros2user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        sudo \
        curl \
        gnupg2 \
        lsb-release \
        ca-certificates \
        tzdata \
        bash-completion \
        build-essential \
        cmake \
        wget \
        software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN if getent passwd "${USER_UID}" > /dev/null; then \
        existing_user="$(getent passwd "${USER_UID}" | cut -d: -f1)"; \
        usermod \
            --login "${USERNAME}" \
            --home "/home/${USERNAME}" \
            --move-home \
            "${existing_user}"; \
    else \
        useradd \
            --uid "${USER_UID}" \
            --create-home \
            --shell /bin/bash \
            "${USERNAME}"; \
    fi \
    && usermod -aG sudo "${USERNAME}" \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" \
        > "/etc/sudoers.d/${USERNAME}"


USER ${USERNAME}
WORKDIR /home/${USERNAME}


# Stage 2
FROM base AS ros
ARG ROS_DISTRO
ENV ROS_DISTRO=${ROS_DISTRO}

RUN sudo curl -sSL \
        https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
    | sudo gpg --dearmor \
        -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
        | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null \
    && sudo apt-get update \
    && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
        ros-dev-tools \
        ros-${ROS_DISTRO}-desktop \
        python3-rosdep \
    && sudo rosdep init \
    && rosdep update \
    && sudo rm -rf /var/lib/apt/lists/*


# Stage 3
FROM ros AS gazebo
ARG GZ_DISTRO
ENV GZ_DISTRO=${GZ_DISTRO}

RUN sudo curl -fsSL \
        https://packages.osrfoundation.org/gazebo.gpg \
        -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
        | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && sudo apt-get update \
    && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
        ${GZ_DISTRO} \
    && sudo rm -rf /var/lib/apt/lists/*

# --- STAGE 4: DEV ---

FROM gazebo AS dev

RUN sudo apt-get update \
    && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
        vim \
        tmux \
    && sudo rm -rf /var/lib/apt/lists/*

RUN mkdir -p "${HOME}/ros2_ws"

COPY --from=tmux tmux.conf /home/${USERNAME}/.tmux.conf
COPY --from=bash bash_aliases /home/${USERNAME}/.bash_aliases
COPY --from=bash bash_prompt /home/${USERNAME}/.bash_prompt

COPY --from=scripts . /usr/local/bin/
COPY --from=docker entrypoint.py /usr/local/bin/entrypoint.py

RUN printf '\n[ -f "$HOME/.bash_prompt" ] && . "$HOME/.bash_prompt"\n' \
        >> "${HOME}/.bashrc" \
    && printf '\nsource /opt/ros/%s/setup.bash\n' "${ROS_DISTRO}" \
        >> "${HOME}/.bashrc"

ENTRYPOINT ["python3", "/usr/local/bin/entrypoint.py"]

CMD ["bash"]
