from math import atan2
from rclpy.node import Node
from modules import Stack as stack
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf_transformations import euler_from_quaternion


class Controller(Node):
    def __init__(self, queue, stack):
        super().__init__("papy")
        self.positions = {}
        self.goal = {}
        self.queue = queue
        self.stack = stack

        self.subscription = self.create_subscription(
            Odometry, '/odom', self.callback, 10)

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.02, self.publish_movement)

    def callback(self, msg):
        orientation = msg.pose.pose.orientation
        _, _, orientation = euler_from_quaternion(
            [orientation.x, orientation.y, orientation.z, orientation.w])

        self.positions = {
            "x": msg.pose.pose.position.x,
            "y": msg.pose.pose.position.y,
            "z": msg.pose.pose.position.z,
            "theta": orientation
        }
        self.get_logger().info(str(self.positions))
        return self.positions

    def return_movement(self):

        try:

            velocity = Twist()

            self.goal = self.stack[0]

            diff_x = self.goal["x"] - self.positions["x"]
            diff_y = self.goal["y"] - self.positions["y"]

            atan = atan2(diff_y, diff_x)

            if abs(self.positions["x"] - self.goal["x"]) < 0.1 and abs(self.positions["y"] - self.goal["y"]) < 0.1:
                self.stack.unstack()

            if abs(atan - self.positions["theta"]) > 0.1:
                velocity.linear.x = 0.0
                velocity.angular.z = 0.3 if (atan - self.positions["theta"]) > 0.0 else -0.3

            else:
                velocity.linear.x = 0.5
                velocity.angular.z = 0.0
                self.publisher.publish(velocity)

            self.publisher.publish(velocity)


        except IndexError:
            velocity.linear.x = 0.0
            velocity.angular.z = 0.0
            self.publisher.publish(velocity)
            self.get_logger().info("Fim da jornada")
            exit()

    def publish_movement(self):

        try:
            velocity = Twist()

            self.goal = self.queue[0]

            diff_x = self.goal["x"] - self.positions["x"]
            diff_y = self.goal["y"] - self.positions["y"]

            atan = atan2(diff_y, diff_x)

            if abs(self.positions["x"] - self.goal["x"]) < 0.1 and abs(self.positions["y"] - self.goal["y"]) < 0.1:
                dequeue = self.queue.dequeue()
                self.stack.stackup(dequeue)

            if abs(atan - self.positions["theta"]) > 0.1:
                velocity.linear.x = 0.0
                velocity.angular.z = 0.3 if (atan - self.positions["theta"]) > 0.0 else -0.3
                
            else:
                velocity.linear.x = 0.5
                velocity.angular.z = 0.0
                self.publisher.publish(velocity)

            self.publisher.publish(velocity)


        except IndexError:
            self.return_movement()
