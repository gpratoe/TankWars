from src.tank import Tank
from src.bullet import Bullet
from src.settings import *
from src.physics_manager import PhysicsManager

class EntityManager:
    def __init__(self, physics_manager: PhysicsManager):
        self.tanks: dict[int, Tank] = {}
        self.bullets: dict[int, list[Bullet]] = {}
        self.physics_manager = physics_manager
        self.tanks_to_stop_updating = []

    def add_tank(self, player, pos, angle):
        if player.id in self.tanks:
            return 0
        self.tanks[player.id] = Tank(id=player.id, name=player.name,
                                     color=player.color, pos=pos,
                                     w=TANK_WIDTH, h=TANK_HEIGHT,
                                     angle=angle,
                                     physics_manager=self.physics_manager)
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
        for tank_id in self.tanks_to_stop_updating:
            if tank_id in self.tanks:
                self.tanks.pop(tank_id)
        
        self.tanks_to_stop_updating = []
        
        bullets_to_remove = {}

        tanks_to_process = list(self.tanks.values())
        for tank in tanks_to_process:
            tank.update()
            if tank.is_dead:
                self.physics_manager.destroy_body(tank.tank)
                self.tanks_to_stop_updating.append(tank.id)


        for tank_id, bullets in self.bullets.items():
            if not tank_id in bullets_to_remove:
                bullets_to_remove[tank_id] = []

            bullets_to_process = bullets.copy()
            for bullet in bullets_to_process:
                if bullet.update():
                    bullets_to_remove[tank_id].append(bullet.id)
                    self.bullets[tank_id].remove(bullet)
                
        return self.__get_state(bullets_to_remove)
    
    def __get_state(self, bullets_to_remove):
        state = {
            "tanks": {id: tank.get_state() for id, tank in self.tanks.items()},
            "bullets": {id: [bullet.get_state() for bullet in bullets] for id, bullets in self.bullets.items()},
            "bullets_to_remove": bullets_to_remove
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