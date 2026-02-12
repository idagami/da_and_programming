from turtle import Turtle
import random

start_x = -250
y_pos = range(160, 160 + 3 * 30, 30)


class Invader(Turtle):
    def __init__(self, position, shape):
        super().__init__("square")
        self.penup()
        self.shape(shape)
        self.goto(position)


class InvaderMgr:

    def __init__(self):
        self.invader_objects: list[Invader] = []
        self.move_distance = 4  # speed of movement
        self.direction = 1  # 1 = right, -1 = left

    def create(self, image_invader):
        for y in y_pos:
            for i in range(6):
                x = start_x + i * 60
                invader = Invader((x, y), image_invader)
                self.invader_objects.append(invader)

    def moving(self):
        if not self.invader_objects:
            return

        self.move_distance = (
            4 + (18 - len(self.invader_objects)) // 3
        )  # less invaders left, faster they move

        right_edge = max(invader.xcor() for invader in self.invader_objects)
        left_edge = min(invader.xcor() for invader in self.invader_objects)

        if right_edge > 270:
            self.direction = -1
        elif left_edge < -280:
            self.direction = 1

        for invader in self.invader_objects:
            invader.setx(invader.xcor() + self.move_distance * self.direction)

    def random_shooting_invador(self):
        return random.choice(self.invader_objects)
