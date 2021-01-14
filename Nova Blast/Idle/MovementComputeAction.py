from Global import *
from threading import Thread


class MovementComputeTask(Thread):
    def __init__(self, left: int, right: int):
        super(MovementComputeTask, self).__init__()
        self.left = left
        self.right = right

    def run(self):
        for i in range(self.left, self.right):
            particles[i].updateMovement()
            if particles[i].position.z > 0:
                particles.remove(particles[i])
