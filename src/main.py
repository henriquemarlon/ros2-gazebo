import rclpy
from modules import Controller, Queue, Stack


def main(args=None):
    rclpy.init(args=args)
    queue = Queue()
    subscriebr_node = Controller(queue)
    rclpy.spin(subscriebr_node)
    subscriebr_node.destroy_node()
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()