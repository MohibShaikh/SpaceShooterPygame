import pygame
from random import randint
from math import sqrt,pow


# Initializing Pygame
pygame.init()



# Creating the screen
screen = pygame.display.set_mode((800, 600))


# Background
background=pygame.image.load('background.jpg')

# Background Sound
pygame.mixer.music.load('Background.wav')
pygame.mixer.music.play(-1)


# Game Over text
over_font= pygame.font.Font('test_fixed.otf', 64)


# Title and Icon
pygame.display.set_caption('Space Raider')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)



# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change=0



# Score
score_value = 0
font = pygame.font.Font('test_fixed.otf', 32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render(f'Score: {score_value}', True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameover_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(randint(0, 735))
    enemyY.append(randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)


# Bullet

# Ready - Can't see the bullet on the screen
# Fire - Bullet moving across the screen
bulletImg= pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state='ready'



def enemy(x,y,j):
    screen.blit(enemyImg[j], (x,y))



def player(x,y):
    screen.blit(playerImg, (x,y))



def isColliding(enemyX,enemyY,bulletX,bulletY):
    distance = sqrt((pow(enemyX-bulletX,2)) + (pow(enemyY-bulletY,2)))
    if distance <27:
        return True
    else:
        return False



def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImg,(x+16,y+10))
# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # When keystroke is pressed, check wheter it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-2

            if event.key == pygame.K_RIGHT:
                playerX_change=2

            if event.key == pygame.K_SPACE:
                if bullet_state=='ready':
                    bullet_Sound = pygame.mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX ,bulletY)



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change=0



# Checking for boundaries of the spaceship so it doesn't go out of bounds
    playerX += playerX_change


    if playerX<=0:
        playerX=0
    elif playerX>=738:
        playerX=738


# Enemy Movement
    for j in range(num_of_enemies):

        # Game Over
        if enemyY[j]>450:
            for k in range(num_of_enemies):
                enemyY[k]=2000
            gameover_text()
            break

        enemyX[j] += enemyX_change[j]
        if enemyX[j] <= 0:
            enemyX_change[j] = 1
            enemyY[j] += enemyY_change[j]
        elif enemyX[j] >= 738:
            enemyX_change[j] = -1
            enemyY[j] += enemyY_change[j]

        # Collision
        collision = isColliding(enemyX[j], enemyY[j], bulletX, bulletY)
        if collision:
            explosion_Sound = pygame.mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[j] = randint(0, 735)
            enemyY[j] = randint(50, 150)
        enemy(enemyX[j], enemyY[j],j)

# Bullet Movement
    if bulletY<=0:
        bulletY=480
        bullet_state='ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()