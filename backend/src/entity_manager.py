from src.tank import Tank
from src.bullet import Bullet
from src.settings import *

class EntityManager:
    def __init__(self):
        self.tanks: dict[int, Tank] = {}
        self.bullets: dict[int, list[Bullet]] = {}

    def add_tank(self, player, pos, angle):
        if player.id in self.tanks:
            return 0
        self.tanks[player.id] = Tank(id=player.id, name=player.name,
                                     color=player.color, pos=pos,
                                     w=TANK_WIDTH, h=TANK_HEIGHT,
                                     angle=angle)
        self.bullets[player.id] = self.tanks[player.id].alive_bullets
        return 1

    def remove_tank(self, player_id):
        if player_id in self.tanks:
            del self.tanks[player_id]
            del self.bullets[player_id]

    def update(self):
        '''
        Updates all tanks and bullets in the game.
        Returns state of tanks and bullets and a list of tanks to remove if they died
        '''
        to_remove = []
        for tank in self.tanks.values():
            if tank.update():
                to_remove.append(tank.id)
                self.tanks.pop(tank.id)
                self.bullets.pop(tank.id)
        return self.__get_state(to_remove)
    
    def __get_state(self, tanks_to_remove):
        state = {
            "tanks": {id: tank.get_state() for id, tank in self.tanks.items()},
            "bullets": {id: [bullet.get_state() for bullet in bullets] for id, bullets in self.bullets.items()},
            "tanks_to_remove": tanks_to_remove,
        }
        return state

    def handle_client_input(self, input, player_id):
        try:
            tank = self.tanks.get(player_id)
            if tank:
                tank.mouseX = input['mouseX']
                tank.mouseY = input['mouseY']
                tank.is_shooting = input['shooting']
        except Exception as e:
            print(f"Error handling input: {e}")