from Box2D import b2Vec2
from src.contactlistener import ContactListener

class Utils:
    API_URL = "http://localhost:8000"
    
    def __init__(self):
        self.world = None
        self.gameHeight = 0
        self.gameWidth = 0
        self.PPM = 10
        self.mouseX = 0
        self.mouseY = 0
        self.manager = None
        self.cl = None

    def to_pixel(self, meter):
        return meter * self.PPM
    
    def to_world(self, pixel):
        return pixel / self.PPM
    
    def vec2_to_pixel(self, vec2):
        return b2Vec2(self.to_pixel(vec2[0]), self.to_pixel(vec2[1]))
    
    def vec2_to_world(self, vec2):
        return b2Vec2(self.to_world(vec2[0]), self.to_world(vec2[1]))

utils = Utils()