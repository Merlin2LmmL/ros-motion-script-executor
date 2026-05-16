#!/usr/bin/env python3
"""
ROS2 Movement Executor Node
============================
Executes a sequence of movement instructions by publishing to /cmd_vel.

Usage:
  # With preset instructions (hardcoded defaults):
  ros2 run <your_package> movement_executor

  # With a JSON file:
  ros2 run <your_package> movement_executor --ros-args -p instructions_file:=/path/to/instructions.json

JSON Format Example:
  [
    {"action": "forward",  "linear_x": 0.5,  "angular_z": 0.0,  "duration": 2.0},
    {"action": "turn",     "linear_x": 0.0,  "angular_z": 0.5,  "duration": 1.5},
    {"action": "stop",     "linear_x": 0.0,  "angular_z": 0.0,  "duration": 0.5}
  ]

Supported fields per instruction:
  - action      (str)   : Human-readable label, used for logging only
  - linear_x    (float) : Forward/backward velocity  [m/s],  default 0.0
  - linear_y    (float) : Lateral velocity           [m/s],  default 0.0 (most robots ignore this)
  - linear_z    (float) : Vertical velocity          [m/s],  default 0.0
  - angular_x   (float) : Roll rate                  [rad/s], default 0.0
  - angular_y   (float) : Pitch rate                 [rad/s], default 0.0
  - angular_z   (float) : Yaw rate (turn)            [rad/s], default 0.0
  - duration    (float) : How long to execute        [s],     required
"""

import json
import os
import sys
import time

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from geometry_msgs.msg import Twist


# ---------------------------------------------------------------------------
# Default preset instructions (used when no JSON file is provided)
# ---------------------------------------------------------------------------
DEFAULT_INSTRUCTIONS = [
    {"action": "move_forward",   "linear_x": 0.3, "angular_z":  0.0, "duration": 2.0},
    {"action": "turn_left",      "linear_x": 0.0, "angular_z":  0.5, "duration": 1.5},
    {"action": "move_forward",   "linear_x": 0.3, "angular_z":  0.0, "duration": 2.0},
    {"action": "turn_right",     "linear_x": 0.0, "angular_z": -0.5, "duration": 1.5},
    {"action": "move_backward",  "linear_x":-0.3, "angular_z":  0.0, "duration": 1.0},
    {"action": "stop",           "linear_x": 0.0, "angular_z":  0.0, "duration": 0.5},
]


class MovementExecutorNode(Node):
    """Reads a list of movement instructions and publishes them to /cmd_vel."""

    PUBLISH_RATE_HZ = 10  # How often to publish each Twist command (Hz)

    def __init__(self) -> None:
        super().__init__("movement_executor")

        # ------------------------------------------------------------------
        # Declare parameters
        # ------------------------------------------------------------------
        self.declare_parameter("instructions_file", "")  # empty → use defaults
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("loop", False)             # repeat instructions forever

        # ------------------------------------------------------------------
        # Read parameters
        # ------------------------------------------------------------------
        file_path: str = (
            self.get_parameter("instructions_file")
            .get_parameter_value()
            .string_value
        )
        topic: str = (
            self.get_parameter("cmd_vel_topic")
            .get_parameter_value()
            .string_value
        )
        self._loop: bool = (
            self.get_parameter("loop")
            .get_parameter_value()
            .bool_value
        )

        # ------------------------------------------------------------------
        # Load instructions
        # ------------------------------------------------------------------
        if file_path:
            self._instructions = self._load_instructions(file_path)
        else:
            self.get_logger().info(
                "No instructions_file provided — using preset default instructions."
            )
            self._instructions = DEFAULT_INSTRUCTIONS

        if not self._instructions:
            self.get_logger().error("Instruction list is empty. Shutting down.")
            sys.exit(1)

        self.get_logger().info(
            f"Loaded {len(self._instructions)} instruction(s). "
            f"Publishing to '{topic}'. Loop={self._loop}"
        )

        # ------------------------------------------------------------------
        # Publisher
        # ------------------------------------------------------------------
        self._publisher = self.create_publisher(Twist, topic, 10)

        # ------------------------------------------------------------------
        # Start execution via a one-shot timer (gives the node time to spin up)
        # ------------------------------------------------------------------
        self._timer = self.create_timer(0.5, self._start_execution)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_instructions(self, file_path: str) -> list:
        """Load and validate a JSON instruction file."""
        abs_path = os.path.expanduser(file_path)
        if not os.path.isfile(abs_path):
            self.get_logger().error(f"Instructions file not found: '{abs_path}'")
            sys.exit(1)

        try:
            with open(abs_path, "r") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            self.get_logger().error(f"Failed to parse JSON: {exc}")
            sys.exit(1)

        if not isinstance(data, list):
            self.get_logger().error(
                "JSON file must contain a top-level list of instruction objects."
            )
            sys.exit(1)

        validated = []
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                self.get_logger().warn(f"Instruction #{i} is not a dict — skipping.")
                continue
            if "duration" not in item:
                self.get_logger().warn(
                    f"Instruction #{i} ('{item.get('action', '?')}') "
                    f"missing 'duration' — skipping."
                )
                continue
            validated.append(item)

        self.get_logger().info(
            f"Loaded {len(validated)}/{len(data)} valid instructions from '{abs_path}'."
        )
        return validated

    def _build_twist(self, instruction: dict) -> Twist:
        """Convert an instruction dict to a Twist message."""
        msg = Twist()
        msg.linear.x  = float(instruction.get("linear_x",  0.0))
        msg.linear.y  = float(instruction.get("linear_y",  0.0))
        msg.linear.z  = float(instruction.get("linear_z",  0.0))
        msg.angular.x = float(instruction.get("angular_x", 0.0))
        msg.angular.y = float(instruction.get("angular_y", 0.0))
        msg.angular.z = float(instruction.get("angular_z", 0.0))
        return msg

    def _execute_instruction(self, index: int, instruction: dict) -> None:
        """Publish a single instruction for its specified duration."""
        action   = instruction.get("action", f"step_{index}")
        duration = float(instruction["duration"])
        twist    = self._build_twist(instruction)

        self.get_logger().info(
            f"[{index + 1}/{len(self._instructions)}] '{action}' | "
            f"lin=({twist.linear.x:.2f}, {twist.linear.y:.2f}, {twist.linear.z:.2f}) "
            f"ang=({twist.angular.x:.2f}, {twist.angular.y:.2f}, {twist.angular.z:.2f}) "
            f"for {duration:.2f}s"
        )

        interval   = 1.0 / self.PUBLISH_RATE_HZ
        end_time   = time.time() + duration

        while time.time() < end_time:
            self._publisher.publish(twist)
            time.sleep(interval)

    def _publish_stop(self) -> None:
        """Send a zero-velocity command to halt the robot."""
        self._publisher.publish(Twist())
        self.get_logger().info("Published STOP command (zero velocity).")

    def _start_execution(self) -> None:
        """Entry point triggered once after node startup."""
        # Cancel the one-shot startup timer
        self._timer.cancel()

        run = 0
        try:
            while True:
                run += 1
                if self._loop:
                    self.get_logger().info(f"--- Starting loop iteration {run} ---")

                for i, instruction in enumerate(self._instructions):
                    self._execute_instruction(i, instruction)

                if not self._loop:
                    break

        except KeyboardInterrupt:
            self.get_logger().info("Interrupted by user.")
        finally:
            self._publish_stop()
            self.get_logger().info("Movement execution complete.")
            rclpy.shutdown()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(args=None) -> None:
    rclpy.init(args=args)
    node = MovementExecutorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
