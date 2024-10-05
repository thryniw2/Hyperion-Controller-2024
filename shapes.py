import pygame
import math
class Point:
    def __init__(self, pygame, x, y, rot, radius, last_point=None):
        self.pg = pygame
        self.pos = [x, y]
        self.rot = math.radians(rot)
        self.rad = radius
        self.last_point = last_point
        self.calc_end()
        self.colors = {"active": [20, 200, 140, 255], 
                       "inactive": [200, 200, 200, 255],
                       "hover": [255,255,20,150],
                       "border_normal": [255, 255, 255, 40],
                       "border_error": [0, 30, 255, 40]}
        self.color = self.colors["active"]
        self.is_error = False
        self.border_color = self.colors["border_normal"]

    def error_toggle(self):
        # Switch between error point and normal point 
        if self.is_error: 
            self.border_color = self.colors["border_normal"]
            self.is_error = False
        else:
            self.border_color = self.colors ["border_error"]
            self.is_error = True

    def calc_end(self):
        end_x = self.pos[0] + self.rad * math.cos(self.rot)
        end_y = self.pos[1] + self.rad * math.sin(self.rot)
        self.end = [end_x, end_y]

    def move(self, pressed, rect):
        if pressed[self.pg.K_w]: # UP
            self.pos[1] = max(rect.top, self.pos[1] - 1)
        elif pressed[self.pg.K_s]:     # DOWN
            self.pos[1] = min(rect.bottom, self.pos[1] + 1)
        if pressed[self.pg.K_d]:      # RIGHT
            self.pos[0] = min(rect.right, self.pos[0] + 1)
        elif pressed[self.pg.K_a]:     # LEFT
            self.pos[0] = max(rect.left, self.pos[0] - 1)
        
        self.calc_end()

    def get_pos(self):
        return self.pos
    
    def collides(self, x, y):
        return self.rect.collidepoint(x, y)

    def draw(self, surface, visible, is_selected = False, is_hovered = False):
        if (self.last_point):
            self.pg.draw.line(surface, [200,100,0,255], self.last_point.get_pos(), self.pos, 3)
        if (visible or is_selected):
            self.pg.draw.line(surface,[150,150,150,255], self.pos, self.end, 5)
            self.rect = self.pg.draw.circle(surface, self.border_color, self.pos, self.rad, 5)
        if (not is_selected and not is_hovered):
            self.pg.draw.circle(surface, self.colors["inactive"], self.pos, 5, 5)
        elif (is_selected):
            self.pg.draw.circle(surface, self.colors["active"], self.pos, 5, 5)
        else:
            self.pg.draw.circle(surface, self.colors["hover"], self.pos, 5, 5)

class Start:
    def __init__(self, pygame, x):
        self.pg = pygame
        self.size = (50, 50)
        self.pos = [x, self.size[1] / 2]
        self.rect = [x - self.size[0] / 2, 0, self.size[0], self.size[1]]
        self.colors = {
            "start": [254, 138, 24, 255]
        }

    def get_pos(self):
        return self.pos

    def draw(self, surface):
        self.pg.draw.circle(surface, self.colors["start"], self.pos, 5, 5)
        self.pg.draw.rect(surface, self.colors["start"], self.rect, 3, 3)
