#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from enum import Enum
from geometry_msgs.msg import Twist
from std_msgs.msg import String  # Unified with your YOLO node

class State(Enum):
    IDLE_WAIT = 1   # Spinning/Scanning for a person
    APPROACH  = 2   # Person found, moving toward them
    OBSTACLE  = 3   # Path blocked, performing avoidance maneuver
    ARRIVED   = 4   # Goal reached, stopping
    HOMING    = 5   # Returning to start

class JimeBrain(Node):
    def __init__(self):
        super().__init__('jime_brain')
        
        # Publishers & Subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.yolo_sub = self.create_subscription(
            String, 
            'detections', 
            self.detection_callback, 
            10)

        # Internal State & Variables
        self.current_state = State.IDLE_WAIT
        self.last_detection_time = self.get_clock().now()
        
        # Main Control Loop (10Hz)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.state_machine_loop)
        
        self.get_logger().info("JIME Brain Online. Initial State: IDLE_WAIT (Scanning)")

    def detection_callback(self, msg):
        """Triggered when the YOLO node sends a detection string"""
        if "Detected" in msg.data:
            self.last_detection_time = self.get_clock().now()
            
            # Transition from Scanning to Approaching if we see someone
            if self.current_state == State.IDLE_WAIT:
                self.get_logger().info("Person detected! Switching to APPROACH.")
                self.current_state = State.APPROACH

    def state_machine_loop(self):
        """The heart of the robot: acts based on current state"""
        msg = Twist()
        now = self.get_clock().now()
        
        # --- TIMEOUT LOGIC ---
        # If we haven't seen anyone for 3 seconds, go back to scanning
        time_since_last = (now - self.last_detection_time).nanoseconds / 1e9
        if self.current_state == State.APPROACH and time_since_last > 3.0:
            self.get_logger().warn("Target lost. Returning to IDLE_WAIT.")
            self.current_state = State.IDLE_WAIT

        # --- STATE ACTIONS ---
        if self.current_state == State.IDLE_WAIT:
            # Spin slowly to look around
            msg.angular.z = 0.6
            self.get_logger().info("Scanning...", throttle_duration_sec=5.0)

        elif self.current_state == State.APPROACH:
            # Move forward toward the target
            msg.linear.x = 0.25 
            msg.angular.z = 0.0
            self.get_logger().info("Target Locked: Approaching.", throttle_duration_sec=5.0)

        elif self.current_state == State.OBSTACLE:
            # Simple avoidance: back up and turn
            msg.linear.x = -0.1
            msg.angular.z = 1.0
            
        elif self.current_state == State.ARRIVED:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        # Publish the movement command
        self.cmd_vel_pub.publish(msg)

    def stop_robot(self):
        """Emergency stop utility"""
        msg = Twist()
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info("Robot stopped.")

def main(args=None):
    rclpy.init(args=args)
    node = JimeBrain()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt detected.")
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()