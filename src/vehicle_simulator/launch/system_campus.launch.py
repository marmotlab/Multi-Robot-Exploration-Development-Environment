import os
import yaml 

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction, TimerAction, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from launch_ros.actions import Node, PushRosNamespace
from launch.substitutions import LaunchConfiguration, TextSubstitution 

def declare_world_action(context, world_name):
    world_name_str = str(world_name.perform(context))
    declare_world = DeclareLaunchArgument('world', default_value=[os.path.join(get_package_share_directory('vehicle_simulator'), 'world', world_name_str + '.world')], description='')
    return [declare_world]

def generate_robot_groups(context, *args, ** kwargs):
    n = int(LaunchConfiguration('n_robots').perform(context))
    world_name = LaunchConfiguration('world_name').perform(context)
    checkTerrainConn = LaunchConfiguration('checkTerrainConn').perform(context)
    vis_tools = LaunchConfiguration('vis_tools').perform(context)
    sensorOffsetX = LaunchConfiguration('sensorOffsetX').perform(context)
    sensorOffsetY = LaunchConfiguration('sensorOffsetY').perform(context)
    vehicleHeight = LaunchConfiguration('vehicleHeight').perform(context)
    cameraOffsetZ = LaunchConfiguration('cameraOffsetZ').perform(context)
    vehicleX_list = LaunchConfiguration('vehicleX_list').perform(context)
    vehicleY_list = LaunchConfiguration('vehicleY_list').perform(context)
    vehicleZ = LaunchConfiguration('vehicleZ').perform(context)
    terrainZ = LaunchConfiguration('terrainZ').perform(context)
    vehicleYaw = LaunchConfiguration('vehicleYaw').perform(context)
    terrainVoxelSize = LaunchConfiguration('terrainVoxelSize').perform(context)
    groundHeightThre = LaunchConfiguration('groundHeightThre').perform(context)
    adjustZ = LaunchConfiguration('adjustZ').perform(context)
    terrainRadiusZ = LaunchConfiguration('terrainRadiusZ').perform(context)
    minTerrainPointNumZ = LaunchConfiguration('minTerrainPointNumZ').perform(context)
    smoothRateZ = LaunchConfiguration('smoothRateZ').perform(context)
    adjustIncl = LaunchConfiguration('adjustIncl').perform(context)
    terrainRadiusIncl = LaunchConfiguration('terrainRadiusIncl').perform(context)
    minTerrainPointNumIncl = LaunchConfiguration('minTerrainPointNumIncl').perform(context)
    smoothRateIncl = LaunchConfiguration('smoothRateIncl').perform(context)
    InclFittingThre = LaunchConfiguration('InclFittingThre').perform(context)
    maxIncl = LaunchConfiguration('maxIncl').perform(context)
    use_sim_time = LaunchConfiguration('use_sim_time').perform(context)
    gazebo_gui = LaunchConfiguration('gazebo_gui').perform(context)

    vehicleX_vals = yaml.safe_load(vehicleX_list)
    vehicleY_vals = yaml.safe_load(vehicleY_list)

    if not isinstance(vehicleX_vals, list):
        vehicleX_vals = [vehicleX_vals]
    if not isinstance(vehicleY_vals, list):
        vehicleY_vals = [vehicleY_vals]

    robot_groups = []
    for i in range(n):
        ns = f'robot_{i}'

        vehicleX = vehicleX_vals[i]
        vehicleY = vehicleY_vals[i]

        include_system = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory('vehicle_simulator'), 'launch', 'system.launch.py')
        ),
        launch_arguments={'checkTerrainConn': checkTerrainConn,
                        'vis_tools': vis_tools,
                        'world_name': world_name,
                        'namespace': TextSubstitution(text=str(ns)), # ns,
                        'sensorOffsetX': sensorOffsetX,
                        'sensorOffsetY': sensorOffsetY,
                        'vehicleHeight': vehicleHeight,
                        'cameraOffsetZ': cameraOffsetZ,
                        'vehicleX'  : TextSubstitution(text=str(vehicleX)),
                        'vehicleY'  : TextSubstitution(text=str(vehicleY)),
                        'vehicleZ': vehicleZ,
                        'terrainZ': terrainZ,
                        'vehicleYaw': vehicleYaw,
                        'terrainVoxelSize': terrainVoxelSize,
                        'groundHeightThre': groundHeightThre,
                        'adjustZ': adjustZ,
                        'terrainRadiusZ': terrainRadiusZ,
                        'minTerrainPointNumZ': minTerrainPointNumZ,
                        'smoothRateZ': smoothRateZ,
                        'adjustIncl': adjustIncl,
                        'terrainRadiusIncl': terrainRadiusIncl,
                        'minTerrainPointNumIncl': minTerrainPointNumIncl,
                        'smoothRateIncl': smoothRateIncl,
                        'InclFittingThre': InclFittingThre,
                        'maxIncl': maxIncl,
                        'use_sim_time': use_sim_time,
                        'gazebo_gui': gazebo_gui,
            }.items()
        )
        group = GroupAction([PushRosNamespace(ns), include_system])
        robot_groups.append(group)
    return robot_groups

def generate_launch_description():
    world_name = LaunchConfiguration('world_name')
    sensorOffsetX = LaunchConfiguration('sensorOffsetX')
    sensorOffsetY = LaunchConfiguration('sensorOffsetY')
    vehicleHeight = LaunchConfiguration('vehicleHeight')
    cameraOffsetZ = LaunchConfiguration('cameraOffsetZ')
    vehicleX_list = LaunchConfiguration('vehicleX_list')
    vehicleY_list = LaunchConfiguration('vehicleY_list')
    vehicleZ = LaunchConfiguration('vehicleZ')
    terrainZ = LaunchConfiguration('terrainZ')
    vehicleYaw = LaunchConfiguration('vehicleYaw')
    terrainVoxelSize = LaunchConfiguration('terrainVoxelSize')
    groundHeightThre = LaunchConfiguration('groundHeightThre')
    adjustZ = LaunchConfiguration('adjustZ')
    terrainRadiusZ = LaunchConfiguration('terrainRadiusZ')
    minTerrainPointNumZ = LaunchConfiguration('minTerrainPointNumZ')
    smoothRateZ = LaunchConfiguration('smoothRateZ')
    adjustIncl = LaunchConfiguration('adjustIncl')
    terrainRadiusIncl = LaunchConfiguration('terrainRadiusIncl')
    minTerrainPointNumIncl = LaunchConfiguration('minTerrainPointNumIncl')
    smoothRateIncl = LaunchConfiguration('smoothRateIncl')
    InclFittingThre = LaunchConfiguration('InclFittingThre')
    maxIncl = LaunchConfiguration('maxIncl')
    use_sim_time = LaunchConfiguration('use_sim_time')
    gazebo_gui = LaunchConfiguration('gazebo_gui')
    checkTerrainConn = LaunchConfiguration('checkTerrainConn')
    verbose = LaunchConfiguration('verbose')
    vis_tools = LaunchConfiguration('vis_tools')
    namespace = LaunchConfiguration('namespace')
    n_robots = LaunchConfiguration('n_robots')

    declare_world_name = DeclareLaunchArgument('world_name', default_value='indoor', description='')
    declare_sensorOffsetX = DeclareLaunchArgument('sensorOffsetX', default_value='0.0', description='')
    declare_sensorOffsetY = DeclareLaunchArgument('sensorOffsetY', default_value='0.0', description='')
    declare_vehicleHeight = DeclareLaunchArgument('vehicleHeight', default_value='0.75', description='')
    declare_cameraOffsetZ = DeclareLaunchArgument('cameraOffsetZ', default_value='0.0', description='')
    declare_vehicleX_list = DeclareLaunchArgument('vehicleX_list', default_value='[0.0]', description='')
    declare_vehicleY_list = DeclareLaunchArgument('vehicleY_list', default_value='[0.0]', description='')
    declare_vehicleX = DeclareLaunchArgument('vehicleX', default_value='0.0', description='X position for one robot (will be overridden)')
    declare_vehicleY = DeclareLaunchArgument('vehicleY', default_value='0.0',description='Y position for one robot (will be overridden)')
    declare_vehicleZ = DeclareLaunchArgument('vehicleZ', default_value='0.0', description='')
    declare_terrainZ = DeclareLaunchArgument('terrainZ', default_value='0.0', description='')
    declare_vehicleYaw = DeclareLaunchArgument('vehicleYaw', default_value='0.0', description='')
    declare_terrainVoxelSize = DeclareLaunchArgument('terrainVoxelSize', default_value='0.05', description='')
    declare_groundHeightThre = DeclareLaunchArgument('groundHeightThre', default_value='0.1', description='')
    declare_adjustZ = DeclareLaunchArgument('adjustZ', default_value='true', description='')
    declare_terrainRadiusZ = DeclareLaunchArgument('terrainRadiusZ', default_value='1.0', description='')
    declare_minTerrainPointNumZ = DeclareLaunchArgument('minTerrainPointNumZ', default_value='5', description='')
    declare_smoothRateZ = DeclareLaunchArgument('smoothRateZ', default_value='0.5', description='')
    declare_adjustIncl = DeclareLaunchArgument('adjustIncl', default_value='true', description='')
    declare_terrainRadiusIncl = DeclareLaunchArgument('terrainRadiusIncl', default_value='2.0', description='')
    declare_minTerrainPointNumIncl = DeclareLaunchArgument('minTerrainPointNumIncl', default_value='200', description='')
    declare_smoothRateIncl = DeclareLaunchArgument('smoothRateIncl', default_value='0.5', description='')
    declare_InclFittingThre = DeclareLaunchArgument('InclFittingThre', default_value='0.2', description='')
    declare_maxIncl = DeclareLaunchArgument('maxIncl', default_value='30.0', description='')
    declare_use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='false', description='')
    declare_gazebo_gui = DeclareLaunchArgument('gazebo_gui', default_value='false', description='')
    declare_checkTerrainConn = DeclareLaunchArgument('checkTerrainConn', default_value='false', description='')
    declare_verbose = DeclareLaunchArgument('verbose', default_value='true', description='')
    declare_vis_tools = DeclareLaunchArgument('vis_tools', default_value='true', description='')
    declare_namespace = DeclareLaunchArgument('namespace', default_value='robot_X')
    declare_n_robots = DeclareLaunchArgument('n_robots', default_value='1')

    world = LaunchConfiguration('world')

    start_gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')),
        launch_arguments={'world': world,
                        'gui': gazebo_gui,
                        'verbose': verbose
    }.items()
    )

    start_robot_systems = OpaqueFunction(function=generate_robot_groups)

    rviz_config_file = os.path.join(get_package_share_directory('vehicle_simulator'), 'rviz', 'vehicle_simulator.rviz')
    start_rviz = Node(
    package='rviz2',
    executable='rviz2',
    arguments=['-d', rviz_config_file],
    output='screen'
    )

    delayed_start_rviz = TimerAction(
    period=8.0,
    actions=[
        start_rviz
    ]
    ) 

    ld = LaunchDescription()

    # Add the actions
    ld.add_action(declare_world_name)
    ld.add_action(declare_gazebo_gui)
    ld.add_action(declare_checkTerrainConn)
    ld.add_action(declare_verbose)
    ld.add_action(declare_vis_tools)
    ld.add_action(declare_namespace)
    ld.add_action(declare_n_robots)
    ld.add_action(declare_sensorOffsetX)
    ld.add_action(declare_sensorOffsetY)
    ld.add_action(declare_vehicleHeight)
    ld.add_action(declare_cameraOffsetZ)
    ld.add_action(declare_vehicleX_list)
    ld.add_action(declare_vehicleY_list)
    ld.add_action(declare_vehicleX)
    ld.add_action(declare_vehicleY)
    ld.add_action(declare_vehicleZ)
    ld.add_action(declare_terrainZ)
    ld.add_action(declare_vehicleYaw)
    ld.add_action(declare_terrainVoxelSize)
    ld.add_action(declare_groundHeightThre)
    ld.add_action(declare_adjustZ)
    ld.add_action(declare_terrainRadiusZ)
    ld.add_action(declare_minTerrainPointNumZ)
    ld.add_action(declare_smoothRateZ)
    ld.add_action(declare_adjustIncl)
    ld.add_action(declare_terrainRadiusIncl)
    ld.add_action(declare_minTerrainPointNumIncl)
    ld.add_action(declare_smoothRateIncl)
    ld.add_action(declare_InclFittingThre)
    ld.add_action(declare_maxIncl)
    ld.add_action(declare_use_sim_time)
    ld.add_action(OpaqueFunction(function=declare_world_action, args=[world_name]))

    ld.add_action(start_gazebo)
    ld.add_action(start_robot_systems)
    ld.add_action(delayed_start_rviz)

    return ld
