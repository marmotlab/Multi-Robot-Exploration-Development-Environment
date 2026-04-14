from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # 把 robot_0/map 对齐到全局 map（即没有偏移）
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="robot0_map_to_global",
            arguments=["0", "0", "0", "0", "0", "0", "map", "robot_0/map"]
        ),

        # 把 robot_1/map 偏移到全局 map 
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="robot1_map_to_global",
            arguments=["3.4", "-6.0", "0", "0", "0", "0", "map", "robot_1/map"]
        ),
        # Node(
        #     package="tf2_ros",
        #     executable="static_transform_publisher",
        #     name="robot2_map_to_global",
        #     arguments=["5.7", "8.0", "0", "0", "0", "0", "map", "robot_2/map"]
        # ),
    
    ])
