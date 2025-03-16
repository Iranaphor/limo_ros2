import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    limo_navigation_prefix = get_package_share_directory('limo_navigation')
    rviz_config_dir = os.path.join(get_package_share_directory('limo_navigation'), 'rviz', 'limo_navigation.rviz')
    map_yaml_file = LaunchConfiguration('map_yaml_file', default=os.path.join(limo_navigation_prefix, 'maps', 'map.yaml'))
    initial_pose = LaunchConfiguration('initial_pose', default='[0.0, 0.0, 0.0]')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'map_yaml_file',
            default_value=map_yaml_file,
            description='Full path to the map yaml file to load'
        ),
        DeclareLaunchArgument(
            'initial_pose',
            default_value='[0.0, 0.0, 0.0]',
            description='Initial pose to start from [x, y, theta]'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        ),
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'yaml_filename': map_yaml_file}],
            remappings=[('/map', '/map')]
        ),
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='nav2_amcl',
                    executable='amcl',
                    name='amcl',
                    output='screen',
                    parameters=[
                        {'use_sim_time': use_sim_time},
                        {'yaml_filename': map_yaml_file}
                    ],
                    remappings=[('/scan', 'scan'), ('/map', '/map')]
                )
            ]
        ),
        TimerAction(
            period=10.0,
            actions=[
                Node(
                    package='slam_toolbox',
                    executable='async_slam_toolbox_node',
                    name='slam_toolbox',
                    output='screen',
                    parameters=[
                        {'use_sim_time': use_sim_time},
                        {'mode': 'localization'},
                        {'map_start_pose': initial_pose},
                        {'use_map_saver': True}
                    ],
                    remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static'), ('/scan', 'scan'), ('/map', '/map')]
                )
            ]
        )
    ])