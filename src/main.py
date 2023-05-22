import rclpy
from modules import Controller, Queue


def main(args=None):
    rclpy.init(args=args)
    queue = Queue()
    subscriber_node = Controller(queue)
    rclpy.spin(subscriber_node)
    subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()