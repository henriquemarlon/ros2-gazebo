import rclpy
import 
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
from math import atan2

    
class Turtle_Controller(Node):
    def __init__(self, queue):
        super().__init__("turtlebot")
        #Variáveis necessárias movimentação
        self.coordinates = {"x": 0.0, "y": 0.0, "theta": 0.0}
        self.position_goal = {"x": 0.0, "y": 0.0, "theta": 0.0}
        self.queue = queue
        
        #Criação do publisher
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.02, self.publish_movement)
        
        #Criação do subscriber
        self.subscription = self.create_subscription(Odometry, '/odom', self.callback, 10)
        
    def callback(self, msg):
        # Converte de quaternario para euler
        orientation = msg.pose.pose.orientation
        _, _, orientation = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])

        self.coordinates = {
                "x": msg.pose.pose.position.x,
                "y": msg.pose.pose.position.y,
                "z": msg.pose.pose.position.z,
                "theta": orientation 
            } 
        self.get_logger().info(str(self.coordinates))
        return self.coordinates
        
    def publish_movement(self):
        speed = Twist()
        
        #Atribui a posição de destino o primeiro item da fila
        try:
            self.position_goal = self.queue[0]
        
            #Calcula o arcontangente em que o robô deve rotacionar
            goal_x = self.position_goal["x"]
            goal_y = self.position_goal["y"]

            delta_x = goal_x - self.coordinates["x"] 
            delta_y = goal_y - self.coordinates["y"]

            atan_result = atan2(delta_y, delta_x)
            
            #Condição de que suas posições atuais forem menor que 0.1 o primeiro item da fila é removido
            if abs(self.coordinates["x"] - self.position_goal["x"]) < 0.1 and abs(self.coordinates["y"] - self.position_goal["y"]) < 0.1:
                self.queue.dequeue()
            
            # Rotaciona o robô de acordo com sua posição atual e posição que deseja ir
            if abs(atan_result - self.coordinates["theta"]) > 0.1:
                speed.linear.x = 0.0
                if (atan_result - self.coordinates["theta"]) > 0.0:
                    speed.angular.z = 0.3
                else:
                    speed.angular.z = -0.3
                self.publisher.publish(speed)
                
            
            # Robô anda se já estiver na direção do ponto que deseja chegar
            else: 
                speed.linear.x = 0.5
                speed.angular.z = 0.0
                self.publisher.publish(speed)
                
        except IndexError:
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            self.publisher.publish(speed)
            self.get_logger().info("Fim da jornada")
            exit()
            

def main(args=None):
    rclpy.init(args=args)
    queue = Queue()
    subscriebr_node = Turtle_Controller(queue)
    rclpy.spin(subscriebr_node)
    subscriebr_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()