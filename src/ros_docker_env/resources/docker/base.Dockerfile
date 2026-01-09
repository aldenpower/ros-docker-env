ARG base_image=ubuntu:jammy
FROM $base_image AS base

RUN apt update \
 && apt install -y \
   sudo

ARG user_id
ARG username
ENV USERNAME=$username

# Check if UID already exists, and only create user if it's free
RUN if getent passwd "$user_id" > /dev/null; then \
      echo "User with UID $user_id already exists. Skipping useradd."; \
      existing_user=$(getent passwd "$user_id" | cut -d: -f1); \
      usermod -l "$USERNAME" -d /home/"$USERNAME" -m "$existing_user"; \
    else \
      useradd -U --uid "$user_id" -ms /bin/bash "$USERNAME"; \
    fi \
 && echo "$USERNAME:$USERNAME" | chpasswd \
 && usermod -aG sudo "$USERNAME" \
 && echo "$USERNAME ALL=NOPASSWD: ALL" > /etc/sudoers.d/$USERNAME

USER $USERNAME

WORKDIR /home/$USERNAME

RUN export DEBIAN_FRONTEND=noninteractive \
 && sudo apt-get update \
 && sudo -E apt-get install -y \
    tzdata \
    apt-utils \
 && sudo ln -fs /usr/share/zoneinfo/America/Bahia /etc/localtime \
 && sudo dpkg-reconfigure --frontend noninteractive tzdata \
 && sudo apt-get clean

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN sudo apt update \
  && sudo apt install -y \
   build-essential \
   cmake \
   wget \
   git \
   software-properties-common \
   apt-utils \
   curl \
   gnupg2 \
   lsb-release \
   bash-completion \
  && sudo apt-get clean

FROM base AS ros

# Name of the ROS distribution
ARG ros_distribution

#     # Add the ROS2 repository and GPG key
RUN sudo curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
RUN sudo /bin/sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'

RUN sudo apt update && sudo apt install -y \
    ros-dev-tools \
    ros-${ros_distribution}-desktop

RUN sudo apt update && \
    sudo apt install -y \
    python3-pip \
    python3-rosdep
    # && sudo rm -rf /var/lib/apt/lists/*

# Initialize rosdep
RUN sudo rosdep init && \
    rosdep update

FROM ros AS gazebo

# Name of the Gazebo distribution
ARG gz_distribution

RUN sudo /bin/bash -c 'curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg'
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
RUN sudo apt-get update
RUN sudo apt install -y \
  ${gz_distribution}

FROM ros AS dev

CMD ["bash"]
