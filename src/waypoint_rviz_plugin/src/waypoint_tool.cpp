#include <waypoint_tool.hpp>

#include <string>

#include <rviz_common/display_context.hpp>
#include <rviz_common/logging.hpp>
#include <rviz_common/properties/string_property.hpp>
#include <rviz_common/properties/qos_profile_property.hpp>

#include <unistd.h>

namespace waypoint_rviz_plugin
{
WaypointTool::WaypointTool()
: rviz_default_plugins::tools::PoseTool(), qos_profile_(5)
{
  shortcut_key_ = 'w';

  topic_property_ = new rviz_common::properties::StringProperty("Topic", "waypoint", "The topic on which to publish navigation waypionts.",
                                       getPropertyContainer(), SLOT(updateTopic()), this);
  
  qos_profile_property_ = new rviz_common::properties::QosProfileProperty(topic_property_, qos_profile_);

  robot_ns_property_ = new rviz_common::properties::StringProperty("Robot Namespace", "", "Namespace prefix for multi-robot, e.g. robot_0",
                                getPropertyContainer(), SLOT(updateTopic()), this);
}

WaypointTool::~WaypointTool() = default;

void WaypointTool::onInitialize()
{
  rviz_default_plugins::tools::PoseTool::onInitialize();
  qos_profile_property_->initialize(
    [this](rclcpp::QoS profile) {this->qos_profile_ = profile;});
  setName("Waypoint");
  updateTopic();
  vehicle_z = 0;
}

void WaypointTool::updateTopic()
{
  rclcpp::Node::SharedPtr raw_node =
    context_->getRosNodeAbstraction().lock()->get_raw_node();
  
  // close old three topics
  pub_.reset();
  sub_.reset();
  pub_joy_.reset();

  std::string ns_prefix = robot_ns_property_->getStdString();
  if (!ns_prefix.empty() && ns_prefix.front() == '/') ns_prefix.erase(0, 1);
  if (!ns_prefix.empty()) ns_prefix += "/";

  // sub_ = raw_node->template create_subscription<nav_msgs::msg::Odometry>("state_estimation", 5 ,std::bind(&WaypointTool::odomHandler,this,std::placeholders::_1));
  
  // pub_ = raw_node->template create_publisher<geometry_msgs::msg::PointStamped>("way_point", qos_profile_);
  // pub_joy_ = raw_node->template create_publisher<sensor_msgs::msg::Joy>("joy", qos_profile_);
  sub_ = raw_node->create_subscription<nav_msgs::msg::Odometry>(
           "/" + ns_prefix + "state_estimation", 5,
           std::bind(&WaypointTool::odomHandler, this, std::placeholders::_1));

  pub_ = raw_node->create_publisher<geometry_msgs::msg::PointStamped>("/" + ns_prefix + "way_point", qos_profile_);

  pub_joy_ = raw_node->create_publisher<sensor_msgs::msg::Joy>("/" + ns_prefix + "joy", qos_profile_);

  clock_ = raw_node->get_clock();
}

void WaypointTool::odomHandler(const nav_msgs::msg::Odometry::ConstSharedPtr odom)
{
  vehicle_z = odom->pose.pose.position.z;
}

void WaypointTool::onPoseSet(double x, double y, double theta)
{
  if (!pub_ || !pub_joy_) return;

  /* 读取 namespace 前缀（与 updateTopic 保持一致） */
  // std::string ns_prefix = robot_ns_property_->getStdString();
  // if (!ns_prefix.empty() && ns_prefix.front() == '/') ns_prefix.erase(0, 1);
  // if (!ns_prefix.empty()) ns_prefix += "/";

  sensor_msgs::msg::Joy joy;

  joy.axes.push_back(0);
  joy.axes.push_back(0);
  joy.axes.push_back(-1.0);
  joy.axes.push_back(0);
  joy.axes.push_back(1.0);
  joy.axes.push_back(1.0);
  joy.axes.push_back(0);
  joy.axes.push_back(0);

  joy.buttons.push_back(0);
  joy.buttons.push_back(0);
  joy.buttons.push_back(0);
  joy.buttons.push_back(0);
  joy.buttons.push_back(0);
  joy.buttons.push_back(0);
  joy.buttons.push_back(0);
  joy.buttons.push_back(1);
  joy.buttons.push_back(0);
  joy.buttons.push_back(0);
  joy.buttons.push_back(0);

  joy.header.stamp = clock_->now();
  // joy.header.frame_id = ns_prefix.empty() ? "waypoint_tool" : (ns_prefix + "waypoint_tool");
  joy.header.frame_id = "waypoint_tool";
  pub_joy_->publish(joy);

  geometry_msgs::msg::PointStamped waypoint;
  // waypoint.header.frame_id = ns_prefix.empty() ? "map" : (ns_prefix + "map");
  waypoint.header.frame_id = "map";
  waypoint.header.stamp = joy.header.stamp;
  waypoint.point.x = x;
  waypoint.point.y = y;
  waypoint.point.z = vehicle_z;

  pub_->publish(waypoint);
  usleep(10000);
  pub_->publish(waypoint);
}
}

#include <pluginlib/class_list_macros.hpp> 
PLUGINLIB_EXPORT_CLASS(waypoint_rviz_plugin::WaypointTool, rviz_common::Tool)
