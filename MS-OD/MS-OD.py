import pygame
import sys
import random
import math
# pygame 1.9.4

pygame.init()
pygame.key.set_repeat(0)
size = width, height = 1280, 720
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

teal = [0, 150, 255]
black = [0, 0, 0]
white = [255, 255, 255]
green = [0, 255, 0]
red = [255, 0, 0]
blue = [0, 0, 255]
orange = [255, 156, 55]

font1 = pygame.font.Font("res/pixelmix.ttf", 23)
font2 = pygame.font.Font("res/pixelmix_bold.ttf", 150)
font3 = pygame.font.Font("res/pixelmix_bold.ttf", 50)
font4 = pygame.font.Font("res/pixelmix_bold.ttf", 48)
font5 = pygame.font.Font("res/pixelmix_bold.ttf", 75)

def game():
    xspeed = 0  
    yspeed = 0
    xpos = 0
    ypos = 0

    money = 2000  
    lives = 50

    click = 0  
    icon = 0
    place = 0

    enemycount = 0  
    producecount = 0
    wave = 1
    spawncount = 0
    alienspacing = 30
    numaliens = 5
    empty = 0
    hlth = 10
    spd = 2
    healthspacing = -10

    enemies1 = []
    turrets1 = []
    turrets2 = []
    turrets3 = []
    bullets = []
    lasers = []

    class Turret:  
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.cost = 300
            self.image = pygame.image.load("res/towerimg1.gif")
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.reload = 0

        def shoot(self):
            if self.reload > 60 and len(enemies1) > 0:
                min_d = 300  
                enemy = None
                for e1 in enemies1:
                    d = math.sqrt((t1.x - e1.x) ** 2 + (t1.y - e1.y) ** 2)
                    if d < min_d:
                        min_d = d
                        enemy = e1
                if enemy != None:
                    angle = math.atan2(t1.y - enemy.y - 30, t1.x - enemy.x - 30)
                    bx = -5 * math.cos(angle)
                    by = -5 * math.sin(angle)
                    bullet = Bullet([t1.x, t1.y], [bx, by])
                    bullets.append(bullet)
                self.reload = 0
            self.reload = self.reload + 1

        def draw(self):
            screen.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

        def hitTest(self, x, y):
            if x > self.x - self.width / 2 and x < self.x + self.width / 2 and y > self.y - self.height / 2 and y < self.y + self.height / 2:
                return True
            else:
                return False

    class Turret2: 
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.cost = 500
            self.image = pygame.image.load("res/towerimg2.gif")
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.reload = 0

        def shoot(self):
            if self.reload > 15 and len(enemies1) > 0:
                min_d = 150  
                enemy = None
                for e1 in enemies1:
                    d = math.sqrt((t2.x - e1.x - 15) ** 2 + (t2.y - e1.y - 15) ** 2)
                    if d < min_d:
                        min_d = d
                        enemy = e1
                if enemy != None:
                    laser = Laser([self.x, self.y], [enemy.x + 15, enemy.y + 15])
                    lasers.append(laser)
                self.reload = 0
            self.reload = self.reload + 1

        def draw(self):
            screen.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

        def hitTest(self, x, y):
            if x > self.x - self.width / 2 and x < self.x + self.width / 2 and y > self.y - self.height / 2 and y < self.y + self.height / 2:
                return True
            else:
                return False

    class Turret3:  
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.cost = 1000
            self.image = pygame.image.load("res/towerimg3.gif")
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        def draw(self):
            screen.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

        def hitTest(self, x, y):
            if x > self.x - self.width / 2 and x < self.x + self.width / 2 and y > self.y - self.height / 2 and y < self.y + self.height / 2:
                return True
            else:
                return False

    class Enemy1:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.image = pygame.image.load("res/alien.gif")
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.xspeed = -spd
            self.yspeed = 0
            self.health = hlth

        def draw(self):
            screen.blit(self.image, (self.x, self.y))
            for x in range(0, self.health):
                rct = pygame.Rect(self.x - healthspacing + x * 1, self.y - 5, 3, 4)
                pygame.draw.rect(screen, green, rct, 0)

        def move(self):
            rect = self.image.get_rect()
            rect.left = self.x
            rect.top = self.y
            if rect.colliderect(barrierleftrect):
                self.xspeed = -spd
                self.yspeed = 0
            if rect.colliderect(barrierrightrect):
                self.xspeed = spd
                self.yspeed = 0
            if rect.colliderect(barrierdownrect) or rect.colliderect(barrierdownrect2):
                self.xspeed = 0
                self.yspeed = spd
            self.x += self.xspeed
            self.y += self.yspeed

        def hitTest(self, x, y):
            if x > self.x - 25 and x < self.x + self.width + 25 and y > self.y - 25 and y < self.y + self.height + 25:
                return True
            else:
                return False

    class Bullet: 
        def __init__(self, pos, speed):
            self.x = pos[0]
            self.y = pos[1]
            self.width = 5
            self.height = 5
            self.pos = pos
            self.speed = speed

        def move(self):
            self.pos[0] = int(self.pos[0] + self.speed[0])
            self.pos[1] = int(self.pos[1] + self.speed[1])
            self.x = self.pos[0]
            self.y = self.pos[1]

        def draw(self):
            pygame.draw.circle(screen, blue, self.pos, 10, 3)

        def hitTest(self, x, y):
            if x > self.x - self.width / 2 and x < self.x + self.width / 2 and y > self.y - self.height / 2 and y < self.y + self.height / 2:
                return True
            else:
                return False

    class Laser: 
        def __init__(self, start, end):
            self.start = start
            self.end = end

        def draw(self):
            pygame.draw.line(screen, red, self.start, self.end, 2)

    tower1 = pygame.image.load("res/towerimg1.gif")
    tower2 = pygame.image.load("res/towerimg2.gif")
    tower3 = pygame.image.load("res/towerimg3.gif")
    backround = pygame.image.load("res/tronbg.gif")


    barrierleftrect = pygame.Rect(978, 524, 150, 50)  
    barrierrightrect = pygame.Rect(220, 360, 50, 50)
    barrierdownrect = pygame.Rect(185, 150, 50, 50)
    barrierdownrect2 = pygame.Rect(1045, 320, 1000, 50)

    trackrect1 = pygame.Rect(229, 159, 1030, 40)  
    trackrect2 = pygame.Rect(229, 170, 40, 175)
    trackrect3 = pygame.Rect(229, 328, 822, 40)
    trackrect4 = pygame.Rect(1010, 330, 40, 199)
    trackrect5 = pygame.Rect(0, 489, 1030, 40)
    menurect1 = pygame.Rect(230, 0, 824, 200)
    menurect2 = pygame.Rect(0, 0, 1280, 57)
    menurect3 = pygame.Rect(175, 75, 935, 15)
    menurect4 = pygame.Rect(230, 583, 824, 200)
    menurect5 = pygame.Rect(0, 663, 1280, 57)
    menurect6 = pygame.Rect(175, 625, 935, 150)

    while True:
        xpos = xpos + xspeed 
        ypos = ypos + yspeed
        screen.blit(backround, [0, 0, 0, 0])
        mx, my = pygame.mouse.get_pos()
        mouserect = pygame.Rect(mx - 25, my - 25, 50, 50) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_1]:  
            icon = 1
            click = 0
        if keys[pygame.K_2]:
            icon = 2
            click = 0
        if keys[pygame.K_3]:
            icon = 3
            click = 0
        if keys[pygame.K_d]:
            click = 0
            icon = 0

        if pygame.mouse.get_pressed()[0]:
            if click == 0:
                if icon == 1 and money >= 300 and place == 0:  
                    t1 = Turret(mx, my)
                    turrets1.append(t1)
                    money = money - 300
                if icon == 2 and money >= 500 and place == 0:
                    t2 = Turret2(mx, my)
                    turrets2.append(t2)
                    money = money - 500
                click = 1

                if icon == 3 and money >= 1000 and place == 0:
                    t3 = Turret3(mx, my)
                    turrets3.append(t3)
                    money = money - 1000
                click = 1

        if mouserect.colliderect(trackrect1) or mouserect.colliderect(trackrect2) or mouserect.colliderect(
                trackrect3) or mouserect.colliderect(trackrect4) or mouserect.colliderect(
                trackrect5) or mouserect.colliderect(menurect1) or mouserect.colliderect(
                menurect2) or mouserect.colliderect(menurect3) or mouserect.colliderect(
                menurect4) or mouserect.colliderect(menurect5) or mouserect.colliderect(menurect6):
            place = 1
        else:
            place = 0

        for t1 in turrets1:  
            if t1.hitTest(mx, my):
                place = 1

        for t2 in turrets2:
            if t2.hitTest(mx, my):
                place = 1

        for t3 in turrets3:
            if t3.hitTest(mx, my):
                place = 1

        if pygame.mouse.get_pressed()[
            2]: 
            for t1 in turrets1:
                if t1.hitTest(mx, my):
                    money = money + 200
                    turrets1.remove(t1)

        if pygame.mouse.get_pressed()[2]:
            for t2 in turrets2:
                if t2.hitTest(mx, my):
                    money = money + 350
                    turrets2.remove(t2)

        if pygame.mouse.get_pressed()[2]:
            for t3 in turrets3:
                if t3.hitTest(mx, my):
                    money = money + 750
                    turrets3.remove(t3)

        if click != 1 and icon == 1:  
            screen.blit(tower1, (mx - 25, my - 25))
            renderedText = font1.render("Дракон", 1, white)
            screen.blit(renderedText, (545, 600))
            renderedText = font1.render("Натисни 'D' щоб відхилити", 1, white)
            screen.blit(renderedText, (500, 90))
            renderedText = font1.render("Ціна: $300           Відстань: Велика         Шкода: Мала", 1, white)
            screen.blit(renderedText, (250, 640))
            renderedText = font1.render("Наносить групову шкоду, але спрацьовує повільно й часто промахується", 1, white)
            screen.blit(renderedText, (220, 680))
            if place == 0:
                pygame.draw.circle(screen, green, [mx, my], 300,
                                   1)
            if place == 1 or money < 300:
                pygame.draw.circle(screen, red, [mx, my], 300,
                                   1) 

        if click != 1 and icon == 2:
            screen.blit(tower2, (mx - 25, my - 25))
            renderedText = font1.render("Натисни 'D' щоб відхилити", 1, white)
            screen.blit(renderedText, (500, 90))
            renderedText = font1.render("Рицар", 1, white)
            screen.blit(renderedText, (545, 600))
            renderedText = font1.render("Ціна: $500           Відстань: Мала           Шкода: Велика", 1, white)
            screen.blit(renderedText, (250, 640))
            renderedText = font1.render("Ніколи не промахується і швидко атакує", 1, white)
            screen.blit(renderedText, (400, 680))
            if place == 0:
                pygame.draw.circle(screen, green, [mx, my], 150, 1)
            if place == 1 or money < 500:
                pygame.draw.circle(screen, red, [mx, my], 150, 1)

        if click != 1 and icon == 3:
            screen.blit(tower3, (mx - 25, my - 25))
            renderedText = font1.render("Натисни 'D' щоб відхилити", 1, white)
            screen.blit(renderedText, (500, 90))
            renderedText = font1.render("Магічний грошовий портал", 1, white)
            screen.blit(renderedText, (558, 600))
            renderedText = font1.render("Ціна: $1000           Вдістань: Немає           Шкода: Немає", 1, white)
            screen.blit(renderedText, (235, 640))
            renderedText = font1.render("Виробляє $75 кожні 5 секунд", 1, white)
            screen.blit(renderedText, (400, 680))
            if place == 0:
                pygame.draw.circle(screen, green, [mx, my], 75, 1)
            if place == 1 or money <= 999:
                pygame.draw.circle(screen, red, [mx, my], 75, 1)

        for e1 in enemies1:
            for b in bullets:
                if e1.hitTest(b.x, b.y) or e1.hitTest(b.x + b.width, b.y) or e1.hitTest(b.x,
                                                                                        b.y + b.height) or e1.hitTest(
                        b.x + b.width, b.y + b.height):
                    e1.health = e1.health - 1
                    break

        for e1 in enemies1:
            for l in lasers:
                if e1.hitTest(l.end[0], l.end[1]) or e1.hitTest(l.end[0], l.end[1]) or e1.hitTest(l.end[0], l.end[
                    1]) or e1.hitTest(l.end[0], l.end[1]):
                    e1.health = e1.health - 2
                    lasers.remove(l)
                    break

        for e1 in enemies1: 
            if e1.x < -30:
                enemies1.remove(e1)
                lives = lives - 1

        for t1 in turrets1:
            t1.shoot()
            t1.draw()

        for t2 in turrets2:
            t2.shoot()
            t2.draw()

        for t3 in turrets3:
            t3.draw()

        for b in bullets:
            b.draw()
            b.move()
            if b.pos[0] < 0 or b.pos[0] > width or b.pos[1] < 0 or b.pos[
                1] > height: 
                bullets.remove(b)

        for l in lasers:
            l.draw()

        if producecount >= 500: 
            for t3 in turrets3:
                money = money + 75
            producecount = 0

        for e1 in enemies1:
            if e1.health <= 0: 
                enemies1.remove(e1)
                money = money + 2
            e1.draw()
            e1.move()

        if enemycount % alienspacing == 0 and spawncount < numaliens:
            e1 = Enemy1(1300, 162)
            enemies1.append(e1)
            spawncount = spawncount + 1  
            empty = 0

        if len(enemies1) <= 0 and empty == 0:  
            hlth = hlth + 4  
            healthspacing = healthspacing + 2  
            money = money + 250  
            spawncount = 0
            if numaliens < 65:  
                numaliens = numaliens * 1.5
            if alienspacing > 5:  
                alienspacing = alienspacing - 1
            if spd < 10:
                spd = spd + 1 
            empty = 1  
            wave = wave + 1  

        if enemycount >= 100:  
            enemycount = 0

        if lives <= 0:  
            lose(wave)

        enemycount = enemycount + 1
        producecount = producecount + 1

        renderedText = font1.render("$" + str(money), 1, white, ) 
        screen.blit(renderedText, (10, 10))
        renderedText = font1.render("Життя: " + str(lives), 1, white, ) 
        screen.blit(renderedText, (1100, 10))
        renderedText = font1.render("Хвилі: " + str(wave), 1, white, ) 
        screen.blit(renderedText, (600, 10))
        pygame.display.flip()
        pygame.time.delay(10)  

def start():
    startrect = pygame.Rect(550, 250, 200, 50)  
    howrect = pygame.Rect(455, 350, 400, 50)
    quitrect = pygame.Rect(565, 450, 180, 50)
    backround = pygame.image.load("res/start.gif")
    ##    pygame.mixer.music.load('gamemusic.wav') 
    ##    pygame.mixer.music.play(-1)
    while True:
        screen.blit(backround, [0, 0, 0, 0])
        mx, my = pygame.mouse.get_pos()
        mouserect = pygame.Rect(mx - 15, my - 15, 30, 30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE]:
            game()

        renderedText = font2.render("Володар Ночі", 1, white)
        screen.blit(renderedText, (10, 50))

        if mouserect.colliderect(
                startrect):
            renderedText = font3.render(">Почати", 1, orange)
            screen.blit(renderedText, (550, 250))
            if pygame.mouse.get_pressed()[0]:
                game()
        else:
            renderedText = font3.render("Почати", 1, white)
            screen.blit(renderedText, (550, 250))

        if mouserect.colliderect(howrect):
            renderedText = font3.render(">Як грати", 1, orange)
            screen.blit(renderedText, (500, 350))
            if pygame.mouse.get_pressed()[0]:
                howtoplay()
        else:
            renderedText = font3.render("Як грати", 1, white)
            screen.blit(renderedText, (550, 350))

        if mouserect.colliderect(quitrect):
            renderedText = font3.render(">Вийти", 1, orange)
            screen.blit(renderedText, (565, 450))
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()
        else:
            renderedText = font3.render("Вийти", 1, white)
            screen.blit(renderedText, (565, 450))

        pygame.display.flip()

def howtoplay():
    backround = pygame.image.load("res/how-to-play.gif")
    while True:
        screen.blit(backround, [0, 0, 0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE]:
            start()
        pygame.display.flip()


def lose(wave):
    backround = pygame.image.load("res/start.gif")
    while True:
        screen.blit(backround, [0, 0, 0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE]:
            game()
        renderedText = font5.render("ТИ ПРОЖИВ: " + str(wave) + " ХВИЛЬ", 1, red, )
        screen.blit(renderedText, (125, 50))
        renderedText = font4.render("SPACE Щоб показати хто босс підземелья", 1, red)
        screen.blit(renderedText, (19, 350))
        pygame.display.flip()


start()
