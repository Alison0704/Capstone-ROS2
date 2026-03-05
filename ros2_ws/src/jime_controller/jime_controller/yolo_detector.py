#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
from ultralytics import YOLO

class PiYoloDetector(Node):
    def __init__(self):
        super().__init__('pi_yolo_detector')
        
        self.model = YOLO('yolov8n.pt') 
        self.cap = cv2.VideoCapture(0)
        
        self.publisher_ = self.create_publisher(String, 'detections', 10)
        
        self.timer = self.create_wall_timer(0.1, self.timer_callback)
        self.get_logger().info("Pi YOLO Brain is online.")

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            results = self.model(frame, classes=[0], verbose=False)
            for result in results:
                if len(result.boxes) > 0:
                    msg = String()
                    msg.data = f"Detected {len(result.boxes)} people!"
                    self.publisher_.publish(msg)
                    self.get_logger().info(msg.data)
        else:
            # This is what you'll see in Docker until you move to the Pi
            self.get_logger().warn("Hardware camera not found - this is normal in Docker!", once=True)

def main(args=None):
    rclpy.init(args=args)
    node = PiYoloDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cap.release()
        rclpy.shutdown()

if __name__ == '__main__':
    main()