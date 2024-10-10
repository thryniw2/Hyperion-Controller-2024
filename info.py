from copy import copy
import math

class InfoBox:
    def __init__(self, pygame, pos, size):
        self.pg = pygame
        self.bg_color = [150, 150, 150]
        self.text_color = [50, 50, 0]
        self.size = size
        self.area = self.pg.Surface(self.size)
        self.rect = self.area.get_rect()
        self.rect.topleft = pos
        self.area.fill(self.bg_color)
        self.text_box = None
        self.is_text_box_hovered = False
        self.font = pygame.font.Font("freesansbold.ttf", 25)

    def map_coord(self, point):
        # Assume 4:1 ratio
        # img_size = [571, 571]
        # real_size = [144, 144]
        pos = point.get_pos()
        return [pos[0] * 0.25, pos[1] * 0.25, round(point.get_rot(), 2), "N/A" if point.get_rad() < 0 else round(point.get_rad() * 0.25, 1)]

    def collides_text_box(self, mouse_x, mouse_y):
        self.is_text_box_hovered = self.text_box and self.text_box.collides(mouse_x - self.rect.left, mouse_y - self.rect.top)
        return self.is_text_box_hovered

    def makeText(self, message, pos, justified = "left"):
        text = self.font.render(message, True, self.text_color, self.bg_color)
        text_rect = text.get_rect()
        if justified == "left":
            text_rect.topleft = pos
        elif justified == "right":
            text_rect.topright = [self.rect.width - pos[0], pos[1]]
        self.new_area.blit(text, text_rect)
        return text_rect.size

    def instructions(self):
        message = ["Key Shortcuts:"
                , "wasd: move selected point"
                , "e/v: toggle use_error/visibility"
                , "x/z: remove selected/last point"
                , "</> Arrow: select prev/next point"
                , "o/p (SHIFT): inc. (dec.) rad/rot "
                , "m: change mode"]
        text_y = 0
        self.new_area = copy(self.area)
        for l in message:
            text_y += self.makeText(l, (0, text_y))[1]

        return [self.new_area, self.rect]

    def displayPointInfo(self, selected, point):
        self.new_area = copy(self.area)
        # Point id:
        id = "Start" if selected < 0 else selected
        self.makeText(f"Point: {id}", (10, 0))

        # Point use_error:
        e = False if selected < 0 else point.is_error
        self.makeText(f"use_error: {e}", (10, 0), "right")

        # Point location:
        self.makeText(f"(x, y, rot, radius): {self.map_coord(point)}", (10, 30))
        
        # Point EventCall:
        width = self.makeText("EventCall: ", (10, 60))[0]
        self.text_box = point.create_tb((width + 10, 60))
        self.text_box.draw(self.new_area, self.is_text_box_hovered)

        return [self.new_area, self.rect]
    
    def create_timeline(self, event, is_end):
        self.new_area = copy(self.area)
        if not is_end:
            min_rect = [12, 10, 20, 20]
            self.pg.draw.rect(self.new_area, [235, 50, 12, 255], min_rect, 3, 3)[2]
            width = self.makeText("Wait for: ", (50, 5))[0]
        else:
            border_color =  [20, 230, 50, 255] #  if self.visibility else [235, 50, 50, 255]
            sprite = self.pg.Surface((35, 35))
            rect = sprite.get_rect()
            rect.topleft = [rect.left + 5, rect.top + 10]
            sprite.fill([35, 35, 255, 255])
            self.pg.draw.rect(sprite, border_color, [0, 0] + list(rect.size), 3, 3)
            sprite = self.pg.transform.flip(sprite, False, True)
            self.new_area.blit(sprite, rect)
            width = self.makeText("EventCall: ", (50, 5))[0]
        
        self.text_box = TextBox(self.pg, (width + 60, 7), event)


    def display_timeline(self, pos):
        new_area = copy(self.new_area)

        self.rect = new_area.get_rect()
        self.rect.topleft = pos 
        
        self.text_box.draw(self.new_area, self.is_text_box_hovered)
        
        return [new_area, self.rect]

        
class TextBox:
    def __init__(self, pygame, pos, message):
        self.is_active = False
        self.was_hovered = False
        self.message = message
        self.current_text = message
        self.pg = pygame
        self.area = self.pg.Surface([200, 30])
        self.rect = self.area.get_rect()
        self.rect.topleft = pos
        self.colors = {
            "text": [0, 0, 0, 255],
            "bg": [255, 255, 255, 255],
            "hover": [255, 255, 0, 255],
            "saved": [44, 255, 15, 255],
            "unsaved": [255, 20, 40, 255]
        }
        self.area.fill(self.colors["bg"])
        self.font = pygame.font.Font("freesansbold.ttf", 25)
        self.makeText()

    def set_active(self, status):
        self.is_active = status
        if status and self.current_text == "NOTHING":
            self.current_text = ""
        elif not status and self.current_text == "":
            self.current_text = "NOTHING"
        self.makeText()

    def get_is_active(self):
        return self.is_active
    
    def collides(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y)
    
    def save_message(self):
        self.message = self.current_text
        return self.message
    
    def get_message(self):
        return self.message

    def modify(self, e):
        pressed = self.pg.key.get_pressed()
        if pressed[self.pg.K_BACKSPACE]:
            self.current_text = self.current_text[:-1]
        elif pressed[self.pg.K_RETURN]:
            self.set_active(False)
            return self.save_message()
        elif pressed[self.pg.K_ESCAPE]:
            self.current_text = self.message
            self.set_active(False)
        else:
            self.current_text += e.unicode
        self.makeText()
        
    def makeText(self):
        self.new_area = copy(self.area)
        if self.is_active:
            msg = self.current_text + "|"
        else:
            msg = self.current_text
        text = self.font.render(msg, True, self.colors["text"], self.colors["bg"])
        text_rect = text.get_rect()
        y_pos = (self.rect.height / 2) - (text_rect.height / 2)
        if not self.is_active or text_rect.width < self.rect.width - 20:
            text_rect.topleft = (10, y_pos)
        else:
            text_rect.topright = [self.rect.width - 10, y_pos]
        self.new_area.blit(text, text_rect)
        
    def draw(self, scr, is_hovered = False):    
        if not self.is_active and is_hovered:
            self.pg.draw.rect(self.new_area, self.colors["hover"], [0, 0] + list(self.new_area.get_size()), 3, 3)
        elif (self.message == self.current_text or (self.message == "NOTHING" and self.current_text == "")):
            self.pg.draw.rect(self.new_area, self.colors["saved"], [0, 0] + list(self.new_area.get_size()), 3, 3)
        else:
            self.pg.draw.rect(self.new_area, self.colors["unsaved"], [0, 0] + list(self.new_area.get_size()), 3, 3)
        
        
        scr.blit(self.new_area, self.rect)

