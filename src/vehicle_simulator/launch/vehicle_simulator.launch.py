import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch.utilities import perform_substitutions
import tempfile
import subprocess

def spawn_entities(context, *args, **kwargs):
    namespace = LaunchConfiguration('namespace')
    ns = namespace.perform(context)
    vehicleX = LaunchConfiguration('vehicleX')
    x = vehicleX.perform(context)

    lidar_xacro = os.path.join(get_package_share_directory('vehicle_simulator'), 'urdf', 'lidar.urdf.xacro') 
    # lidar_urdf = Command(['xacro',' ', lidar_xacro])

    urdf_xml = subprocess.check_output(['xacro', lidar_xacro]).decode()

    print(f"Launching spawn_entities with namespace: {ns}")
    print(f"value with namespace: {x}")

    tmp_urdf = tempfile.NamedTemporaryFile(delete=False, suffix='.urdf')
    tmp_urdf.write(urdf_xml.encode())
    tmp_urdf.close()

    spawn_lidar = Node(
      package='gazebo_ros',
      executable='spawn_entity.py',
      arguments=[
          '-entity', f'{ns}/lidar', 
          '-file', tmp_urdf.name,
          '-robot_namespace', ns
      ],
      output='screen'
    )

    robot_xacro = os.path.join(get_package_share_directory('vehicle_simulator'), 'urdf', 'robot.sdf')
    spawn_robot = Node(
      package='gazebo_ros', 
      executable='spawn_entity.py',
      arguments=[
        '-file', robot_xacro,
        '-entity', f'{ns}/robot',
        '-robot_namespace', ns
      ],
      output='screen',
    )

    camera_xacro = os.path.join(get_package_share_directory('vehicle_simulator'), 'urdf', 'camera.urdf.xacro')
    spawn_camera = Node(
      package='gazebo_ros', 
      executable='spawn_entity.py',
      arguments=[
        '-file', camera_xacro,
        '-entity', f'{ns}/camera',
        '-robot_namespace', ns
        ],
      output='screen'
    )

    return [spawn_lidar, spawn_robot, spawn_camera]

def launch_vehicle_simulator(context, *args, **kwargs):
    ns = ''.join(perform_substitutions(context, [LaunchConfiguration('namespace')]))

    print(f"Launching vehicle_simulator with namespace: {ns}")

    start_vehicle_simulator = Node(
      package='vehicle_simulator', 
      executable='vehicleSimulator',
      parameters=[
        {
          'use_gazebo_time': False,
          'sensorOffsetX': float(LaunchConfiguration('sensorOffsetX').perform(context)),
          'sensorOffsetY': float(LaunchConfiguration('sensorOffsetY').perform(context)),
          'vehicleHeight': float(LaunchConfiguration('vehicleHeight').perform(context)),
          'cameraOffsetZ': float(LaunchConfiguration('cameraOffsetZ').perform(context)),
          'vehicleX': float(LaunchConfiguration('vehicleX').perform(context)),
          'vehicleY': float(LaunchConfiguration('vehicleY').perform(context)),
          'vehicleZ': float(LaunchConfiguration('vehicleZ').perform(context)),
          'terrainZ': float(LaunchConfiguration('terrainZ').perform(context)),
          'vehicleYaw': float(LaunchConfiguration('vehicleYaw').perform(context)),
          'terrainVoxelSize': float(LaunchConfiguration('terrainVoxelSize').perform(context)),
          'groundHeightThre': float(LaunchConfiguration('groundHeightThre').perform(context)),
          'adjustZ': LaunchConfiguration('adjustZ').perform(context) == 'true',
          'terrainRadiusZ': float(LaunchConfiguration('terrainRadiusZ').perform(context)),
          'minTerrainPointNumZ': int(LaunchConfiguration('minTerrainPointNumZ').perform(context)),
          'smoothRateZ': float(LaunchConfiguration('smoothRateZ').perform(context)),
          'adjustIncl': LaunchConfiguration('adjustIncl').perform(context) == 'true',
          'terrainRadiusIncl': float(LaunchConfiguration('terrainRadiusIncl').perform(context)),
          'minTerrainPointNumIncl': int(LaunchConfiguration('minTerrainPointNumIncl').perform(context)),
          'smoothRateIncl': float(LaunchConfiguration('smoothRateIncl').perform(context)),
          'InclFittingThre': float(LaunchConfiguration('InclFittingThre').perform(context)),
          'maxIncl': float(LaunchConfiguration('maxIncl').perform(context)),
          'use_sim_time': LaunchConfiguration('use_sim_time').perform(context) == 'true',
          'namespace': ns
        }
        ],
        output='screen'
    )

    return [start_vehicle_simulator]

def generate_launch_description():
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
    world_name = LaunchConfiguration('world_name')
    namespace = LaunchConfiguration('namespace')

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
    declare_world_name = DeclareLaunchArgument('world_name', default_value='garage', description='')
    declare_namespace = DeclareLaunchArgument('namespace', default_value='robot_X', description='')

    start_spawn = OpaqueFunction(function=spawn_entities)
    

    # start_vehicle_simulator = Node(
    #   package='vehicle_simulator', 
    #   executable='vehicleSimulator',
    #   namespace=namespace,
    #   parameters=[
    #     {
    #       'use_gazebo_time': False,
    #       'sensorOffsetX': sensorOffsetX,
    #       'sensorOffsetY': sensorOffsetY,
    #       'vehicleHeight': vehicleHeight,
    #       'cameraOffsetZ': cameraOffsetZ,
    #       'vehicleX': vehicleX,
    #       'vehicleY': vehicleY,
    #       'vehicleZ': vehicleZ,
    #       'terrainZ': terrainZ,
    #       'vehicleYaw': vehicleYaw,
    #       'terrainVoxelSize': terrainVoxelSize,
    #       'groundHeightThre': groundHeightThre,
    #       'adjustZ': adjustZ,
    #       'terrainRadiusZ': terrainRadiusZ,
    #       'minTerrainPointNumZ': minTerrainPointNumZ,
    #       'smoothRateZ': smoothRateZ,
    #       'adjustIncl': adjustIncl,
    #       'terrainRadiusIncl': terrainRadiusIncl,
    #       'minTerrainPointNumIncl': minTerrainPointNumIncl,
    #       'smoothRateIncl': smoothRateIncl,
    #       'InclFittingThre': InclFittingThre,
    #       'maxIncl': maxIncl,
    #       'use_sim_time': use_sim_time,
    #       'robot_ns': namespace
    #     }
    #     ],
    #     output='screen'
    # )

    # delayed_start_vehicle_simulator = TimerAction(
    #   period=5.0,
    #   actions=[
    #     start_vehicle_simulator
    #   ]
    # )

    start_vehicle_simulator = OpaqueFunction(function=launch_vehicle_simulator)

    # delayed_start_vehicle_simulator = TimerAction(
    #   period=5.0,
    #   actions=[
    #     start_vehicle_simulator
    #   ]
    # )

    ld = LaunchDescription()

    # Add the actions
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
    ld.add_action(declare_world_name)
    ld.add_action(declare_namespace)

    ld.add_action(start_spawn)
    # ld.add_action(delayed_start_vehicle_simulator)
    ld.add_action(start_vehicle_simulator)

    return ld
