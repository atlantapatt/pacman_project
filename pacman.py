#!/usr/bin/env python
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from board import boards
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
startup_counter = 0
moving = False


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))

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

run = True

if run == True:
    print('game is running')

while run:
    timer.tick(fps)
    print(counter)
    print(flicker)
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
    draw_misc()
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
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
