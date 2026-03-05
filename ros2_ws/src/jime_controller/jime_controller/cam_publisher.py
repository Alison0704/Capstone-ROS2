import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class MacCamBridge(Node):
    def __init__(self):
        super().__init__('mac_cam_bridge')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()
        
        # We connect to the stream coming from your Mac host
        # 'host.docker.internal' is the special address to talk back to your Mac
        self.cap = cv2.VideoCapture("udp://192.168.2.12:1234")
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(msg)
        else:
            self.get_logger().warn("Waiting for Mac camera stream...")

def main():
    rclpy.init()
    rclpy.spin(MacCamBridge())
    rclpy.shutdown()

if __name__ == '__main__':
    main()