from turtle import Turtle


MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
snake_body = ["head", "b", "c"]


class Snake:
    def __init__(self):
        self.body_segments_obj = []
        self.create_snake()  # By calling this in __init__, you automatically
        # build the snake segments as soon as you make the object.
        # Without it, you’d have to manually call snake.create_snake()
        # every time, which is less convenient.
        self.head = self.body_segments_obj[0]
        self.head.color("yellow")

    def create_snake(self):  # inside class, it doesnt matter that f was
        # created AFTER if was called in init, python reads file as a whole.
        # Unlike regular code, where f can be called only after it was defined
        x_start = 0
        y_start = 0
        for segment in snake_body:
            segment = Turtle("square")
            segment.color("white")
            segment.penup()
            segment.goto(x_start, y_start)
            x_start -= 20  # to stay adjacent toprevious square body
            # self.speed() cannot be used becuz we disabled the animation.
            self.body_segments_obj.append(segment)

    def move(self):
        for seg_num in range(
            len(self.body_segments_obj) - 1, 0, -1  # range(start, stop, step)
        ):  # range from last piece whose index will be (len(obj) - 1)
            # my_screen.update() ## we see each single segment move in order 1 2 3 1 2 3, not simultaneously
            # time.sleep(1)  ## adds 1 second delay after each segment moves
            new_x = self.body_segments_obj[seg_num - 1].xcor()
            new_y = self.body_segments_obj[seg_num - 1].ycor()
            self.body_segments_obj[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def move_up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)  # the rest of body will follow in move() function

    def move_down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def move_left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def move_right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def extend(self):
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_x = self.body_segments_obj[-1].xcor()
        new_y = self.body_segments_obj[-1].ycor()
        new_segment.goto(new_x, new_y)
        self.body_segments_obj.append(new_segment)

    def reset(self):  # we are initializing the snake again
        # for segment in self.body_segments_obj: # option 2 to visually hide the old snake from screen
        #     segment.goto(1000, 1000)
        for seg in self.body_segments_obj:
            seg.hideturtle()
        self.body_segments_obj.clear()
        self.create_snake()
        self.head = self.body_segments_obj[0]
        self.head.color("yellow")
