import math
from info import TextBox
class Point:
    def __init__(self, pygame, x, y, rot, start_angle, radius=10, is_error=False, event="NOTHING", last_point=None):
        self.pg = pygame
        self.pos = [x, y]
        self.start_angle = start_angle  # Bot relative 0 angle
        self.rot = math.radians(rot) + self.start_angle
        self.min_rad = radius
        self.rad = radius
        self.rect = None
        self.event = event
        self.tb = None
        self.last_point = last_point
        self.calc_end()
        self.colors = {"active": [20, 200, 140, 255], 
                       "inactive": [200, 200, 200, 255],
                       "hover": [255,255,20,150],
                       "border_normal": [255, 255, 255, 40],
                       "border_error": [0, 30, 255, 40],
                       "border_end": [235, 50, 50, 255],
                       "angle": [150,150,150,255]}
        self.color = self.colors["active"]
        self.is_error = is_error
        self.border_color = self.colors["border_normal"]
        self.part_end = False
        self.off_surface = self.pg.Surface([50,50])

    def error_toggle(self):
        # Switch between error point and normal point 
        if self.is_error: 
            self.border_color = self.colors["border_normal"]
            self.is_error = False
        else:
            self.border_color = self.colors["border_error"]
            self.is_error = True

    def calc_end(self):
        end_x = self.pos[0] + self.rad * math.cos(self.start_angle + self.rot)
        end_y = self.pos[1] - self.rad * math.sin(self.start_angle + self.rot)
        self.end = [end_x, end_y]

    def modify(self, pressed, rect):
        if pressed[self.pg.K_w]:        # UP
            self.pos[1] = max(rect.top, self.pos[1] - 1)
        elif pressed[self.pg.K_s] and not pressed[self.pg.K_LCTRL]:# DOWN
            self.pos[1] = min(rect.bottom, self.pos[1] + 1)
        if pressed[self.pg.K_d]:        # RIGHT
            self.pos[0] = min(rect.right, self.pos[0] + 1)
        elif pressed[self.pg.K_a]:      # LEFT
            self.pos[0] = max(rect.left, self.pos[0] - 1)
        # Reduce radius
        if pressed[self.pg.K_o] and (pressed[self.pg.K_RSHIFT] or pressed[self.pg.K_LSHIFT]):        
            self.rad = max(self.rad - 2, self.min_rad)
        # Increase radius
        elif pressed[self.pg.K_o]:      
            self.rad += 2
        # decrease angle (clockwise)
        if pressed[self.pg.K_p] and (pressed[self.pg.K_RSHIFT] or pressed[self.pg.K_LSHIFT]):
            self.rot -= math.pi / 8
            while self.rot - self.start_angle < -math.pi - 0.1:
                self.rot += 2 * math.pi
        # increase angle (counter clockwise)
        elif pressed[self.pg.K_p]:
            self.rot += math.pi / 8
            while self.rot - self.start_angle >= math.pi:
                self.rot -= 2 * math.pi
        self.calc_end()

    def get_pos(self):
        return self.pos
    
    def get_rot(self):
        return math.degrees(self.rot - self.start_angle)
    
    def get_rad(self):
        return self.rad
    
    def create_tb(self, pos):
        self.tb = TextBox(self.pg, pos, self.event)
        return self.tb
    
    def destroy_tb(self):
        self.tb = None

    def save_event(self):
        if self.tb:
            self.event = self.tb.save_message().replace(" ", "_")
        self.tb = None
    
    def get_event(self):
        return self.event
    
    def collides(self, x, y):
        return self.rect and self.rect.collidepoint(x, y)

    def draw(self, surface, visible, is_selected = False, is_hovered = False, is_end = False):
        self.part_end = is_end
        if (self.last_point):
            self.pg.draw.line(surface, [200,100,0,255], self.last_point.get_pos(), self.pos, 3)
        if is_end:
            min_rect = [self.pos[0] - self.min_rad, self.pos[1] - self.min_rad, self.min_rad * 2, self.min_rad * 2]
            self.rect = self.pg.draw.rect(surface, self.colors["border_end"], min_rect, 3, 3)
            self.pg.draw.line(surface, self.colors["angle"], self.pos, self.end, 5)
        elif (visible or is_selected):
            self.rect = self.pg.draw.circle(surface, self.border_color, self.pos, self.rad, 5)
            self.pg.draw.line(surface, self.colors["angle"], self.pos, self.end, 5)
        if (not is_selected and not is_hovered):
            self.pg.draw.circle(surface, self.colors["inactive"], self.pos, 5, 5)
        elif (is_selected):
            self.pg.draw.circle(surface, self.colors["active"], self.pos, 5, 5)
        else:
            self.pg.draw.circle(surface, self.colors["hover"], self.pos, 5, 5)

class Start:
    def __init__(self, pygame, x, event = "NOTHING"):
        self.pg = pygame
        self.event = event
        self.tb = None
        self.was_selected = True
        self.rot = math.radians(270)
        self.flips = [False, True]
        self.robot = [16, 16]
        self.size = [self.robot[0] * 4, self.robot[1] * 4]
        self.pos = [x + 50, self.size[1] / 2]
        self.center = [self.size[0] / 2, self.size[1] / 2]
        self.colors = {
            "inactive": [254, 138, 24, 255],
            "active": [30, 230, 20, 255],
            "bg": [35, 35, 255, 255]
        }
        self.sprite = self.create_sprite(self.was_selected)

    def create_sprite(self, is_active):
        border_color = self.colors["active" if is_active else "inactive"] 
        sprite = self.pg.Surface(self.size)
        self.rect = sprite.get_rect()
        self.rect.topleft = [self.pos[0] - (self.size[0] / 2), 0]
        sprite.fill(self.colors["bg"])
        self.pg.draw.rect(sprite, border_color, [0, 0] + self.size, 3, 3)
        self.pg.draw.line(sprite, border_color, self.center, [self.center[0], 0], 3)
        
        return self.pg.transform.rotate(sprite, round(math.degrees(self.rot)))

    def modify(self, pressed, rect):
        if pressed[self.pg.K_d]:        # RIGHT
            self.pos[0] = min(rect.right - 190, self.pos[0] + 1)
            self.was_selected = False
        elif pressed[self.pg.K_a]:      # LEFT
            self.pos[0] = max(rect.left + 125, self.pos[0] - 1)
            self.was_selected = False
        elif pressed[self.pg.K_w]:      
            self.rot = (self.rot + (math.pi / 2)) % (2 * math.pi)
            self.was_selected = False
        elif pressed[self.pg.K_s]:
            self.rot = (self.rot - (math.pi / 2) + (2 * math.pi)) % (2 * math.pi)
            self.was_selected = False

    def get_pos(self):
        return self.pos
    
    def get_rot(self):
        return math.degrees(self.rot)
    
    def get_rad(self):
        return -1
    
    def create_tb(self, pos):
        self.tb = TextBox(self.pg, pos, self.event)
        return self.tb
    
    def destroy_tb(self):
        self.tb = None

    def save_event(self):
        if self.tb:
            self.event = self.tb.save_message().replace(" ", "_")
        self.tb = None

    def draw(self, surface, is_selected):
        if (is_selected and not self.was_selected) or (not is_selected and self.was_selected):
            self.sprite = self.create_sprite(is_selected)
            self.was_selected = is_selected
        surface.blit(self.sprite, self.rect)