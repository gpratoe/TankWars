from abc import ABC, abstractmethod


class Mediator(ABC):
    @abstractmethod
    def notify(self, event:str, **kwargs):
        pass

class BaseMediator(ABC):
    def __init__(self):
        self._mediator = None

    def set_mediator(self, mediator:Mediator):
        self._mediator = mediator

class CollisionMediator(Mediator):
    def __init__(self, physics_component, logic_component):
        self._physics_component = physics_component
        self._logic_component = logic_component
        self._physics_component.set_mediator(self)
        self._logic_component.set_mediator(self)

    def notify(self, event:str, **kwargs):
        if event == 'Collision':
            self._logic_component.handle_collision(**kwargs)
        elif event == 'DestroyBody':
            self._physics_component.destroy_body(**kwargs)
        elif event == 'Shooting':
            self._logic_component.handle_shooting(**kwargs)

