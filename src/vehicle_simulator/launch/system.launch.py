import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression, PathJoinSubstitution

def generate_launch_description():
    world_name = LaunchConfiguration('world_name')
    sensorOffsetX = LaunchConfiguration('sensorOffsetX')
    sensorOffsetY = LaunchConfiguration('sensorOffsetY')
    vehicleHeight = LaunchConfiguration('vehicleHeight')
    cameraOffsetZ = LaunchConfiguration('cameraOffsetZ')
    vehicleX = LaunchConfiguration('vehicleX')
    vehicleY = LaunchConfiguration('vehicleY')
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
    vis_tools = LaunchConfiguration('vis_tools')
    gazebo_gui = LaunchConfiguration('gazebo_gui')
    checkTerrainConn = LaunchConfiguration('checkTerrainConn')
    namespace = LaunchConfiguration('namespace')

    declare_world_name = DeclareLaunchArgument('world_name', default_value='indoor', description='')
    declare_sensorOffsetX = DeclareLaunchArgument('sensorOffsetX', default_value='0.0', description='')
    declare_sensorOffsetY = DeclareLaunchArgument('sensorOffsetY', default_value='0.0', description='')
    declare_vehicleHeight = DeclareLaunchArgument('vehicleHeight', default_value='0.75', description='')
    declare_cameraOffsetZ = DeclareLaunchArgument('cameraOffsetZ', default_value='0.0', description='')
    declare_vehicleX = DeclareLaunchArgument('vehicleX', default_value='0.0', description='')
    declare_vehicleY = DeclareLaunchArgument('vehicleY', default_value='0.0', description='')
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
    declare_vis_tools = DeclareLaunchArgument('vis_tools', default_value='true', description='')
    declare_gazebo_gui = DeclareLaunchArgument('gazebo_gui', default_value='false', description='')
    declare_checkTerrainConn = DeclareLaunchArgument('checkTerrainConn', default_value='false', description='')
    declare_namespace = DeclareLaunchArgument('namespace', default_value='robot_X', description='')

    start_local_planner = IncludeLaunchDescription(
      FrontendLaunchDescriptionSource(os.path.join(
        get_package_share_directory('local_planner'), 'launch', 'local_planner.launch')
      ),
      launch_arguments={
        'cameraOffsetZ': cameraOffsetZ,
        'goalX': vehicleX,
        'goalY': vehicleY,
        'namespace': namespace,
      }.items()
    )

    start_terrain_analysis = IncludeLaunchDescription(
      FrontendLaunchDescriptionSource(os.path.join(
        get_package_share_directory('terrain_analysis'), 'launch', 'terrain_analysis.launch')
      ),
      launch_arguments = {
        'namespace': namespace,
      }.items()
    )

    start_terrain_analysis_ext = IncludeLaunchDescription(
      FrontendLaunchDescriptionSource(os.path.join(
        get_package_share_directory('terrain_analysis_ext'), 'launch', 'terrain_analysis_ext.launch')
      ),
      launch_arguments={
        'checkTerrainConn': checkTerrainConn,
        'namespace': namespace,
      }.items()
    )
    
    start_vehicle_simulator = IncludeLaunchDescription(
      PythonLaunchDescriptionSource(os.path.join(
        get_package_share_directory('vehicle_simulator'), 'launch', 'vehicle_simulator.launch.py')
      ),
      launch_arguments={
        'world_name': world_name,
        'sensorOffsetX': sensorOffsetX,
        'sensorOffsetY': sensorOffsetY,
        'vehicleHeight': vehicleHeight,
        'cameraOffsetZ': cameraOffsetZ,
        'vehicleX': vehicleX,
        'vehicleY': vehicleY,
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
        'gui': gazebo_gui,
        'namespace': namespace,
      }.items()
    )

    start_sensor_scan_generation = IncludeLaunchDescription(
      FrontendLaunchDescriptionSource(os.path.join(
        get_package_share_directory('sensor_scan_generation'), 'launch', 'sensor_scan_generation.launch')
      ),
      launch_arguments={
        'namespace': namespace,
      }.items()
    )

    start_visualization_tools = IncludeLaunchDescription(
      FrontendLaunchDescriptionSource(os.path.join(
        get_package_share_directory('visualization_tools'), 'launch', 'visualization_tools.launch')
      ),
      launch_arguments={
        'world_name': world_name,
        'namespace': namespace,
      }.items(),
      condition=IfCondition(vis_tools)
    )

    start_joy = Node(
      package='joy', 
      executable='joy_node',
      name='ps3_joy',
      output='screen',
      parameters=[{
                  'dev': "/dev/input/js0",
                  'deadzone': 0.12,
                  'autorepeat_rate': 0.0,
                  'namespace': namespace,
        }]
    )

    ld = LaunchDescription()

    # Add the actions
    ld.add_action(declare_world_name)
    ld.add_action(declare_sensorOffsetX)
    ld.add_action(declare_sensorOffsetY)
    ld.add_action(declare_vehicleHeight)
    ld.add_action(declare_cameraOffsetZ)
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
    ld.add_action(declare_vis_tools)
    ld.add_action(declare_gazebo_gui)
    ld.add_action(declare_checkTerrainConn)
    ld.add_action(declare_namespace)

    ld.add_action(start_local_planner)
    ld.add_action(start_terrain_analysis)
    ld.add_action(start_terrain_analysis_ext)
    ld.add_action(start_vehicle_simulator)
    ld.add_action(start_sensor_scan_generation)
    ld.add_action(start_visualization_tools)
    ld.add_action(start_joy)

    return ld