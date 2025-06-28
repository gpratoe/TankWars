from abc import ABC, abstractmethod
from src.common_types import EntityType
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
        if event == "CreateBody":
            btype = kwargs.pop("type")
            logic_entity = kwargs.pop("logic_entity")
            kwargs["id"] = logic_entity.id
            physics_body = self._physics_component.create_body(btype,
                                                               **kwargs)
            match btype:
                case EntityType.TANK:
                    mediator = TankMediator(physics_body,
                                            logic_entity)
                    logic_entity.last_state = logic_entity.get_state()
                    self._input_router.register_mediator(mediator,
                                                         logic_entity.id)
                case EntityType.BULLET:
                    mediator = BulletMediator(physics_body,
                                              logic_entity)
                    logic_entity.last_state = physics_body.get_state()

                case EntityType.BUFF:
                    mediator = BuffMediator(physics_body,
                                            logic_entity)

                case _:
                    pass
        elif event == 'DestroyBody':
            self._physics_component.destroy_body(**kwargs)

class TankMediator(Mediator):
    def __init__(self, physics_tank, logic_tank):
        self._physics_tank = physics_tank
        self._logic_tank = logic_tank
        self._physics_tank.set_mediator(self)
        self._logic_tank.set_mediator(self)

    def get_physics_comp(self):
        return self._physics_tank
    def get_logic_comp(self):
        return self._logic_tank

    def notify(self, event:str, **kwargs):
        if event == "Shooting" and not self._logic_tank.is_dead:
            self._physics_tank.stop_tank()
            self._physics_tank.rotate_towards_target(**kwargs)
            angle = self._physics_tank.angle
            hwh = self._physics_tank.wh/2
            dx = hwh * math.cos(angle)
            dy = hwh * math.sin(angle)

            bullet_pos = (self._physics_tank.x + dx,
                          self._physics_tank.y + dy)

            self._logic_tank.shoot(bullet_pos, self._physics_tank.angle)

        elif event == "StopTank":
            self._physics_tank.stop_tank()

        elif event == "GetPhysicsState":
            return self._physics_tank.get_state()

        elif event == "MoveTank":
            self._physics_tank.move_to_target(**kwargs)

        elif event == "Hit":
            damage = kwargs["damage"]
            self._logic_tank.health -= damage
            if self._logic_tank.health <= 0:
                self._logic_tank.is_dead = True

class BulletMediator(Mediator):
    def __init__(self, physics_bullet, logic_bullet):
        self._physics_bullet = physics_bullet
        self._logic_bullet = logic_bullet
        self._physics_bullet.set_mediator(self)
        self._logic_bullet.set_mediator(self)

    def notify(self, event:str, **kwargs):
        if event == "GetPhysicsState":
            return self._physics_bullet.get_state()
        elif event == "GetLogic":
            return self._logic_bullet.get_logic()
        elif event == "Bounce":
            self._logic_bullet.bounces_left -= 1
            if self._logic_bullet.bounces_left < 0:
                self._logic_bullet.is_dead = True
        elif event == "Dead":
            self._logic_bullet.is_dead = True

class BuffMediator(Mediator):
    def __init__(self, physics_buff, logic_buff):
        self._physics_buff = physics_buff
        self._logic_buff = logic_buff
        self._physics_buff.set_mediator(self)
        self._logic_buff.set_mediator(self)

    def notify(self, event:str, **kwargs):
        if event == "GetPhysicsState":
            return self._physics_buff.get_state()
        elif event == "Taken":
            target = kwargs["target"]
            self._logic_buff.taken = True
            self._logic_buff.effect.apply(target)
