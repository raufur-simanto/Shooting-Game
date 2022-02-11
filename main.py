# Shooting Game using pygame
# created by raufursimanto03065@gmail.com 

import pygame
import random
pygame.init()

# creating window of height 500 and width 500
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("Shooting Game")

# setting music file
bulletSound = pygame.mixer.Sound('bullet.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# getting high score from file
with open("high_score.txt", 'r') as f:
    line = f.read()
    text, value = line.strip().split(':')

# setting sore
score = 0 
high_score = int(value)
clock = pygame.time.Clock()

# save score
def save_score():
    with open("high_score.txt", "w") as f:
        f.write("High_score:"+str(high_score))

# load images for player
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load(
    'R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load(
    'L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')


class Player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.walkCount = 0
        self.left = False
        self.right = False
        self.standing = True
        self.isJump = False
        self.jumpCount = 10
        self.hitbox = (self.x + 15, self.y+10, 29, 52)
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >=27:
                self.walkCount = 0

            if self.standing == False:
                if self.left:
                    win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1

                else:
                    win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1

            else:
                if self.left:
                    win.blit(walkLeft[0], (self.x, self.y))

                else:
                    win.blit(walkRight[0], (self.x, self.y))

            self.hitbox = (self.x + 15, self.y+10, 29, 52)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

            # health bar
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

    def hit(self):
        self.isJump = False
        self.jumpCount = 10 
        self.x = random.randint(10, 450)
        self.y = 405
        self.walkCount = 0

        # decreaseing health
        if self.health > 0:
            self.health -= 5
        else:
            self.visible = False
            goblin.visible = False
            pygame.time.delay(500)
            
            #pygame.display.update()

        # display -5 points of hit with goblin
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render('-5', 1, (255, 0, 0))
        text1 = font1.render("Game Over!!!",1,(255, 0, 0) )

        if self.visible == False:
            win.blit(text1, (50, 200)) # game over
        else:
            win.blit(text, (250 - (text.get_width()/2), 200))

        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit() 


class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy():
    # load images
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        self.health = 9
        self.visible = True

    def draw(self, win):
        self.move()

        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # health bar
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (9 - self.health)), 10))

            self.hitbox = (self.x + 17, self.y+2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel

            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
            #print("hit")
        else:
            self.visible = False
            if player.visible == True:
                self.reapear()

    def reapear(self):
        if  self.visible == False:
            self.x = random.randint(30,470)
            self.y = 410
            self.health = 9
            self.walkCount = 0
            pygame.time.delay(300)
            """i = 0
            while i < 300:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()"""
            self.visible = True
            #pygame.display.update()


player = Player(200, 405, 64, 64)
goblin = Enemy(20, 410, 64, 64, 450)


def redrawWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: '+str(score), 1, (0, 0, 0))
    text1 = font.render('High Score: '+str(high_score), 1, (0, 0, 0))
    win.blit(text1, (150, 10))
    win.blit(text, (350, 10))
    player.draw(win)
    goblin.draw(win)

    for bullet in bullets: 
            bullet.draw(win)

    pygame.display.update()


font = pygame.font.SysFont('comicsans', 30, True)


# maingameloop
bullets = []
shootingTime = 0
run = True
while run == True:
    clock.tick(27)

    # checking collision between goblin and player
    if goblin.visible and player.visible:
        if player.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and player.hitbox[1] + player.hitbox[3] > goblin.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > goblin.hitbox[0] and player.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                player.hit()  
                score -= 5 

    # checking collision with bullet
    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1]+ goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] +goblin.hitbox[2]:         
                        goblin.hit()
                        score += 1
                        if score > high_score:
                            high_score = score 
                        bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0 and player.visible:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    # checking keyboard or mouse event 
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            #print(f"Total Score {score}")
            run = False
            save_score()

    keys = pygame.key.get_pressed() 

    if shootingTime > 0:
        shootingTime += 1
    if shootingTime > 3:
        shootingTime = 0

    if keys[pygame.K_SPACE] and shootingTime == 0 and player.visible:
        bulletSound.play()  # placeing bullet sound 
        if player.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(player.x + player.width // 2), round(player.y + player.height // 2), 6, (0, 0, 0), facing))
            shootingTime = 1

    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False

    elif keys[pygame.K_RIGHT] and player.x + player.width < 500:
        player.x += player.vel
        player.right = True
        player.left = False
        player.standing = False

    else:
        player.standing = True
        player.walkCount = 0


    if player.isJump == False:
        if keys[pygame.K_UP]:       
            player.isJump = True
            #player.left = False
            #player.right = False
            player.walkCount = 0

    else: 
        if player.jumpCount >= -10:
            flag = 1 
            if player.jumpCount < 0:
                flag = -1
            player.y -= (player.jumpCount ** 2) * 0.5 * flag
            player.jumpCount -= 1

        else:
            player.isJump = False
            player.jumpCount = 10

    redrawWindow()


pygame.quit()