import math
import random

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen (width = 800, height = 600)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
# using "icon" variable I just set:
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
# coordinates:
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
# ( , ) = (range of possible random values):
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 0.6
enemyY_change = 40
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready - you can't see bullet on screen
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    # "blit" means we're drawing player onto screen
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    # "blit" means we're drawing player onto screen
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # blit makes it show up on screen


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # Changing screen color. RGB = red, green, blue; (R, G, B):
    # Can find numbers needed for specific colors online
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # all of the events that are happening get into pygame event:
    for event in pygame.event.get():
        # creating button to close game:
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -.7
            if event.key == pygame.K_RIGHT:
                playerX_change = .7
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                # Get the current x cordinate of the spaceship:
                bulletX = playerX
                fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # anything continuous has to be inside infinite "while running" loop

    playerX += playerX_change

    # prevents going out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

    enemyX += enemyX_change

    enemyX[i] += enemyX_change[i]
    if enemyX[i] <= 0:
        enemyX_change[i] = 4
        enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 736:
        enemyX_change[i] = -4
        enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change

    # screen gets drawn first, then other things:
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, testY)

    # updating screen:
    pygame.display.update()
