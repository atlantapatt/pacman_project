# from pacman import powerup, eaten_ghost, ghost_spooked, ghost_dead, screen
# import pygame

class Ghost:

    def __init__(self, x_coord, y_coord, target, speed, img, direction, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direction
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead)  or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(ghost_spooked, (self.x_pos, self.y_pos))
        else:
            screen.blit(ghost_dead, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36,36))
        return ghost_rect
    
    def check_collisions(self):
        self.turns = [False, False, False, False]
        self.in_box = True
        return self.turns, self.in_box 