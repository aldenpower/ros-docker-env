ARG BASE_IMAGE=ubuntu:jammy
# Stage 1
FROM $BASE_IMAGE AS base

# Install sudo and basic deps
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    gnupg2 \
    lsb-release \
 && rm -rf /var/lib/apt/lists/*

ARG USER_UID
# ARG username
ENV USERNAME=ros2user

# Check if UID already exists, and only create user if it's free
RUN if getent passwd "$USER_UID" > /dev/null; then \
      echo "User with UID $USER_UID already exists. Skipping useradd."; \
      existing_user=$(getent passwd "$USER_UID" | cut -d: -f1); \
      usermod -l "$USERNAME" -d /home/"$USERNAME" -m "$existing_user"; \
    else \
      useradd -U --uid "$USER_UID" -ms /bin/bash "$USERNAME"; \
    fi \
 && echo "$USERNAME:$USERNAME" | chpasswd \
 && usermod -aG sudo "$USERNAME" \
 && echo "$USERNAME ALL=NOPASSWD: ALL" > /etc/sudoers.d/$USERNAME

USER $USERNAME

WORKDIR /home/$USERNAME

RUN sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tzdata \
    wget \
    bash-completion \
 && sudo ln -fs /usr/share/zoneinfo/America/Bahia /etc/localtime \
 && sudo dpkg-reconfigure --frontend noninteractive tzdata \
 && sudo rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN sudo apt update \
  && sudo apt install -y \
   build-essential \
   cmake \
   wget \
   software-properties-common \
   apt-utils \
   curl \
   gnupg2 \
   lsb-release \
   bash-completion \
  && sudo apt-get clean

# Stage 2
FROM base AS ros
ARG ros_distribution

RUN sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null \
 && sudo apt-get update && sudo apt-get install -y \
    ros-dev-tools \
    ros-${ros_distribution}-desktop \
    python3-rosdep \
 && sudo rosdep init && rosdep update \
 && sudo rm -rf /var/lib/apt/lists/*

# Stage 3
FROM ros AS gazebo
ARG gz_distribution

# Gazebo Installation
RUN sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
 && sudo apt-get update && sudo apt-get install -y \
    ${gz_distribution} \
 && sudo rm -rf /var/lib/apt/lists/*

# --- STAGE 4: DEV ---
FROM gazebo AS dev
ARG ros_distribution

COPY --from=tmux_config tmux.conf /home/ros2user/.tmux.conf
COPY --from=bash bash_aliases /home/ros2user/.bash_aliases
COPY --from=docker entrypoint.sh /home/ros2user/entrypoint.sh

RUN sudo apt update \
 && sudo apt install -y \
   vim \
   tmux \
 && sudo rm -rf /var/lib/apt/lists/*

# 2. Create ROS2 Workspace
RUN mkdir -p ~/ros2_ws/src

RUN if [ -f ~/.bashrc ]; then \
    echo ". /opt/ros/${ros_distribution}/setup.bash" >> ~/.bashrc; \
    fi

ENTRYPOINT ["/home/ros2user/entrypoint.sh"]
CMD ["bash"]
