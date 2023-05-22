import csv
from collections import deque


class Queue(deque):
    def __init__(self, csv_pontos="./utils/cordinates_theta.csv"):
        super().__init__()
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        with open(csv_pontos) as csv_pontos:
            csv_pontos = csv.reader(csv_pontos, delimiter=',')
            for row in csv_pontos:
                self.x, self.y, self.theta = [float(x) for x in row]
                new_position = {"x": self.x, "y": self.y, "theta": self.theta}
                self.enqueue(new_position)
        
    def enqueue(self, x):
        super().append(x)
        
    def dequeue(self):
        return super().popleft()