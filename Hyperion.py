import pygame
import time
from shapes import Point, Start
from info import InfoBox, TextBox
from copy import copy
from file_manager import FileManager

def create_window(w,h):
    pygame.init()
    screen = pygame.display.set_mode([w,h], 0, 0)
    pygame.display.set_caption("Hyperion Controller")
    pause_time = 0.02
    return screen

class Part:
    def __init__(self, start, visibility, end=None):
        self.start = start
        self.active = True
        self.visibility = visibility
        self.part_type = "continuousLine"
        self.wait_event = "NOTHING"
        self.event = "NOTHING"
        self.pts = []
        self.create_timeline()
        self.end = end

    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get_start_command(self, is_text):
        if is_text:
            event = self.start.event if self.start.event != "NOTHING" else "_"
            return f"-start {(self.start.pos[0]-50)/4},{self.start.pos[1]/4},0.0 {event} # START\n"
        event = f", EventCall({self.start.event})" if self.start.event != "NOTHING" else ""
        return f"path.start({(self.start.pos[0]-50)/4},{self.start.pos[1]/4},0.0{event})\n"
    
    def get_commands(self):
        return self.pts
    
    def get_wait_event(self):
        if self.wait_event[0].isdigit() and self.wait_event[-1].isdigit():
            return self.wait_event + "ms"
        return self.wait_event
    
    def get_event(self):
        return self.event
    
    def set_start(self, pt):
        self.start = pt
        if len(self.pts) > 0:
            self.pts[0].last_point = pt

    def set_end(self, pt):
        self.end = pt
    
    def set_visibility(self, status):
        self.visibility = status

    def set_pts(self, pts):
        self.pts = pts
        self.end = pts[-1]

    def set_event(self):
        self.wait_event = self.info1.text_box.save_message().replace(" ", "_")
        self.event = self.info2.text_box.save_message().replace(" ", "_")

    def create_sprite(self):
        border_color =  [20, 230, 50, 255] if self.visibility else [235, 50, 50, 255]
        sprite = pygame.Surface((35, 35))
        rect = sprite.get_rect()
        rect.topleft = [rect.top - (rect.width / 2), 0]
        sprite.fill([149,145,164])
        pygame.draw.rect(sprite, border_color, [0, 0] + list(rect.size), 3, 3)
        return pygame.transform.flip(sprite, False, True)

    def create_timeline(self):
        self.info1 = InfoBox(pygame, [0, 0], [400, 50])
        self.info2 = InfoBox(pygame, [0, 0], [400, 50])

        self.info1.create_timeline(self.wait_event, False)
        self.info2.create_timeline(self.event, True)

    def display_timeline(self, scr, pos):
        area, self.rect1 = self.info1.display_timeline((pos[0], pos[1]))
        scr.blit(area, self.rect1)
        height = self.rect1.height + 5
        area, self.rect2 = self.info2.display_timeline((pos[0], pos[1] + height))
        scr.blit(area, self.rect2)
        return height + self.rect2.height

    def update(self, x, y):
        self.info1.collides_text_box(x, y)
        self.info2.collides_text_box(x, y)
        self.collides = self.rect1.collidepoint([x, y]) or self.rect2.collidepoint([x, y])

    def draw(self, field):
        for i, p in enumerate(self.pts):
            p.draw(field, False, is_end=i == len(self.pts) - 1)

def save_pts(file, path):
    with open(file) as f:
        for pts in path:
            if pts[1] == "continuous_line":
                for pt in pts[1:]:
                    f.write()
    
    
def run_controller(screen):
    parts = []
    pts = []
    hovers = []
    robot = Start(pygame, 125)
    start = robot
    visibility = True
    parts.append(Part(robot, visibility))
    selected_part = 0
    prev_selected_part = selected_part
    part_tb = None
    selected = -1
    instruction_area, instruction_rect = InfoBox(pygame, (700, 50), (450, 250)).instructions()
    point_info = InfoBox(pygame, (50, 650), (550, 100))
    point_info.displayPointInfo(selected, start)
    fm = FileManager(pygame, "Auto")
    save_box = TextBox(pygame, [50, 20], "NOTHING")
    img = pygame.image.load('Into the deep.jpg')
    board = screen.blit(img, [50,50])
    mode = "create"
    typing = False
    prev_selected = selected
    while True:
        event = pygame.event.poll()
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        # Handle Window Events
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        # Handle Mouse Events
        elif event.type == pygame.MOUSEBUTTONUP:
            if not typing and save_box.collides(x, y):
                save_box.set_active(True)
                typing = True
            elif not typing and point_info.collides_text_box(x, y):
                point_info.text_box.set_active(True)
                typing = True
            elif not typing and parts[selected_part].info1.collides_text_box(x, y):
                if part_tb:
                    part_tb.set_active(False)
                part_tb = parts[selected_part].info1.text_box
                part_tb.set_active(True)
                typing = True
            elif not typing and parts[selected_part].info2.collides_text_box(x, y):
                if part_tb:
                    part_tb.set_active(False)
                part_tb = parts[selected_part].info2.text_box
                part_tb.set_active(True)
                typing = True
            elif typing:
                if point_info.text_box:
                    point_info.text_box.set_active(False)
                if part_tb:
                    part_tb.set_active(False)
                    part_tb = None
                save_box.set_active(False)
                typing = False
            
            if len(hovers) != 0:
                selected = hovers[0]
            elif (mode == "create" and board.collidepoint([x,y])):
                if len(pts) != 0:
                    new_point = Point(pygame, x - board.left, y - board.top, 0, robot.get_rot(), last_point = start if selected < 0 else pts[selected])
                    if selected < len(pts) - 1:
                        pts[selected + 1].last_point = new_point
                        pts.insert(selected + 1, new_point)
                    else:
                        if selected_part < len(parts) - 1:
                            parts[selected_part + 1].set_start(new_point)
                        pts.append(new_point)
                else:
                    pts.append(Point(pygame, x - board.left, y - board.top, 0, robot.get_rot(), last_point = start))
                print(x, y)
                selected += 1
            else:
                print("out of bounds")

        # Handle universal KeyPress Events
        if event.type == pygame.KEYDOWN and not typing: 
            pressed = pygame.key.get_pressed()
            if len(pts) > 0:
                parts[selected_part].set_pts(pts)
            # Navigate points/parts
            if pressed[pygame.K_LEFT]:
                selected = max(selected - 1, -1)
            elif pressed[pygame.K_RIGHT]:
                selected = min(selected + 1, len(pts) - 1)
            elif pressed[pygame.K_UP]:
                if selected_part > 0:
                    selected_part -= 1
            elif pressed[pygame.K_DOWN]:
                if selected_part < len(parts) - 1:
                    selected_part += 1
            if pressed[pygame.K_LCTRL] and pressed[pygame.K_s]:
                fm.write_code(parts)
                fm.write_text(parts)
            
            # Create/Delete Parts
            if pressed[pygame.K_n] and len(pts) >= 0:
                start = parts[selected_part].get_end()
                parts[selected_part].set_visibility(False)
                if selected_part == len(parts) - 1:
                    parts.append(Part(start, visibility))
                else:
                    parts.insert(selected_part + 1, Part(start, visibility, parts[selected_part + 1].get_end()))
                selected_part += 1
            elif pressed[pygame.K_b] and len(parts) > 1:
                if selected_part < len(parts) - 1:
                    parts[selected_part + 1].set_start(parts[selected_part].get_start())
                    prev_selected_part = selected_part + 1
                parts.pop(selected_part)
            
            # Delete last point in part
            if pressed[pygame.K_z] and len(pts) > 0:
                pts.pop()
                selected = len(pts) - 1
                if selected_part < len(parts) - 1:
                    parts[selected_part + 1].set_start(pts[selected])
            
        if selected != prev_selected:
            if prev_selected >= 0 and prev_selected < len(pts):
                pts[prev_selected].destroy_tb()
            info_area, info_rect = point_info.displayPointInfo(selected, start if selected < 0 else pts[selected])
            prev_selected = selected

        if selected_part != prev_selected_part:
            pts = parts[selected_part].get_commands()
            start = parts[selected_part].get_start()
            selected = -1
            prev_selected = selected
            prev_selected_part = selected_part

        # Handle TextBox KeyPress Events
        if event.type == pygame.KEYDOWN and typing:
            if save_box.get_is_active():
                save_box.modify(event)
                if not save_box.get_is_active():
                    fm.set_filename(save_box.save_message())
                    typing = False
            if point_info.text_box and point_info.text_box.get_is_active():
                point_info.text_box.modify(event)
                if not point_info.text_box.get_is_active():
                    pts[selected].save_event()
                    typing = False
            if part_tb and part_tb.get_is_active():
                part_tb.modify(event)
                if not part_tb.get_is_active():
                    parts[selected_part].set_event()
                    part_tb = None
                    typing = False
        
        # Handle Start KeyPress Events
        elif event.type == pygame.KEYDOWN and selected == -1:
            start.modify(pressed, board)
            
            # update point info
            info_area, info_rect = point_info.displayPointInfo(selected, start)

        # Handle Point KeyPress Events
        elif event.type == pygame.KEYDOWN and selected >= 0:
            pts[selected].modify(pressed, board)
            if pressed[pygame.K_e]:
                pts[selected].error_toggle()
            if pressed[pygame.K_v] and not typing:
                visibility = not visibility
            
            # Delete points
            if pressed[pygame.K_x] and selected > -1:
                if selected != len(pts) - 1:
                    pts[selected + 1].last_point = pts[selected].last_point
                pts.pop(selected)
                if selected >= len(pts):
                    selected = len(pts) - 1
                    if selected_part < len(parts) - 1:
                        parts[selected_part + 1].set_start(pts[selected])
            
            # update point info
            info_area, info_rect = point_info.displayPointInfo(selected, pts[selected] if selected >= 0 else start)
        

        # Reset the Screen
        screen.fill((0, 0, 0))
        
        # Draw InfoBoxes
        screen.blit(instruction_area, instruction_rect)
        if len(pts) != 0:
            screen.blit(info_area, info_rect)
            point_info.text_box.draw(info_area, point_info.collides_text_box(x, y))
        
        
        field = copy(img)
        robot.draw(field, selected == -1)

        # Draw the Timeline
        timeline_y = 350
        for i, part in enumerate(parts):
            if i != selected_part:
                part.draw(field)
            height = part.display_timeline(screen, (700, timeline_y))
            part.update(x, y)
            timeline_y += height + 10
        # end_timeline.display_timeline(screen, (700, timeline_y), True)
        
        # Draw the Field
        save_box.draw(screen, save_box.collides(x, y))
        hovers = []
        for i, pt in enumerate(pts):
            if pt.collides(x - board.left, y - board.top) and not selected == i:
                hovers.append(i)
            pt.draw(field, visibility, selected == i, i in hovers, i == len(pts) - 1)
        board = screen.blit(field, [board.left, board.top])

        pygame.display.update()
        

if __name__ == "__main__":
    scr = create_window(1200,750)
    #scr.fill((0, 0, 0))
    #pt = Point(pygame, 200, 400, 60, 30)
    #pt2 = Point(pygame, 400, 500, 60, 50, pt)
    #pt.draw(scr, True)
    #pt2.draw(scr, True)
    #pygame.display.update()
    #time.sleep(5)
    run_controller(scr)
