from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # The YOLO Vision Node
        Node(
            package='jime_controller',
            executable='yolo_detector',
            name='yolo_detector',
            output='screen'
        ),
        # The Brain/State Machine Node
        Node(
            package='jime_controller',
            executable='jime_brain',
            name='jime_brain',
            output='screen'
        ),
        # Optional: Add your camera node here if you want it to auto-start
        # Node(
        #     package='v4l2_camera',
        #     executable='v4l2_camera_node',
        #     name='camera',
        #     parameters=[{'video_device': '/dev/video0'}]
        # )
    ])