import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class MacCamBridge(Node):
    def __init__(self):
        super().__init__('mac_cam_bridge')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()
        
        # Aggressive FFMPEG settings to prevent hanging
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "probesize;32|analyzeduration;0|flags;low_delay|fflags;nobuffer"
        
        # Listen on 0.0.0.0 (all interfaces)
        self.url = "udp://0.0.0.0:1234?overrun_nonfatal=1&fifo_size=50000000"
        self.get_logger().info(f"Opening stream: {self.url}")
        
        self.cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        
        if not self.cap.isOpened():
            self.get_logger().error("COULD NOT OPEN STREAM! Check Mac FFmpeg.")
        else:
            self.get_logger().info("Stream opened successfully. Publishing to /camera/image_raw")

        self.timer = self.create_timer(0.01, self.timer_callback)

    def timer_callback(self):
        # Use grab() + retrieve() for faster performance than read()
        if self.cap.grab():
            ret, frame = self.cap.retrieve()
            if ret:
                msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                self.publisher_.publish(msg)
        else:
            # If we lose the stream, try to re-initialize
            self.get_logger().warn("Dropped frame or stream lost...", once=True)

def main(args=None):
    rclpy.init(args=args)
    node = MacCamBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cap.release()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
