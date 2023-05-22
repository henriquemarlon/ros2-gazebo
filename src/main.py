import rclpy
from modules import Controller, Queue, Stack


def main(args=None):
    rclpy.init(args=args)
    queue = Queue()
    stack = Stack()
    subscriber_node = Controller(queue, stack)
    rclpy.spin(subscriber_node)
    subscriber_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
