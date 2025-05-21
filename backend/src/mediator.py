from abc import ABC, abstractmethod
import math


class Mediator(ABC):
    @abstractmethod
    def notify(self, event:str, **kwargs):
        pass

class BaseMediator(ABC):
    def __init__(self):
        self._mediator = None

    def set_mediator(self, mediator:Mediator):
        self._mediator = mediator

class LogicPhysicsMediator(Mediator):
    def __init__(self, physics_component, logic_component, input_router):
        self._physics_component = physics_component
        self._logic_component = logic_component
        self._physics_component.set_mediator(self)
        self._logic_component.set_mediator(self)
        self._input_router = input_router

    def notify(self, event:str, **kwargs):
        if event == "CreateBullet":
            logic_bullet = kwargs["logic_bullet"]
            pos = kwargs["pos"]
            angle = kwargs["angle"]
            speed = kwargs["speed"]
            groupIndex = kwargs["groupIndex"]
            physics_bullet = self._physics_component.create_bullet(bullet_id=logic_bullet.id,
                                                                 pos=pos,
                                                                 angle=angle,
                                                                 speed=speed,
                                                                 groupIndex=groupIndex)
            mediator = BulletMediator(physics_bullet, logic_bullet)
            logic_bullet.last_state = physics_bullet.get_state()

        elif event == 'CreateTank':
            logic_tank = kwargs["logic_tank"]
            pos = kwargs["pos"]
            dim = kwargs["dim"]
            physics_tank = self._physics_component.create_tank(tank_id=logic_tank.id,
                                                               pos=pos,
                                                               dim=dim)
            mediator = TankMediator(physics_tank, logic_tank)
            logic_tank.last_state = logic_tank.get_state()
            self._input_router.register_mediator(mediator, logic_tank.id)

        elif event == 'Collision':
            self._logic_component.handle_collision(**kwargs)
        elif event == 'DestroyBody':
            self._physics_component.destroy_body(**kwargs)

class TankMediator(Mediator):
    def __init__(self, physics_tank, logic_tank):
        self._physics_tank = physics_tank
        self._logic_tank = logic_tank
        self._physics_tank.set_mediator(self)
        self._logic_tank.set_mediator(self)

    def notify(self, event:str, **kwargs):
        if event == "Shooting":
            self._physics_tank.stop_tank()
            self._physics_tank.rotate_towards_target(**kwargs)
            angle = self._physics_tank.angle
            dx = self._physics_tank.wh/2 * math.cos(angle)
            dy = self._physics_tank.wh/2 * math.sin(angle)

            bullet_pos = (self._physics_tank.x + dx,
                          self._physics_tank.y + dy)

            self._logic_tank.shoot(bullet_pos, self._physics_tank.angle)

        elif event == "StopTank":
            self._physics_tank.stop_tank()

        elif event == "GetPhysicsState":
            return self._physics_tank.get_state()

        elif event == "MoveTank":
            self._physics_tank.move_to_target(**kwargs)

class BulletMediator(Mediator):
    def __init__(self, physics_bullet, logic_bullet):
        self._physics_bullet = physics_bullet
        self._logic_bullet = logic_bullet
        self._physics_bullet.set_mediator(self)
        self._logic_bullet.set_mediator(self)

    def notify(self, event:str, **kwargs):
        if event == "GetPhysicsState":
            return self._physics_bullet.get_state()
