from Box2D import b2Vec2
import math

class Utils:
    API_URL = "http://localhost:8000"
    
    def __init__(self):
        self.PPM = 10

    def to_pixel(self, meter):
        return meter * self.PPM
    
    def to_world(self, pixel):
        return pixel / self.PPM
    
    def vec2_to_pixel(self, vec2):
        return b2Vec2(self.to_pixel(vec2[0]), self.to_pixel(vec2[1]))
    
    def vec2_to_world(self, vec2):
        return b2Vec2(self.to_world(vec2[0]), self.to_world(vec2[1]))
    

    def get_linear_velocity(self, speed, angle):
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        return (vx, vy)


utils = Utils()