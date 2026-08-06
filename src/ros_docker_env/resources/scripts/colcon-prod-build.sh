cd /home/ros2user/ros2_ws

colcon build \
  --merge-install \
  --cmake-args -DCMAKE_BUILD_TYPE=Release
