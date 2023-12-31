#!/usr/bin/env python
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from board import boards
# from Ghost_Class import Ghost
import pygame
import math

print('start game')
pygame.init()



WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 60
level = boards
color = 'blue'
font = pygame.font.Font('freesansbold.ttf', 20)
PI = math.pi
player_images = []
for i in range (1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45,45)))
ghost_red = pygame.transform.scale(pygame.image.load('assets/ghost_images/red.png'), (45,45))
ghost_blue = pygame.transform.scale(pygame.image.load('assets/ghost_images/blue.png'), (45,45))
ghost_orange = pygame.transform.scale(pygame.image.load('assets/ghost_images/orange.png'), (45,45))
ghost_pink = pygame.transform.scale(pygame.image.load('assets/ghost_images/pink.png'), (45,45))
ghost_spooked = pygame.transform.scale(pygame.image.load('assets/ghost_images/powerup.png'), (45,45))
ghost_dead = pygame.transform.scale(pygame.image.load('assets/ghost_images/dead.png'), (45,45))


red_x = 56
red_y = 58
red_direction = 0

blue_x = 448
blue_y = 388
blue_direction = 2

orange_x = 448
orange_y = 438
orange_direction = 2

pink_x = 440
pink_y = 438
pink_direction = 2

player_x = 450
player_y = 663
direction = 0
counter = 0
flicker = False
turns_allowed = [False, False, False, False]
#R,L,U,D
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

red_dead = False
blue_dead = False
orange_dead = False
pink_dead = False
red_box = False
blue_box = False
orange_box = False
pink_box = False
ghost_speed = 2

startup_counter = 0
moving = False
lives = 3



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
        #draw ghosts and change image when player collects powerup
        if (not powerup and not self.dead)  or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(ghost_spooked, (self.x_pos, self.y_pos))
        else:
            screen.blit(ghost_dead, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36,36))
        return ghost_rect
    
    def check_collisions(self):
        num1 = ((HEIGHT -50)// 32)
        num2 = (WIDTH//30)
        ##num 3 is half the width of the sprites' bodies
        num3 = 15
        
        self.turns = [False, False, False, False]
        if self.center_x // 30 < 29:
            #Right and left collisions for ghosts
            if level[self.center_y//num1][(self.center_x - num3)//num2] < 3 \
                or (level[self.center_y//num1][(self.center_x - num3)//num2] == 9 and (
            self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y//num1][(self.center_x + num3)//num2] < 3 \
                or (level[self.center_y//num1][(self.center_x + num3)//num2] == 9 and (
            self.in_box or self.dead)):
                self.turns[0] = True
            #Up and down collisions for ghosts
            if level[(self.center_y + num3)//num1][(self.center_x)//num2] < 3 \
                or (level[(self.center_y + num3)//num1][(self.center_x)//num2] == 9 and (
            self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3)//num1][(self.center_x)//num2] < 3 \
                or (level[(self.center_y - num3)//num1][(self.center_x)//num2] == 9 and (
            self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <=18:
                    if level[(self.center_y + num3)//num1][self.center_x//num2] < 3 \
                        or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3)//num1][self.center_x//num2] < 3 \
                        or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_x % num1 <=18:
                    if level[(self.center_y)//num1][(self.center_x - num2)//num2] < 3 \
                        or (level[(self.center_y)//num1][(self.center_x - num2)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[(self.center_y)//num1][(self.center_x + num2)//num2] < 3 \
                        or (level[(self.center_y)//num1][(self.center_x + num2)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <=18:
                    if level[(self.center_y + num3)//num1][self.center_x//num2] < 3 \
                        or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3)//num1][self.center_x//num2] < 3 \
                        or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_x % num1 <=18:
                    if level[(self.center_y)//num1][(self.center_x - num3)//num2] < 3 \
                        or (level[(self.center_y)//num1][(self.center_x - num3)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[(self.center_y)//num1][(self.center_x + num3)//num2] < 3 \
                        or (level[(self.center_y)//num1][(self.center_x + num3)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            else:
                self.turns[0] = True
                self.turns[1]= True
            #check if ghost is in box
            if 350 < self.x_pos < 550 and 370 < self.y_pos < 490:
                self.in_box = True
            else:
                self.in_box = False
                

        return self.turns, self.in_box 

    def move_orange(self):
        #direction for moving right
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        #direction for moving left
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] > self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        #direction for moving up
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed    
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        #direction for moving down
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        #if goes off screen 
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

#check if colliding with white dots
def check_collisions(scr, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scr += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scr += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scr, power, power_count, eaten_ghosts

def draw_board(lvl):
    num1 = ((HEIGHT -  50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
            if lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 10)
            if lvl[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i*num1),
                                 (j * num2 + (0.5 * num2), i*num1 + num1), 3)
            if lvl[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i*num1 + (0.5*num1)),
                                 (j * num2 + num2, i*num1 + (0.5*num1)), 3)
            if lvl[i][j] == 5:
                pygame.draw.arc(screen, color, 
                                [(j*num2 - (num2*0.4))  - 2, (i * num1 + (0.5*num1)), num2, num1], 0, PI/2, 3)
            if lvl[i][j] == 6:
                pygame.draw.arc(screen, color, 
                                [(j*num2 + (num2*0.5)), (i * num1 + (0.5*num1)), num2, num1], PI/2, PI, 3)
            if lvl[i][j] == 7:
                pygame.draw.arc(screen, color, 
                                [(j*num2 + (num2*0.5)), (i * num1 - (0.4*num1)), num2, num1], PI, 3*PI/2, 3)
            if lvl[i][j] == 8:
                pygame.draw.arc(screen, color, 
                                [(j*num2 - (num2*0.4)) - 2, (i * num1 - (0.4*num1)), num2, num1], 3*PI/2, 2*PI, 3)
            if lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i*num1 + (0.5*num1)),
                                 (j * num2 + num2, i*num1 + (0.5*num1)), 3)

def draw_player():
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    #Should I change the numbers to constants
    num1 = (HEIGHT-50)//32
    num2 = (WIDTH//30)
    #checks width of body size
    num3 = 15 
    


    if centerx //30 < 29:
        #check player location
        if direction == 0:
            if level[centery//num1][(centerx - num3)// num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery//num1][(centerx + num3)// num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3)//num1][(centerx)// num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3)//num1][(centerx)// num2] < 3:
                turns[2] = True

        #check if can move up or down
        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3)//num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3)//num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[(centery//num1)][(centerx - num2)// num2] < 3:
                    turns[1] = True
                if level[(centery//num1)][(centerx + num2) // num2] < 3:
                    turns[0] = True

        #check if can move right or left
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1)//num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1)//num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[(centery//num1)][(centerx - num3)// num2] < 3:
                    turns[1] = True
                if level[(centery//num1)][(centerx + num3) // num2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1]= True

    return turns

def move_player(play_x, play_y):
    if direction == 0 and turns_allowed [0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed [2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def get_targets(orange_x, orange_y, blue_x, blue_y, pink_x, pink_y, red_x, red_y):
    if player_x < 450:
        runaway_x = 980
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    #where and how ghosts run away during player powerup
    if powerup:
        if not orange.dead:
            orange_target = (runaway_x, runaway_y)
        else:
            orange_target = return_target
        if not pink.dead:
            pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not red.dead:
            red_target = (runaway_x, runaway_y)
        else:
            red_target = return_target
        if not blue.dead:
            blue_target = (runaway_x, runaway_y)
        else:
            blue_target = return_target
    else:
        if not orange.dead:
            if 340 < orange_x < 560 and 380 < orange_y < 500:
                orange_target = (400, 100)
            orange_target = (player_x, player_y)
        else:
            orange_target = return_target
        if not pink.dead:
            if 340 < pink_x < 560 and 380 < pink_y < 500:
                pink_target = (400, 100)
            pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not red.dead:
            if 340 < red_x < 560 and 380 < red_y < 500:
                red_target = (400, 100)
            red_target = (player_x, player_y)
        else:
            red_target = return_target
        if not blue.dead:
            if 340 < blue_x < 560 and 380 < blue_y < 500:
                blue_target = (400, 100)
            blue_target = (player_x, player_y)
        else:
            blue_target = return_target

    return [orange_target, pink_target, red_target, blue_target]


run = True

if run == True:
    print('game is running')

while run:
    timer.tick(fps) 
    if counter < 19:
        counter  += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True


    screen.fill('black')
    draw_board(boards)
    draw_player()
    red = Ghost(red_x, red_y, targets[0], ghost_speed, ghost_red, red_direction, red_dead,
                 red_box, 0)
    blue = Ghost(blue_x, blue_y, targets[0], ghost_speed, ghost_blue, blue_direction, blue_dead,
                 blue_box, 1)
    orange = Ghost(orange_x, orange_y, targets[0], ghost_speed, ghost_orange, orange_direction, orange_dead,
                    orange_box, 2)
    pink = Ghost(pink_x, pink_y, targets[0], ghost_speed, ghost_pink, pink_direction, pink_dead,
                  pink_box, 3)

    
    draw_misc()
    targets = get_targets(orange_x, orange_y, blue_x, blue_y, pink_x, pink_y, red_x, red_y)
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        orange_x, orange_y, orange_direction = orange.move_orange()
        blue_x, blue_y, blue_direction = blue.move_orange()
        red_x, red_y, red_direction = red.move_orange()
        pink_x, pink_y, pink_direction = pink.move_orange()

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quitting game')
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command =  1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command =  3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command =  direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command =  direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()
pygame.quit()
