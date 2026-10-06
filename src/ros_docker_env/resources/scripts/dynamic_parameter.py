#!/usr/bin/env python3

import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node


class DynamicParameterTest(Node):

    def __init__(self):
        super().__init__("dynamic_parameter_test")

        self.declare_parameter("speed", 100.0)
        self.declare_parameter("enabled", True)
        self.declare_parameter("name", "param")

        self.add_on_set_parameters_callback(
            self.parameters_callback
        )

        self.get_logger().info("Dynamic parameter test node started")

    def parameters_callback(self, params):
        for param in params:
            self.get_logger().info(
                f"Parameter changed: {param.name} = {param.value}"
            )

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)

    node = DynamicParameterTest()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
