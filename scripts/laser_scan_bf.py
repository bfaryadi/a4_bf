#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import Header
from builtin_interfaces.msg import Duration
from rclpy.qos import qos_profile_sensor_data

class LaserScanToMarker(Node):
    def __init__(self):
        super().__init__('laser_scan_bf')
        self.publisher = self.create_publisher(Marker, '/visualization_marker', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, qos_profile_sensor_data)

    def listener_callback(self, msg):
        points = [Point() for i in range(len(msg.ranges))]
        for i in range(len(msg.ranges)):
            L = msg.ranges[i]
            if(not math.isinf(L)):
                theta = msg.angle_min + i*msg.angle_increment
                points[i] = Point(x=L*math.cos(theta),y=L*math.sin(theta),z=0.0)
        marker = self.get_marker_with_points(points)
        print(f'Publishing message: {marker}')
        self.publisher.publish(marker)
    
    def get_marker_with_points(self, points: list):
        ''' Creates a visualization_msgs/Marker from a list of points
        Input:
        points: A list of geometry_msgs/Point objects
        Return:
        marker: a visualization_msgs/Marker object that can be published to Rviz
        on topic 'visualization_marker'
        '''
        # -- initialize marker
        marker = Marker()
        # -- fill message header
        marker.header = Header()
        marker.header.frame_id = 'laser_link'
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = ''
        marker.id = 0 # Id of marker will always be 0
        marker.type = Marker.POINTS # Points
        marker.action = Marker.ADD # Add
        # Set size
        marker.scale.x = 0.02
        marker.scale.y = 0.02
        marker.scale.z = 0.02
        # Set color
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0
        # Append the points to the points array
        marker.points = points
        # Show for 2 seconds
        marker.lifetime = Duration(sec=2)
        return marker

def main(args=None):
    rclpy.init(args=args)
    node = LaserScanToMarker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()