import pygame
import time
from shapes import Point, Start
from info import InfoBox
from copy import copy

def create_window(w,h):
    pygame.init()
    screen = pygame.display.set_mode([w,h], 0, 0)
    pygame.display.set_caption("Hyperion Controller")
    pause_time = 0.02
    return screen

def save_pts(file, path):
    with open(file) as f:
        for pts in path:
            if pts[1] == "continuous_line":
                for pt in pts[1:]:
                    f.write()
    
    
def run_controller(screen):
    pts = []
    hovers = []
    font = pygame.font.Font('freesansbold.ttf', 25)
    instruction_area, instruction_rect = InfoBox(pygame, (700, 50), (450, 250)).instructions()
    img = pygame.image.load('Into the deep.jpg')
    board = screen.blit(img, [50,50])
    start = Start(pygame, 450)
    mode = "create"
    selected = -1
    prev_selected = selected
    visibility = True
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
            if len(hovers) != 0:
                selected = hovers[0]
            elif (mode == "create" and board.collidepoint([x,y])):
                if len(pts) != 0:
                    new_point = Point(pygame, x - board.left, y - board.top, 0, 20, pts[selected])
                    if selected < len(pts) - 1:
                        pts[selected + 1].last_point = new_point
                        pts.insert(selected + 1, new_point)
                    else:
                        pts.append(new_point)
                else:
                    pts.append(Point(pygame, x - board.left, y - board.top, 0, 20, start))
                print(x, y)
                selected += 1
            else:
                print("out of bounds")

        if len(pts) != 0 and selected != prev_selected:
            info_area, info_rect = InfoBox(pygame, (50, 650), (500, 100)).displayPointInfo(selected, pts[selected])

        # Handle KeyPress Events
        if event.type == pygame.KEYDOWN and len(pts) != 0:
            pressed = pygame.key.get_pressed()
            pts[selected].move(pressed, board)
            if pressed[pygame.K_z]:
                pts.pop()
                selected = len(pts) - 1
            elif pressed[pygame.K_x]:
                if selected != len(pts) - 1:
                    pts[selected + 1].last_point = pts[selected].last_point
                pts.pop(selected)
                if len(pts) <= selected:
                    selected = len(pts) - 1
            if pressed[pygame.K_LEFT]:
                selected = max(selected - 1, -1)
            elif pressed[pygame.K_RIGHT]:
                selected = min(selected + 1, len(pts) - 1)
            if pressed[pygame.K_e]:
                pts[selected].error_toggle()
            if pressed[pygame.K_v]:
                visibility = not visibility

        # Draw the field
        screen.fill((0, 0, 0))
        screen.blit(instruction_area, instruction_rect)
        if len(pts) != 0:
            screen.blit(info_area, info_rect)
        field = copy(img)
        start.draw(field)
        hovers = []
        for i, pt in enumerate(pts):
            if i == selected:
                pt.draw(field, visibility, is_selected = True)
            elif pt.collides(x - board.left, y - board.top):
                hovers.append(i)
                pt.draw(field, visibility, is_hovered = True)
            else:
                pt.draw(field, visibility)
        board = screen.blit(field, [board.left, board.top])
        pygame.display.update()
        

if __name__ == "__main__":
    print("here")
    scr = create_window(1200,750)
    #scr.fill((0, 0, 0))
    #pt = Point(pygame, 200, 400, 60, 30)
    #pt2 = Point(pygame, 400, 500, 60, 50, pt)
    #pt.draw(scr, True)
    #pt2.draw(scr, True)
    #pygame.display.update()
    #time.sleep(5)
    run_controller(scr)
