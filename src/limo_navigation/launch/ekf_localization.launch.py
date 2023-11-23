import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Get the launch directory
    launch_dir = os.path.join(
        get_package_share_directory('limo_navigation'), 'launch')

    # Create the launch configuration variables
    # namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    # autostart = LaunchConfiguration('autostart')

    # lifecycle_nodes = [
    #     'map_server',
    #     'amcl',
    #     'controller_server',
    #     'planner_server',
    #     'behavior_server',
    #     'bt_navigator',
    #     'waypoint_follower']

    # declare_namespace = DeclareLaunchArgument(
    #     'namespace', default_value='',
    #     description='Top-level namespace')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false',
        description='Use simulation (Gazebo) clock if true')

    # declare_autostart = DeclareLaunchArgument(
    #     'autostart', default_value='true',
    #     description='Automatically startup the nav2 stack')

    robot_localization_node = Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(get_package_share_directory('limo_navigation'), 'params/ekf.yaml'), {'use_sim_time': use_sim_time}]
    )

    # start_lifecycle_mgr = Node(
    #     package='nav2_lifecycle_manager',
    #     executable='lifecycle_manager',
    #     name='lifecycle_manager_navigation',
    #     output='screen',
    #     parameters=[{'use_sim_time': use_sim_time},
    #                 {'autostart': autostart},
                    # {'node_names': lifecycle_nodes}])

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_use_sim_time)
    # ld.add_action(declare_autostart)
    # ld.add_action(declare_namespace)

    # ld.add_action(launch_limo_localization)
    ld.add_action(robot_localization_node)

    # ld.add_action(start_lifecycle_mgr)

    return ld