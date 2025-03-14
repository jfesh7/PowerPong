#Game data for PowerPong

import sys, os
import math
import random
import pygame
from utils import *

#string constants

BIG = "big"
SMALL = "small"
CATCH = "catch"
OBSTACLE = "obstacle"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
PLAYER = "player"
COMPUTER = "computer"
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

#All movement in this game is done by floating point addition.
#In order to do this, the rect is not moved directly.
#It is moved indirectly by a position coordinate.

class Paddle(pygame.sprite.Sprite):
    control = PLAYER
    upKey = 0
    downKey = 0
    speed = 5.0
    power = None
    small_image = None
    big_image = None
    p = 0
    difficulty = 0

    def __init__(self, side, paddletype):
        pygame.sprite.Sprite.__init__(self)
        self.area = pygame.display.get_surface().get_rect()
        self.image = load_png(paddletype + ".png")
        self.o_image = self.image
        self.rect = self.image.get_rect()
        self.side = side
        self.score = 0
        self.reset()

    def reset(self):
        self.score = 0
        self.reset_power()
        self.rect.centery = self.area.centery
        if self.side == 1:
            self.rect.left = self.area.left
        else:
            self.rect.right = self.area.right
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.top = self.rect.top

    def reset_power(self):
        self.power = None
        self.image = self.o_image
        if self.side == 1:
            self.rect = self.image.get_rect(midleft=self.rect.midleft)
        else:
            self.rect = self.image.get_rect(midright=self.rect.midright)
        self.p = 0
        self.top = self.rect.top

    def new_launch(self): #virtual method that is defined in derived AI class
        pass

    def aim(self, opponent):
        pass

    def update_power(self):
        self.p += 1
        if self.p % 60 == 0:
            self.powertime -= 1
            if self.powertime == 0:
                self.reset_power()

    def update(self, ball=0): #ball argument is a virtual argument included for derived AI
        keyboard = pygame.key.get_pressed()
        if keyboard[self.upKey]:
            self.moveup()
        if keyboard[self.downKey]:
            self.movedown()
        if self.power:
            self.update_power()

    def moveup(self):
        self.top -= self.speed
        newpos = self.image.get_rect(top=self.top, left=self.rect.left)
        if newpos.top < self.area.top:
            newpos.top = self.area.top
            self.top = newpos.top
        self.rect = newpos

    def movedown(self):
        self.top += self.speed
        newpos = self.image.get_rect(top=self.top, left=self.rect.left)
        if newpos.bottom > self.area.bottom:
            newpos.bottom = self.area.bottom
            self.top = newpos.top
        self.rect = newpos

    def powerup(self, powerup):
        if powerup.power == OBSTACLE:
            Obstacle()
            return
        self.reset_power()
        if powerup.power == BIG:
            self.grow()
        if powerup.power == SMALL:
            self.shrink()
        if powerup.power == CATCH:
            self.catch()

    def save_pos(self):
        if self.side == 1:
            midleft = self.rect.midleft
            self.rect = self.image.get_rect(midleft=midleft)
            self.top = self.rect.top
        else:
            midright = self.rect.midright
            self.rect = self.image.get_rect(midright=midright)
            self.top = self.rect.top

    def grow(self):
        self.power = BIG
        if self.big_image:
            self.image = self.big_image
        else:
            self.image = pygame.transform.scale2x(self.image)
        self.save_pos()
        self.powertime = 15

    def shrink(self):
        self.power = SMALL
        x = round(self.rect.width*0.75)
        y = round(self.rect.height*0.5)
        if self.small_image:
            self.image = self.small_image
        else:
            self.image = pygame.transform.smoothscale(self.image, (x, y))
        self.save_pos()
        self.powertime = 15

    def catch(self):
        self.power = CATCH
        self.powertime = 15

class AIPaddle(Paddle):
    control = COMPUTER
    max_range = 500
    direction = UP
    distance = 0
    move = 0
    difficulty = MEDIUM
    
    def __init__(self, side, paddletype):
        Paddle.__init__(self, side, paddletype)
        self.reset()

    def reset(self):
        Paddle.reset(self)
        self.range = self.max_range
        self.new_direction()
        self.move = 0

    def new_launch(self):
        self.new_direction()
        self.move = 0
        self.distance = random.randint(0, self.area.height//2)
        self.range = self.max_range

    def new_direction(self):
        self.direction = random.choice([UP, DOWN])

    def new_range(self):
        self.range = random.randint(150, self.max_range)

    def in_range(self, ball):
        return ball.rect.centerx > (self.area.right - self.range)

    def block(self):
        self.range = self.max_range
        self.rect.centery = self.area.centery
        self.top = self.rect.top

    def aim(self, opponent):
        if opponent.rect.centery > self.area.centery:
            self.direction = UP
        if opponent.rect.centery < self.area.centery:
            self.direction = DOWN

    def catch(self):
        Paddle.catch(self)
        self.new_launch()

    def update(self, ball):
        if self.in_range(ball):
            if ball.launched:
                if ball.rect.centery < self.rect.centery:
                    self.moveup()
                if ball.rect.centery > self.rect.centery:
                    self.movedown()
            else:
                if self.move < self.distance:
                    self.move += self.speed
                    if self.direction == UP:
                        self.moveup()
                    elif self.direction == DOWN:
                        self.movedown()
                elif ball.side == self.side:
                    ball.launched = True
                    
        if self.power:
            self.update_power()

class Ball(pygame.sprite.Sprite):
    speed = 7.0
    directionAngle = -(math.pi/6)
    vel = pygame.math.Vector2(0, 0)
    launched = False
    side = 1
    wall_sound = fake_sound()
    bounce_sound = fake_sound()
    score_sound = fake_sound()
    collect_sound = fake_sound()
    SOUND = True
    rotating = False #Ball rotates when true
    rotationAngle = 0.0
    rotationRate = 10.0

    def __init__(self, balltype, speed=7.0):
        pygame.sprite.Sprite.__init__(self)
        self.area = pygame.display.get_surface().get_rect()
        self.o_image = load_png(balltype + '.png')
        self.image = self.o_image
        self.reset()

    def reset(self):
        self.rect = self.image.get_rect(center=self.area.center)
        self.topleft = self.rect.topleft
        self.setVel()

    def setVel(self):
        self.vel.x = self.speed * math.cos(self.directionAngle)
        self.vel.y = -self.speed * math.sin(self.directionAngle)

    def newPos(self):
        self.topleft = (self.topleft[0]+self.vel.x, self.topleft[1]+self.vel.y)
        return self.image.get_rect(topleft=self.topleft)

    def rotate(self):
        center = self.rect.center
        if self.vel.x > 0: #Moving right
            self.rotationAngle -= self.rotationRate
        else:
            self.rotationAngle += self.rotationRate
        if self.rotationAngle >= 360:
            self.rotationAngle = 0.0
        self.image = pygame.transform.rotate(self.o_image, self.rotationAngle)
        self.rect = self.image.get_rect(center=center)
            
    def paddleBounce(self, displacement):
        self.play_bounce_sound()
        self.directionAngle = math.pi - self.directionAngle
        deltaAngle = math.radians(random.randint(0, 19))
        if displacement == UP:
            if abs(math.cos(self.directionAngle - deltaAngle)) > 0.7:
                self.directionAngle -= deltaAngle
        elif displacement == DOWN:
            if abs(math.cos(self.directionAngle + deltaAngle)) > 0.7:
                self.directionAngle += deltaAngle

    def score(self, scorer, blocker):
        self.play_score_sound()
        scorer.score += 1
        self.launched = False
        self.side = blocker.side
        if scorer.control == COMPUTER:
            scorer.block()
        if blocker.control == COMPUTER:
            blocker.new_launch()
            if blocker.difficulty in [MEDIUM, HARD]:
                if abs(math.cos(self.directionAngle)) > 0.9: #If ball is moving horizontally enough, aim launch at a gap on other players side
                    blocker.aim(scorer)

    def bounce(self, obstacle, newpos): #Bounce off obstacles
        self.play_bounce_sound()
        if newpos.centerx < obstacle.left:
            if self.vel.x > 0: #Heading right
                self.directionAngle = math.pi-self.directionAngle #Deflect angle horizontally
            else: #Not heading the proper direction for bounce
                self.directionAngle = -self.directionAngle
        elif newpos.centerx > obstacle.right:
            if self.vel.x < 0: #Heading left
                self.directionAngle = math.pi-self.directionAngle
            else: #Not heading the proper direction for bounce
                self.directionAngle = -self.directionAngle
        else: #Vertical bounce
            if newpos.centery < obstacle.centery: #colliding at top of obstacle
                if self.vel.y > 0:
                    self.directionAngle = -self.directionAngle
                else:
                    self.directionAngle = math.pi-self.directionAngle
            elif newpos.centery > obstacle.centery: #bottom
                if self.vel.y < 0:
                    self.directionAngle = -self.directionAngle
                else:
                    self.directionAngle = math.pi-self.directionAngle

    def play_wall_sound(self):
        if self.SOUND:
            self.wall_sound.play(0, 1000)

    def play_bounce_sound(self):
        if self.SOUND:
            self.bounce_sound.play(0, 1000)

    def play_score_sound(self):
        if self.SOUND:
            self.score_sound.play(0, 1000)

    def play_collect_sound(self):
        if self.SOUND:
            self.collect_sound.play(0, 1000)

    def update(self, paddle1, paddle2, powerup, obstacles):
        if self.launched: #If ball is currently launched, move it
            newpos = self.newPos()

            #Bounce off ceiling and set bounds
            if newpos.top < self.area.top:
                newpos.top = self.area.top
                self.play_wall_sound()
                self.directionAngle = -self.directionAngle
            if newpos.bottom > self.area.bottom:
                newpos.bottom = self.area.bottom
                self.play_wall_sound()
                self.directionAngle = -self.directionAngle
            if newpos.left < self.area.left: #Player2 scores
                self.score(paddle2, paddle1)
                newpos.left = self.area.left
                self.directionAngle = math.pi - self.directionAngle
            if newpos.right > self.area.right: #Player1 scores
                self.score(paddle1, paddle2)
                newpos.right = self.area.right
                self.directionAngle = math.pi - self.directionAngle

            if newpos.colliderect(paddle1.rect): #Collision with paddle1
                newpos.left = paddle1.rect.right
                self.last_hit = paddle1
                if paddle1.power == CATCH:
                    self.launched = False
                    self.side = paddle1.side
                if newpos.centery > paddle1.rect.centery:
                    self.paddleBounce(DOWN)
                else:
                    self.paddleBounce(UP)

            if newpos.colliderect(paddle2.rect): #Collision with paddle2
                if paddle2.control == COMPUTER:
                    paddle2.new_range()
                newpos.right = paddle2.rect.left
                self.last_hit = paddle2
                if paddle2.power == CATCH:
                    paddle2.new_launch()
                    if paddle2.difficulty in [MEDIUM, HARD]:
                        if abs(math.cos(self.directionAngle)) > 0.9:
                            paddle2.aim(paddle1)
                    self.launched = False
                    self.side = paddle2.side
                if newpos.centery > paddle2.rect.centery:
                    self.paddleBounce(DOWN)
                else:
                    self.paddleBounce(UP)

            #Bounce off obstacles, if any
            for obstacle in obstacles:
                if obstacle.active:
                    if newpos.colliderect(obstacle.rect):
                        self.bounce(obstacle.rect, newpos)

            #Collect any powerups that are collided with
            power = pygame.sprite.spritecollide(self, powerup, 1)
            if power:
                self.play_collect_sound()
                #if power[0].SOUND:
                #    power[0].sound.play()
                PowerUpText(power[0].power, power[0].rect.center)
                self.last_hit.powerup(power[0]) #Award powerup to last player to hit ball

            #Give ball new position and velocity
            self.setVel()
            self.rect = newpos
            if self.rotating:
                self.rotate()
            self.topleft = self.rect.topleft

        else: #If ball is not launched, move with current paddle
            if self.side == paddle1.side:
                self.rect.centery = paddle1.rect.centery
                self.rect.left = paddle1.rect.right
                self.last_hit = paddle1
            else:
                self.rect.centery = paddle2.rect.centery
                self.rect.right = paddle2.rect.left
                self.last_hit = paddle2
            self.topleft = self.rect.topleft

class PowerUp(pygame.sprite.Sprite):
    containers = []
    ttl = 20 #Time that powerup lasts
    SOUND = True
    style = ''

    def __init__(self, power, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.power = power
        #self.sound = load_sound(power + '.wav')
        self.image = load_png(self.style + '_' + power + ".png")
        self.rect = self.image.get_rect(center=pos)
        self.i = 0

    def update(self):
        self.i += 1
        if self.i % 60 == 0:
            self.ttl -= 1
        if self.ttl < 0:
            self.kill()

class Obstacle(pygame.sprite.Sprite): #An obstacle that either moves or stays
    containers = []
    ttl = 15
    moving = False #Controls whether object moves or stays
    active = False
    obstacletype = 0
    speed = 2

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.area = pygame.display.get_surface().get_rect()
        self.moving = random.choice([True, False])
        self.o_image = load_png(self.obstacletype + '.png')
        x = random.randint(self.area.centerx-75, self.area.centerx+75)
        y = random.randint(self.o_image.get_height(), self.area.bottom-self.o_image.get_height())
        self.rect = self.o_image.get_rect(center=(x, y))
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((0, 0, 0))
        self.image.fill((255, 255, 255), (1, 1, self.rect.width-2, self.rect.height-2))
        self.i = 0

    def update(self):
        self.i += 1
        if not self.active: #Display rectangle where obstacle will appear
            if self.i % 60 == 0:
                self.active = True
                self.image = self.o_image
        if self.i % 60 == 0 and self.active:
            self.ttl -= 1
        if self.ttl == 0:
            self.kill()
        if self.moving and self.active:
            newpos = self.rect.move(0, self.speed)
            if newpos.top < self.area.top or newpos.bottom > self.area.bottom:
                self.speed = -self.speed
            self.rect = newpos

class PowerUpText(pygame.sprite.Sprite): #Flashing text that accompanies power collection
    font = None
    containers = []
    ttl = 2

    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.text = text
        self.image = self.font.render(text, 1, (255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.t = 0

    def update(self):
        self.t += 1
        if self.t % 60 == 0:
            self.ttl -= 1
            if self.ttl == 0:
                self.kill()

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        self.image = self.font.render(self.text, 1, (r, g, b))

class MenuItem(pygame.sprite.Sprite): #A simple menu selection made using a font
    font = None
    FGCOLOR = (255, 255, 255)
    BGCOLOR = (0, 0, 0)
    ACTIVEFGCOLOR = (0, 0, 0)
    ACTIVEBGCOLOR = (255, 255, 255)
    selected = True
    top = 0
    left = 0
    right = 0

    def __init__(self, text, top, left=0, right=0, font=None):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        if font:
            self.font = font
        self.image = self.font.render(self.text, 1, self.FGCOLOR, self.BGCOLOR)
        self.rect = self.image.get_rect(top=top)
        self.top = top
        self.rect.centerx = pygame.display.get_surface().get_rect().centerx
        if left:
            self.left = left
            self.rect.left = left
        elif right:
            self.right = right
            self.rect.right = right

    def update(self):
        self.selected = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.selected = True
        if self.selected:
            self.image = self.font.render(self.text, 1, self.ACTIVEFGCOLOR, self.ACTIVEBGCOLOR)
        else:
            self.image = self.font.render(self.text, 1, self.FGCOLOR, self.BGCOLOR)
        self.rect = self.image.get_rect(top=self.top)
        if self.left:
            self.rect.left = self.left
        elif self.right:
            self.rect.right = self.right
        else:
            self.rect.centerx = pygame.display.get_surface().get_rect().centerx

    def command(self): #Command assignment is optional, and is assigned outside the class
        pass

class ControlOption(MenuItem): #An option used in my change controls menu
    control = 0
    changing = False
    def __init__(self, text, top, left=0, right=0, font=None, control=0):
        MenuItem.__init__(self, text, top, left, right, font)
        self.control = control
        self.image = self.font.render(self.text + pygame.key.name(self.control), 1, self.FGCOLOR, self.BGCOLOR)
        self.rect = self.image.get_rect(top=top)

    def update(self):
        self.selected = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.selected = True
        if self.changing:
            text = self.text + "Press a Key..."
        else:
            text = self.text + pygame.key.name(self.control)
        if self.selected:
            self.image = self.font.render(text, 1, self.ACTIVEFGCOLOR, self.ACTIVEBGCOLOR)
        else:
            self.image = self.font.render(text, 1, self.FGCOLOR, self.BGCOLOR)
        self.rect = self.image.get_rect(top=self.top)
        if self.left:
            self.rect.left = self.left
        elif self.right:
            self.rect.right = self.right
        else:
            self.rect.centerx = pygame.display.get_surface().get_rect().centerx
