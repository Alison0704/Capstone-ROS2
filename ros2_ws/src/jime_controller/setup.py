import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'jime_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=[
        'setuptools',
        'ultralytics',    
        'mediapipe',      
        'opencv-python',  
    ],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='Host Robot Controller for Phase 1-5',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'jime_brain = jime_controller.jime_brain:main',
            'yolo_detector = jime_controller.yolo_detector:main',
        ],
    },
)