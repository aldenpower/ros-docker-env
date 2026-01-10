# ros-docker-env

A simple Python package to manage a Docker-based ROS 2 environment.

*ros-docker-env* provides a small command-line interface and supporting Python code to help create, configure, and manage ROS 2 development environments using Docker. It aims to make working with ROS 2 inside containers more predictable, reproducible, and extensible.

## Motivation

Setting up a ROS 2 development environment typically requires coordinating multiple moving parts, like a compatible Ubuntu base image for each ROS 2 distribution and Optional simulation tools like Gazebo. This project exists to:
- Reduce friction when switching between ROS 2 distributions or machines
- Serve as a foundation for more advanced tooling in the future

## Scope

At the moment, ros-docker-env focuses on:
- Generating Docker build commands for ROS 2 images
- Selecting appropriate base images and simulation dependencies
- Providing a command-line interface

The long-term goal is to expand this into a more complete environment manager, including features such as
Running ROS 2 containers

## Installation

```bash
git clone https://github.com/aldenpower/ros-docker-env.git
cd ros-docker-env
pip install .
```

## Usage
Generate a build command for a ROS 2 image:
```bash
rosdocker build humble
```
Generate a build command including Gazebo:
```bash
rosdocker build jazzy --gazebo
```
Execute the generated command:
```bash
rosdocker build humble --gazebo | sh
```
For help:
```bash
rosdocker -h
```
