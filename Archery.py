import sys
import pygame
from math import sqrt, pow
from random import randint
from time import perf_counter

pygame.init()  # initializes all pygame modules

screen = pygame.display.set_mode((800, 600))  # 800 x 600 screen size

background = pygame.image.load('background.png')

pygame.mixer.music.load("Theme.wav")
pygame.mixer.music.play()

# Title and Icon
pygame.display.set_caption("ARCHERY")
icon = pygame.image.load('bow.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 368
playerY = 480
playerX_change = 0

# Target
targetImg = []
targetX = []
targetY = []
targetX_change = []
num_of_targets = 6

for i in range(num_of_targets):
    targetImg.append(pygame.image.load('target.png'))
    targetX.append(randint(0, 736))
    targetY.append(randint(0, 320))
    targetX_change.append(0 if not i % 2 else 2.7)  # half the targets are stationary and half are moving

# Arrow
arrowImg = pygame.image.load('arrow.png')
arrowX = 0
arrowY = 480
# arrow won't move in X direction
arrowY_change = 6
arrow_state = "loaded"  # Loaded - you can't see the arrow on the screen, Fire - The arrow is in motion

# Score
score_value = 0
font = pygame.font.Font('Delight Candles.ttf', 32)
textX = 10
textY = 10

game_over_font = pygame.font.Font('Delight Candles.ttf', 64)

medal_font = pygame.font.Font('Delight Candles.ttf', 45)

# Timer co-ordinates
timeX = 10
timeY = 60


def show_score(x, y):  # displays the current score on top left
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_time(x, y):  # displays time right below the score
    time = font.render("Time: " + str(time_value), True, (255, 255, 255))
    screen.blit(time, (x, y))


def game_over_text():  # displays 'GAME OVER' in the middle of screen when time runs out
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (215, 150))


def final_medal_text(medal_):  # displays the name of the medal
    delta_x = 0
    if medal_ == 'BRONZE MEDAL':
        medal_text = medal_font.render("You got: " + str(medal_), True, (167, 112, 68))
        delta_x = -18
    if medal_ == 'SILVER MEDAL':
        medal_text = medal_font.render("You got: " + str(medal_), True, (167, 167, 173))
        delta_x = 10
    if medal_ == 'GOLD MEDAL':
        medal_text = medal_font.render("You got: " + str(medal_), True, (214, 175, 54))
        delta_x = 18
    if medal_ == 'NO MEDAL':
        medal_text = medal_font.render("You got: " + str(medal_), True, (255, 255, 255))
        delta_x = 45
    screen.blit(medal_text, (150 + delta_x, 260))


def final_medal_img(medal_type):  # displays the image of respective medal, right below the medal text
    if medal_type == "BRONZE MEDAL":
        medalImg = pygame.image.load("bronze-medal.png")
    if medal_type == 'SILVER MEDAL':
        medalImg = pygame.image.load("silver-medal.png")
    if medal_type == "GOLD MEDAL":
        medalImg = pygame.image.load("gold-medal.png")
    if medal_type == "NO MEDAL":
        medalImg = pygame.image.load("archer.png")
    screen.blit(medalImg, (368, 350))


def player(x, y):  # displays the bow on the screen
    screen.blit(playerImg, (x, y))


def target(x, y, z):  # displays the targets
    screen.blit(targetImg[z], (x, y))


def fire_arrow(x, y):  # function to display and update the position of the arrow
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrowImg, (x + 16, y + 10))


def collide(target_x, target_y, arrow_x, arrow_y):  # checks for collision
    distance = sqrt(pow(target_x - arrow_x, 2) + (pow(target_y - arrow_y, 2)))  # distance formula
    if distance < 27:
        return True
    return False


start_time = perf_counter()

# Game Loop
running = True
while running:

    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        # if keystroke is pressed, check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if arrow_state == "loaded":
                    arrow_sound = pygame.mixer.Sound('arrow-whoosh.wav')
                    arrow_sound.play()
                    arrowX = playerX
                    fire_arrow(playerX, arrowY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_targets):

        # Game Over
        seconds = (perf_counter() - start_time)  # calculate how many seconds
        time_value = int(60 - seconds)  # time remaining
        if time_value <= 0:
            time_value = 0
        if seconds > 60:  # if more than 60 seconds, game over
            for j in range(num_of_targets):
                targetY[j] = 2000  # this moves the targets out of the screen
            if score_value >= 60:
                medal = "GOLD MEDAL"
            elif score_value >= 40:
                medal = "SILVER MEDAL"
            elif score_value >= 20:
                medal = "BRONZE MEDAL"
            else:
                medal = 'NO MEDAL'
            game_over_text()
            final_medal_text(medal)
            final_medal_img(medal)
            break

        targetX[i] += targetX_change[i]
        if targetX[i] <= 0:
            targetX_change[i] = 2.7
        elif targetX[i] >= 736:
            targetX_change[i] = -2.7

        # Collision
        collision = collide(targetX[i], targetY[i], arrowX, arrowY)
        if collision:  # if collision is detected, instantly returns arrow to loaded state and respawns the target
            arrowY = 480
            arrow_state = "loaded"
            if not i % 2:
                score_value += 1
            else:
                score_value += 2
            targetX[i] = randint(0, 736)
            targetY[i] = randint(0, 320)

        target(targetX[i], targetY[i], i)

    # arrow Movement
    if arrowY <= 0:
        arrowY = 480  # arrow missed
        arrow_state = "loaded"
    if arrow_state == "fire":
        fire_arrow(arrowX, arrowY)  # updates the position of arrow
        arrowY -= arrowY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_time(timeX, timeY)
    pygame.display.update()
