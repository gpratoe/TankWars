import math
import logging

class Utils:
    API_URL = "http://localhost:8000"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._setup_logger()

    def _setup_logger(self):
        handler = logging.StreamHandler()
        formmater = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        handler.setFormatter(formmater)
        self.logger.addHandler(handler)

    def to_pixel(self, meter):
        return meter * self.PPM
    
    def to_world(self, pixel):
        return pixel / self.PPM
    
    def vec2_to_pixel(self, vec2):
        return (self.to_pixel(vec2[0]), self.to_pixel(vec2[1]))
    
    def vec2_to_world(self, vec2):
        return (self.to_world(vec2[0]), self.to_world(vec2[1]))
    

    def get_linear_velocity(self, speed, angle):
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        return (vx, vy)

    def clamp(self, v, minv, maxv):
        return max(min(v, maxv), minv)


utils = Utils()
