from src.tank import Tank
from src.bullet import Bullet
from src.settings import *
from src.physics_manager import PhysicsManager

class EntityManager:
    def __init__(self, physics_manager: PhysicsManager):
        self.tanks: dict[int, Tank] = {}
        self.bullets: dict[int, Bullet] = {}
        self.physics_manager = physics_manager
        self.bullet_id_counter = 0
        self.tanks_to_remove = []
        self.bullets_to_remove = []

    def add_tank(self, player, pos, angle):
        if player.id in self.tanks:
            return 0
        
        def shoot_callback(owner_id, pos, angle, damage, speed, groupIndex):
            self.spawn_bullet(owner_id, pos, angle, damage, speed, groupIndex)

        self.tanks[player.id] = Tank(id=player.id, name=player.name,
                                     color=player.color, pos=pos,
                                     w=TANK_WIDTH, h=TANK_HEIGHT,
                                     angle=angle,
                                     physics_manager=self.physics_manager,
                                     shoot_callback=shoot_callback)
        
        return 1

    def spawn_bullet(self, owner_id, pos, angle, damage, speed, groupIndex):
        bullet = Bullet(self.bullet_id_counter, owner_id, pos, angle, damage, speed, groupIndex, self.physics_manager)
        self.bullets.setdefault(self.bullet_id_counter, bullet)
        self.bullet_id_counter += 1

    def remove_tank(self, player_id):
        if player_id in self.tanks:
            del self.tanks[player_id]

    def cleanup_entities(self):
        for tank_id in self.tanks_to_remove:
            if tank_id in self.tanks:
                del self.tanks[tank_id]
        self.tanks_to_remove.clear()

        for bullet_id in self.bullets_to_remove:
            if bullet_id in self.bullets:
                del self.bullets[bullet_id]
        self.bullets_to_remove.clear()

    def update(self):

        state = {'tanks': {}, 'bullets': {}}
        for tank_id, tank in list(self.tanks.items()):
            tank_state, same_state = tank.update_state_and_diff()
            if not same_state and tank_state:
                state['tanks'][tank_id] = tank_state
            if tank.is_dead:
                self.tanks_to_remove.append(tank_id)
        
        for bullet_id, bullet in list(self.bullets.items()):
            bullet.update()
            bullet_state, same_state = bullet.get_state()
            if not same_state and bullet_state:
                state['bullets'][bullet_id] = bullet_state
            if bullet.is_dead:
                self.bullets_to_remove.append(bullet_id)
        self.cleanup_entities()
        
        if state['tanks'] == {} and state['bullets'] == {}:
            return None
        return state
    
    def handle_client_input(self, input, player_id):
        try:
            tank = self.tanks.get(player_id)
            if tank:
                tank.apply_input(input)
        except Exception as e:
            print(f"Error handling input: {e}")