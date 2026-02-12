from turtle import Screen
from obstacles_class import ObstacleMgr
from cannon_class import Cannon
from invaders_class import InvaderMgr
from bombs_class import BombManager
from iron_dome_ppo_class import PpoManager
from score_class import Scoreboard
import time, random, os

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BG_IMAGE = os.path.join(BASE_DIR, "cloudsgif.gif")
INVADER_IMAGE = os.path.join(BASE_DIR, "invader_gif.gif")
CANNON_IMAGE = os.path.join(BASE_DIR, "home_base_gif.gif")

# --------------------------------------------

my_screen = Screen()
my_screen.setup(width=600, height=600)
my_screen.bgcolor("blue")
my_screen.bgpic(BG_IMAGE)
my_screen.title("Space invaders game")
my_screen.tracer(0)

my_screen.addshape(INVADER_IMAGE)
my_screen.addshape(CANNON_IMAGE)

obstacle_mgr = ObstacleMgr()
obstacle_mgr.create()

invader_mgr = InvaderMgr()
invader_mgr.create(INVADER_IMAGE)

score = Scoreboard()

bomb_mgr = BombManager(score)
drop_chance = 0.02

ppo_cannon = Cannon(CANNON_IMAGE)
iron_dome_ppo = PpoManager()


def cannon_shoot():
    if len(iron_dome_ppo.ppo_objects) < 2:
        x = ppo_cannon.xcor()
        iron_dome_ppo.create(x)


my_screen.onkey(key="Right", fun=ppo_cannon.move_right)
my_screen.onkey(key="Left", fun=ppo_cannon.move_left)
my_screen.onkey(key="space", fun=cannon_shoot)
my_screen.onkeypress(my_screen.bye, "q")

my_screen.listen()

while not score.game_is_over:
    my_screen.update()

    invader_mgr.moving()

    if not invader_mgr.invader_objects:  # WIN condition
        score.game_over(result="won")
        break

    if len(bomb_mgr.bomb_objects) < 5 and random.random() < drop_chance:
        shooting_invader = invader_mgr.random_shooting_invador()
        bomb_mgr.create(shooting_invader.position())

    bomb_mgr.move_all()
    bomb_mgr.remove_bomb_offscreen()
    iron_dome_ppo.move_all()
    iron_dome_ppo.remove_ppo_offscreen()

    for ppo_bullet in iron_dome_ppo.ppo_objects[:]:
        removed_bullet = False

        for obstacle in obstacle_mgr.obstacle_objects:
            if ppo_bullet.distance(obstacle) < 10:  # bullet hit obstacle
                obstacle.hideturtle()
                ppo_bullet.hideturtle()
                obstacle_mgr.obstacle_objects.remove(obstacle)
                iron_dome_ppo.ppo_objects.remove(ppo_bullet)
                removed_bullet = True
                break
        if removed_bullet:
            continue

        for bomb in bomb_mgr.bomb_objects[:]:  # bullet hits bomb
            if ppo_bullet.distance(bomb) < 15:
                bomb.hideturtle()
                ppo_bullet.hideturtle()
                bomb_mgr.bomb_objects.remove(bomb)
                iron_dome_ppo.ppo_objects.remove(ppo_bullet)
                removed_bullet = True
                score.increase_score(3)
                break
        if removed_bullet:
            continue

        for invader in invader_mgr.invader_objects:
            if ppo_bullet.distance(invader) < 20:  # bullet hits invader
                invader.hideturtle()
                ppo_bullet.hideturtle()
                invader_mgr.invader_objects.remove(invader)
                score.increase_score(5)
                break

    for bomb in bomb_mgr.bomb_objects[:]:
        if ppo_cannon.distance(bomb) < 15:  # bomb hits cannon
            bomb.hideturtle()
            bomb_mgr.bomb_objects.remove(bomb)
            score.decrease_score(3)
            score.decrease_lives()
            ppo_cannon.reset_position()
            break  # 1 hit minus 1 life, in case 2 bombs drop simultaneously, still 1 life taken

    drop_chance += 0.00001
    time.sleep(0.005)

my_screen.exitonclick()
