from Box2D import b2World
from src.utils import utils
from src.tank import Tank

class Game:
    def __init__(self, w, h):
        self.w = utils.gameWidth = w
        self.h = utils.gameHeight = h
        self.world = utils.world = b2World(gravity=(0, 0), doSleep=True)
        self.time_step = 1.0 / 60
        self.tanks = {}
        self.tanksw = 100
        self.tanksh = 50
        self.tank_initialpos = (self.w/2, self.h/2)
        #self.bullets = {}

    def add_tank(self, name):
        if self.tanks.get(name) is None:
            self.tanks[name] = Tank(name, self.tank_initialpos, self.tanksw, self.tanksh, 0, 10, 17)
            return 0
        else:
            return 1
        

        # maybe return 1 and 0 and handle the jsons in ws.py? idk

    def run(self):
        self.world.Step(self.time_step, 6, 0)
        print(self.tanks)
        # for tank in self.tanks:
        #     tank.update()

game = Game(1900, 1080)