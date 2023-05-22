from collections import deque


class Stack(deque):

    def __init__(self):
        super().__init__()

    def stackup(self, a):
        super().append(a)

    def unstack(self):
        return super().pop()