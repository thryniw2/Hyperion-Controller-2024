class InfoBox:
    def __init__(self, pygame, pos, size):
        self.pygame = pygame
        self.bg_color = [150, 150, 150]
        self.text_color = [50, 50, 0]
        self.size = size
        self.area = self.pygame.Surface(self.size)
        self.rect = self.area.get_rect()
        self.rect.topleft = pos
        self.area.fill(self.bg_color)
        self.font = pygame.font.Font('freesansbold.ttf', 25)

    def makeText(self, message, pos):
        text = self.font.render(message, True, self.text_color, self.bg_color)
        text_rect = text.get_rect()
        text_rect.topleft = pos
        self.area.blit(text, text_rect)
        return text_rect.size

    def instructions(self):
        message = ["Key Shortcuts:"
                , "wasd: move selected point"
                , "e: toggle use_error"
                , "xz: remove selected/last point"
                , "LEFT Arrow: select previous point"
                , "RIGHT Arrow: select next point"
                , "v: toggle visibility"
                , "m: change mode"]
        text_y = 0
        for l in message:
            text_y += self.makeText(l, (0, text_y))[1]

        return [self.area, self.rect]
    
   

    def displayPointInfo(self, selected, point):
        # Point id:
        self.makeText(f"Point: {selected}", (10, 0))

        # Point location:
        self.makeText(f"(x, y): {point.get_pos()}", (10, 30))
        
        return [self.area, self.rect]

        
            

