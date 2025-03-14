#!/usr/bin/python3
###########################################################
# Name: PowerPong
# Developer: Josiah Fesh
# Version: 0.9.8
# Description: A pong game with powerups and themes
###########################################################
"""
PowerPong is pong clone written in Python using the Pygame1.9 graphics library.
"""

HELP = """
Defend your goal!
Score against the opponent!

Default Controls:
    1 Player Game:
        move up - up
        move down - down
        launch ball - space
    2 Player Game:
        p1 move up - a
        p1 move down - z
        p1 launch ball - enter
        p2 move up - up
        p2 move down - down
        p2 launch ball - space
    
Powerups:
    [O] - New obstacle will spawn.
    [B] - Paddle grows
    [S] - Paddle shrinks
    [C] - Paddle can catch and launch ball.
    Powerups only last about 15 seconds.

Game Modes:
    SinglePlayer:
        Easy, Medium, Hard
    MultiPlayer:
        Normal, Fast, Fastest

Settings:
    Theme - Change current game theme
    Sound - Toggle game soundFx on/off
    Music - Toggle game Music on/off
    Score - Set the winning score for game
    Controls - Change game controls"""

INFO = """

Developer:
Josiah Fesh

Graphics and Design:
Josiah Fesh
James Fesh

Sound Effects borrowed from various sources.

Special Thanks:
James Fesh - Modern Dark and Light themes
James Fesh - Sound and Music

Written in Python3.x.
This game uses the Pygame1.9 graphics library.

Executable made with CxFreeze.
Install package compiled with Inno Setup 5.

Thanks for Playing!"""

import sys, os
import pygame
#import pygame._view
import math
import random
from data import *
from utils import *

pygame.init()

if not pygame.mixer: print("Warning, sound disabled.")
if not pygame.font: print("Warning, fonts disabled.")

BLACK = pygame.Color(0, 0, 0)
DARK = pygame.Color(53, 64, 79)
WHITE = pygame.Color(255, 255, 255)
WHITE2 = pygame.Color(250, 250, 250)
GREEN = pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)
LEGORED = pygame.Color(80, 0, 0)
DARKGREEN = pygame.Color(0, 150, 0)
BLUE = pygame.Color(0, 0, 255)
COLDBLUE = pygame.Color(0, 150, 255)
SILVER = pygame.Color(235, 235, 235)
GRAY = pygame.Color(200, 200, 200)
DARKGRAY = pygame.Color(150, 150, 150)
BIG = "big"
SMALL = "small"
CATCH = "catch"
OBSTACLE = "obstacle"
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"
CONTINUE = "Continue"
QUIT = "Quit"
AGAIN = "Play Again"
MENU = "Menu"
ON = "On"
OFF = "Off"
POWERFONT = pygame.font.Font("sansation.ttf", 25)
POWERFONTBIG = pygame.font.Font("sansation.ttf", 45)
POWERFONTSMALL = pygame.font.Font("sansation.ttf", 15)

class Game:
    FPS = 60
    BGCOLOR = BLACK
    FGCOLOR = WHITE
    RESERVED = [pygame.K_p, pygame.K_ESCAPE]
    PLAYER1UP = pygame.K_UP
    PLAYER1DOWN = pygame.K_DOWN
    PLAYER1UP2 = pygame.K_a #For a 2 player game
    PLAYER1DOWN2 = pygame.K_z
    PLAYER2UP = pygame.K_UP
    PLAYER2DOWN = pygame.K_DOWN
    P1LAUNCHKEY = pygame.K_SPACE
    P2LAUNCHKEY = pygame.K_RETURN
    splash_image = "splash1.gif"
    score = load_sound("score.wav")
    paddle = load_sound("paddle.wav")
    wall = load_sound("wall.wav")
    powerup = load_sound("powerup.wav")
    winnerSound = load_sound("winner.wav")
    menuclick = load_sound("menuclick.wav")
    normalMusic = os.path.join("sound", "music", "music.mp3")
    alternateMusic = os.path.join("sound", "music", "alternate.mp3")
    NORMAL = {'name':'Normal', 'ball':'power', 'p1':'green', 'p2':'yellow', 'bg':'normal',
              'obstacle':'normal_o', 'powerupstyle':'classic', 'sounds':{'score':score, 'paddle':paddle, 'wall':wall, 'collect':powerup},
              'music':normalMusic, 'font':{'fg':WHITE, 'bg':BLACK}}
    INVERTED = {'name':'Inverted', 'ball':'inverted', 'p1':'red', 'p2':'blue', 'bg':'invertedbg',
                'obstacle':'inverted_o', 'powerupstyle':'inverted', 'sounds':{'score':score, 'paddle':paddle, 'wall':wall, 'collect':powerup},
                'music':normalMusic, 'font':{'fg':BLACK, 'bg':WHITE}}
    MOD_DARK = {'name':'Modern-Dark', 'ball':'md_ball', 'p1':'md_left', 'p2':'md_right', 'bg':'md_background',
                'obstacle':'md_o', 'powerupstyle':'md', 'sounds':{'score':score, 'paddle':paddle, 'wall':wall, 'collect':powerup},
                'music':normalMusic, 'font':{'fg':WHITE2, 'bg':DARK}}
    MOD_LIGHT = {'name':'Modern-Light', 'ball':'ml_ball', 'p1':'ml_left', 'p2':'ml_right', 'bg':'ml_background',
                 'obstacle':'ml_o', 'powerupstyle':'ml', 'sounds':{'score':score, 'paddle':paddle, 'wall':wall, 'collect':powerup},
                 'music':normalMusic, 'font':{'fg':DARK, 'bg':WHITE2}}
    #SNOW = {'name':'Snow', 'ball':'snow', 'p1':'icepaddle', 'p2':'icepaddle', 'bg':'snowbg',
    #        'obstacle':'snow_o', 'powerupstyle':'classic', 'sounds':{'score':score, 'paddle':paddle, 'wall':wall, 'spawn':pop, 'collect':powerup},
    #        'music':None, 'font':{'fg':WHITE, 'bg':COLDBLUE}}
    #LEGO = {'name':'Lego', 'ball':'lego', 'p1':'legopaddle1', 'p2':'legopaddle2', 'bg':'legobg',
    #        'obstacle':'lego_o', 'powerupstyle':'classic', 'sounds':{'score':legoscore, 'paddle':paddle, 'wall':wall, 'spawn':pop, 'collect':legopowerup},
    #        'music':None, 'font':{'fg':WHITE, 'bg':DARKGREEN}}
    COMPUTER = False
    SOUND = True
    MUSIC = True
    NORMALBALL = 7.0
    FASTBALL = 7.6
    FASTESTBALL = 8.2
    EASYAI = {'speed':5, 'ballspeed':NORMALBALL, 'range':500, 'difficulty':EASY}
    MEDIUMAI = {'speed':5.3, 'ballspeed':FASTBALL, 'range':550, 'difficulty':MEDIUM}
    HARDAI = {'speed':5.6, 'ballspeed':FASTESTBALL, 'range':700, 'difficulty':HARD}
    gameFont = pygame.font.Font("sansation.ttf", 25)
    endscore = 5
    MAX_POWERUPS = 3
    chance_init = 1000
    chance = chance_init
    themes = [NORMAL, INVERTED, MOD_DARK, MOD_LIGHT]
    theme = NORMAL
    def __init__(self, title):
        self.screen = pygame.display.set_mode((650, 500))
        pygame.display.set_caption(title)
        self.icon = load_png("icon.ico")
        pygame.display.set_icon(self.icon)
        self.splash_image = load_png(self.splash_image)
        self.clock = pygame.time.Clock()
        self.show_splash()
        self.clickSound = self.menuclick
        self.setup_theme(self.theme) #Setup theme data

    def show_splash(self):
        self.screen.fill(BLACK)
        splash_image = self.splash_image
        rect = self.splash_image.get_rect(center=self.screen.get_rect().center)
        i = 0
        seconds = 0
        while 1:
            i += 1
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            if i % self.FPS == 0:
                seconds += 1
                if seconds > 1:
                    return

            self.screen.fill(BLACK)
            self.screen.blit(splash_image, rect)
            pygame.display.flip()

    def setup_theme(self, theme): #Change game style to current theme
        self.theme = theme
        self.bg = load_png(theme['bg'] + '.png')
        PowerUp.style = theme['powerupstyle']
        self.FGCOLOR = theme['font']['fg']
        self.BGCOLOR = theme['font']['bg']
        MenuItem.FGCOLOR = self.FGCOLOR
        MenuItem.BGCOLOR = self.BGCOLOR
        MenuItem.ACTIVEFGCOLOR = self.BGCOLOR
        MenuItem.ACTIVEBGCOLOR = self.FGCOLOR
        self.musicFile = self.theme['music']

    def setUp(self, AIdifficulty): #Start new game based on selected theme and mode
        self.player1 = Paddle(1, self.theme['p1'])
        self.ball = Ball(self.theme['ball'])
        #self.spawn_sound = self.theme['sounds']['spawn']
        self.ball.bounce_sound = self.theme['sounds']['paddle']
        self.ball.wall_sound = self.theme['sounds']['wall']
        self.ball.score_sound = self.theme['sounds']['score']
        self.ball.collect_sound = self.theme['sounds']['collect']
        if not self.COMPUTER: #2 Player mode
            self.player2 = Paddle(2, self.theme['p2'])
            self.assignKeys(self.player1, self.PLAYER1UP2, self.PLAYER1DOWN2)
            self.assignKeys(self.player2, self.PLAYER2UP, self.PLAYER2DOWN)
        else: #1 Player mode
            self.player2 = AIPaddle(2, self.theme['p2'])
            self.player2.max_range = AIdifficulty['range']
            self.player2.difficulty = AIdifficulty['difficulty']
            self.ball.speed = AIdifficulty['ballspeed']
            self.assignKeys(self.player1, self.PLAYER1UP, self.PLAYER1DOWN)
        self.ball.SOUND = PowerUp.SOUND = self.SOUND
        if self.musicFile:
            pygame.mixer.music.load(self.musicFile)
        self.player1.speed = AIdifficulty['speed']
        self.player2.speed = AIdifficulty['speed']
        Obstacle.obstacletype = self.theme['obstacle']
        self.p = 0

    def assignKeys(self, player, upKey, downKey): #Assign controls to player
        player.upKey = upKey
        player.downKey = downKey

    def change_controls(self, controls):
        self.PLAYER1UP = controls['p1up']
        self.PLAYER1DOWN = controls['p1down']
        self.P1LAUNCHKEY = controls['p1launch']
        self.PLAYER1UP2 = controls['p1up2']
        self.PLAYER1DOWN2 = controls['p1down2']
        self.PLAYER2UP = controls['p2up']
        self.PLAYER2DOWN = controls['p2down']
        self.P2LAUNCHKEY = controls['p2launch']

    def checkForWinner(self): #Return the winning player, if any.
        if self.player1.score == self.endscore:
            return self.player1
        elif self.player2.score == self.endscore:
            return self.player2
        else:
            return None

    def display_score(self): #Update the score display based on current score
        rects = []
        score1 = self.gameFont.render(str(self.player1.score), 1, self.FGCOLOR, self.BGCOLOR)
        score2 = self.gameFont.render(str(self.player2.score), 1, self.FGCOLOR, self.BGCOLOR)
        scorerect1 = score1.get_rect(top=10, left=10)
        scorerect2 = score2.get_rect(top=10, right=self.screen.get_rect().right-10)
        rects.append(self.screen.blit(score1, scorerect1))
        rects += self.screen.blit(score2, scorerect2)

    def play_sound(self, sound): #Play passed sound if sound is currently on
        if self.SOUND:
            sound.play()

    def spawn_powerup(self): #Spawn a new powerup in center of screen
        #self.play_sound(self.spawn_sound)
        power = random.choice([BIG, SMALL, CATCH, OBSTACLE])
        x = random.randint(self.screen.get_rect().centerx-100, self.screen.get_rect().centerx+100)
        y = random.randint(20, self.screen.get_rect().height-20)
        PowerUp(power, (x, y))
        self.chance = self.chance_init

    def find_theme(self, name): #Returns the theme with a name that matches the name argument
        for theme in self.themes:
            if theme['name'] == name:
                return theme

    def main(self): #Main menu of game
        MenuItem.font = self.gameFont
        logo = POWERFONTBIG.render("Power Pong", 1, self.FGCOLOR)
        logorect = logo.get_rect(centerx=self.screen.get_rect().centerx, top=100)
        singlePlayerButton = MenuItem("Single Player", top=200)
        multiPlayerButton = MenuItem("Multi Player", top=250)
        settingsButton = MenuItem("Settings", top=300)
        exitButton = MenuItem("Exit", top=350)
        helpButton = MenuItem("Help", top=self.screen.get_height()-40, left=15)
        aboutButton = MenuItem("Credits", top=self.screen.get_height()-40, right=self.screen.get_width()-15)
        singlePlayerButton.command = self.single_player
        multiPlayerButton.command = self.multi_player
        settingsButton.command = self.settingsMenu
        exitButton.command = self.exit
        helpButton.command = self.How_to_Play
        aboutButton.command = self.about
        buttons = pygame.sprite.RenderPlain(singlePlayerButton, multiPlayerButton, settingsButton, exitButton, helpButton, aboutButton)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            button.command()

            self.screen.blit(self.bg, (0, 0))
            buttons.update()
            logo = POWERFONTBIG.render("PowerPong", 1, self.FGCOLOR, self.BGCOLOR)
            self.screen.blit(logo, logorect)
            buttons.draw(self.screen)
            pygame.display.flip()

    def single_player(self): #Menu for single player game
        self.COMPUTER = True
        message = self.gameFont.render("Choose Difficulty Level:", 1, self.FGCOLOR, self.BGCOLOR)
        messagerect = message.get_rect(top=100, centerx=self.screen.get_rect().centerx)
        easyButton = MenuItem("Easy", top=200)
        mediumButton = MenuItem("Medium", top=250)
        hardButton = MenuItem("Hard", top=300)
        backButton = MenuItem("Back", top=self.screen.get_height()-40, left=15)
        easyButton.command = lambda: self.setUp(self.EASYAI)
        mediumButton.command = lambda: self.setUp(self.MEDIUMAI)
        hardButton.command = lambda: self.setUp(self.HARDAI)
        buttons = pygame.sprite.RenderPlain(easyButton, mediumButton, hardButton, backButton)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            button.command()
                            if button == backButton:
                                return
                            result = self.run()
                            while result == AGAIN:
                                self.player1.reset()
                                self.player2.reset()
                                result = self.run()

            self.screen.blit(self.bg, (0, 0))
            buttons.update()
            buttons.draw(self.screen)
            self.screen.blit(message, messagerect)
            pygame.display.flip()

    def multi_player(self): #Menu for multiplayer game
        self.COMPUTER = False
        message = self.gameFont.render("Choose Game Speed:", 1, self.FGCOLOR, self.BGCOLOR)
        messagerect = message.get_rect(centerx=self.screen.get_rect().centerx, top=100)
        normalButton = MenuItem("Normal", top=200)
        fastButton = MenuItem("Fast", top=250)
        fastestButton = MenuItem("Fastest", top=300)
        backButton = MenuItem("Back", top=self.screen.get_height()-40, left=15)
        normalButton.command = lambda: self.setUp(self.EASYAI)
        fastButton.command = lambda: self.setUp(self.MEDIUMAI)
        fastestButton.command = lambda: self.setUp(self.HARDAI)
        buttons = pygame.sprite.RenderPlain(normalButton, fastButton, fastestButton, backButton)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            button.command()
                            if button == backButton:
                                return
                            result = self.run()
                            while result == AGAIN: #Run game again if player as long as player wants
                                self.player1.reset()
                                self.player2.reset()
                                result = self.run()

            self.screen.blit(self.bg, (0, 0))
            buttons.update()
            buttons.draw(self.screen)   
            self.screen.blit(message, messagerect)
            pygame.display.flip()

    def settingsMenu(self): #Settings menu for the game
        if self.SOUND: soundtext = "Sound: On"
        else: soundtext = "Sound: Off"
        if self.MUSIC: musictext = "Music: On"
        else: musictext = "Music: Off"
        message = POWERFONTBIG.render("Settings", 1, self.FGCOLOR, self.BGCOLOR)
        messagerect = message.get_rect(top=100, centerx=self.screen.get_rect().centerx)
        themeOption = MenuItem("Theme: " + self.theme['name'], top=200) 
        soundOption = MenuItem(soundtext, top=250)
        musicOption = MenuItem(musictext, top=300)
        scoreOption = MenuItem("Score: " + str(self.endscore), top=350)
        controlOption = MenuItem("Controls", top=400)
        backButton = MenuItem("Back", left=15, top=self.screen.get_height()-40)
        buttons = pygame.sprite.RenderPlain(soundOption, themeOption, scoreOption, backButton, controlOption, musicOption)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            if button == backButton:
                                return
                            elif button == soundOption: #Turn sound on/off
                                if not self.SOUND:
                                    soundOption.text = "Sound: " + ON
                                    self.SOUND = True
                                else:
                                    soundOption.text = "Sound: " + OFF
                                    self.SOUND = False
                            elif button == musicOption: #Turn music on/off
                                if not self.MUSIC:
                                    musicOption.text = "Music: " + ON
                                    self.MUSIC = True
                                else:
                                    musicOption.text = "Music: " + OFF
                                    self.MUSIC = False
                            elif button == themeOption:
                                theme = self.choose_theme()
                                if theme: #New theme
                                    self.setup_theme(theme)
                                    themeOption.text = "Theme: " + self.theme['name']
                                    for button in buttons:
                                        button.FGCOLOR = self.FGCOLOR
                                        button.BGCOLOR = self.BGCOLOR
                                    message = POWERFONTBIG.render("Settings", 1, self.FGCOLOR, self.BGCOLOR)
                            elif button == scoreOption:
                                self.set_score()
                                scoreOption.text = "Score: " + str(self.endscore)
                            elif button == controlOption:
                                controls = self.set_controls()
                                self.change_controls(controls)

            self.screen.blit(self.bg, (0, 0))
            buttons.update()
            buttons.draw(self.screen)
            self.screen.blit(message, messagerect)
            pygame.display.flip()

    def How_to_Play(self):
        backButton = MenuItem("Back", top=15, left=15)
        instructions = pygame.sprite.RenderPlain()
        title = POWERFONTBIG.render("How to Play", 1, self.FGCOLOR, self.BGCOLOR)
        titlerect = title.get_rect(top=100, centerx=self.screen.get_rect().centerx)
        t = 200
        for line in HELP.splitlines():
            if line != "":
                m = MenuItem(line, top=t, left=50, font=POWERFONTSMALL)
                instructions.add(m)
            t += 20

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if backButton.rect.collidepoint(event.pos):
                        self.play_sound(self.clickSound)
                        return
                    if event.button == 5:
                        for i in instructions:
                            i.rect = i.rect.move(0, -12)
                        titlerect = titlerect.move(0, -12)
                    if event.button == 4:
                        for i in instructions:
                            i.rect = i.rect.move(0, 12)
                        titlerect = titlerect.move(0, 12)

            self.screen.blit(self.bg, (0, 0))
            backButton.update()
            instructions.draw(self.screen)
            self.screen.blit(backButton.image, backButton.rect)
            self.screen.blit(title, titlerect)
            pygame.display.flip()

    def about(self):
        pygame.mixer.music.load(self.alternateMusic)
        if self.MUSIC:
            pygame.mixer.music.play()
        logo = POWERFONTBIG.render("PowerPong", 1, self.FGCOLOR, self.BGCOLOR)
        logorect = logo.get_rect(top=300, centerx=self.screen.get_rect().centerx)
        info = pygame.sprite.RenderPlain()
        t = 400
        for line in INFO.splitlines():
            if line != "":
                m = MenuItem(line, top=t, font=POWERFONT)
                info.add(m)
            t += 40

        while 1:
            self.clock.tick(45)
            r = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    pygame.mixer.music.stop()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    return

            self.screen.blit(self.bg, (0, 0))
            for i in info:
                i.rect = i.rect.move(0, -1)
                if self.screen.get_rect().contains(i.rect):
                    r += 1
            logorect = logorect.move(0, -1)
            info.draw(self.screen)
            self.screen.blit(logo, logorect)
            pygame.display.flip()
            if r == 0 and not self.screen.get_rect().contains(logorect): #Return when Credits are finished
                pygame.mixer.music.stop()
                return

    def choose_theme(self): #Displays available themes and changes theme to the one chosen by player
        message = POWERFONT.render("Choose a theme:", 1, self.FGCOLOR, self.BGCOLOR)
        messagerect = message.get_rect(centerx=self.screen.get_rect().centerx, top=100)
        backButton = MenuItem("Back", top=self.screen.get_rect().height-40, left=15)
        themes = pygame.sprite.RenderPlain() #Sprite group for displaying themes
        top = 200
        for theme in self.themes:
            item = MenuItem(theme['name'], top=top)
            themes.add(item)
            top += 50

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if backButton.rect.collidepoint(event.pos):
                        self.play_sound(self.clickSound)
                        return
                    for theme in themes:
                        if theme.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            newTheme = self.find_theme(theme.text)
                            return newTheme

            self.screen.blit(self.bg, (0, 0))
            themes.update()
            backButton.update()
            themes.draw(self.screen)
            self.screen.blit(backButton.image, backButton.rect)
            self.screen.blit(message, messagerect)
            pygame.display.flip()

    def set_score(self):
        message = POWERFONTBIG.render("Game Score:", 1, self.FGCOLOR, self.BGCOLOR)
        messagerect = message.get_rect(centerx=self.screen.get_rect().centerx, top=100)
        score = POWERFONT.render(str(self.endscore), 1, self.FGCOLOR, self.BGCOLOR)
        scorerect = score.get_rect(centerx=self.screen.get_rect().centerx, top=200)
        increase = MenuItem(">>", left=scorerect.right+10, top=200)
        decrease = MenuItem("<<", right=scorerect.left-10, top=200)
        backButton = MenuItem("Back", left=10, top=self.screen.get_rect().height-40)
        buttons = pygame.sprite.RenderPlain(increase, decrease, backButton)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            if button == increase:
                                if self.endscore < 99:
                                    self.endscore += 1
                            elif button == decrease:
                                if self.endscore > 1:
                                    self.endscore -= 1
                            elif button == backButton:
                                return

            self.screen.blit(self.bg, (0, 0))
            buttons.update()
            score = POWERFONT.render(str(self.endscore), 1, self.FGCOLOR, self.BGCOLOR)
            scorerect = score.get_rect(centerx=self.screen.get_rect().centerx, top=200)
            self.screen.blit(message, messagerect)
            self.screen.blit(score, scorerect)
            buttons.draw(self.screen)
            pygame.display.flip()

    def set_controls(self): #Change controls for game
        message = POWERFONT.render("Game Controls:", 1, self.FGCOLOR, self.BGCOLOR)
        messagerect = message.get_rect(centerx=self.screen.get_rect().centerx, top=50)
        singlePlayer = MenuItem("SinglePlayer:", left=50, top=100, font=POWERFONTSMALL)
        sp_p1ctrlup = ControlOption("Player1 Up: ", left=100, top=125, font=POWERFONTSMALL, control=self.PLAYER1UP)
        sp_p1ctrldown = ControlOption("Player1 Down: ", left=100, top=150, font=POWERFONTSMALL, control=self.PLAYER1DOWN)
        sp_p1ctrllaunch = ControlOption("Player1 Launch: ", left=100, top=175, font=POWERFONTSMALL, control=self.P1LAUNCHKEY)
        multiPlayer = MenuItem("MultiPlayer:", left=50, top=225, font=POWERFONTSMALL)
        mp_p1ctrlup = ControlOption("Player1 Up: ", left=100, top=250, font=POWERFONTSMALL, control=self.PLAYER1UP2)
        mp_p1ctrldown = ControlOption("Player1 Down: ", left=100, top=275, font=POWERFONTSMALL, control=self.PLAYER1DOWN2)
        mp_p2ctrlup = ControlOption("Player2 Up: ", left=100, top=300, font=POWERFONTSMALL, control=self.PLAYER2UP)
        mp_p2ctrldown = ControlOption("Player2 Down: ", left=100, top=325, font=POWERFONTSMALL, control=self.PLAYER2DOWN)
        mp_p2ctrllaunch = ControlOption("Player2 Launch: ", left=100, top=350, font=POWERFONTSMALL, control=self.P2LAUNCHKEY)
        backButton = MenuItem("Back", left=10, top=self.screen.get_height()-40, font=POWERFONT)
        backButton.changing = False #Used so no error occurs during button processing
        buttons = pygame.sprite.RenderPlain(sp_p1ctrlup, sp_p1ctrldown, sp_p1ctrllaunch, mp_p1ctrlup, mp_p1ctrldown, mp_p2ctrlup, mp_p2ctrldown, mp_p2ctrllaunch, backButton)
        changing = False
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            if button == backButton: #If user goes back, return new controls
                                controls = {'p1up':sp_p1ctrlup.control, 'p1down':sp_p1ctrldown.control, 'p1launch':sp_p1ctrllaunch.control,
                                            'p1up2':mp_p1ctrlup.control, 'p1down2':mp_p1ctrldown.control,
                                            'p2up':mp_p2ctrlup.control, 'p2down':mp_p2ctrldown.control, 'p2launch':mp_p2ctrllaunch.control}
                                return controls
                            if not changing: #If no other control is being changed
                                button.changing = True
                                changing = True
                elif event.type == pygame.KEYDOWN:
                    if changing and not event.key in self.RESERVED:
                        for button in buttons:
                            if button.changing:
                                button.control = event.key
                                button.changing = False
                                changing = False

            buttons.update()
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(message, messagerect)
            self.screen.blit(singlePlayer.image, singlePlayer.rect)
            self.screen.blit(multiPlayer.image, multiPlayer.rect)
            buttons.draw(self.screen)
            pygame.display.flip()

    def pauseGame(self):
        message = self.gameFont.render("Paused:", 1, self.FGCOLOR, self.BGCOLOR)
        messagerect = message.get_rect(centerx=self.screen.get_rect().centerx, top=180)
        continueButton = MenuItem(CONTINUE, top=230)
        quitButton = MenuItem(QUIT, top=280)
        buttons = pygame.sprite.RenderPlain(continueButton, quitButton)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return CONTINUE
                    elif event.key == pygame.K_ESCAPE:
                        return QUIT
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            return button.text

            buttons.update()
            buttons.draw(self.screen)
            self.screen.blit(message, messagerect)
            pygame.display.flip()

    def endGame(self, winner): #Menu for end of game
        centerx = self.screen.get_rect().centerx
        congrats = "Player %d wins!" % (winner.side)
        congrats = self.gameFont.render(congrats, 1, self.FGCOLOR, self.BGCOLOR)
        congratsrect = congrats.get_rect(top=150, centerx=centerx)
        againButton = MenuItem(AGAIN, top=230)
        menuButton = MenuItem(MENU, top=280)
        buttons = pygame.sprite.RenderPlain(againButton, menuButton)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            self.play_sound(self.clickSound)
                            if button == againButton:
                                return button.text
                            elif button == menuButton:
                                return button.text

            self.screen.blit(self.bg, (0, 0))
            buttons.update()
            buttons.draw(self.screen)
            self.screen.blit(congrats, congratsrect)
            pygame.display.flip()

    def run(self): #Main game loop
        i = 0
        players = pygame.sprite.RenderPlain(self.player1, self.player2)
        ball = pygame.sprite.RenderPlain(self.ball)
        powerups = pygame.sprite.RenderPlain()
        poweruptexts = pygame.sprite.RenderPlain()
        obstacles = pygame.sprite.RenderPlain()
        PowerUp.containers.append(powerups)
        PowerUpText.containers.append(poweruptexts)
        PowerUpText.font = self.gameFont
        Obstacle.containers.append(obstacles)
        self.clock = pygame.time.Clock()
        if self.musicFile and self.MUSIC:
            pygame.mixer.music.play(-1)
        while 1:
            i += 1
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.P1LAUNCHKEY:
                        if self.ball.side == self.player1.side:
                            self.ball.launched = True
                    if event.key == self.P2LAUNCHKEY and not self.COMPUTER:
                        if self.ball.side == self.player2.side:
                            self.ball.launched = True
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        status = self.pauseGame()
                        if status == QUIT:
                            pygame.mixer.music.stop()
                            return

            powerup = random.randint(0, self.chance) #Random chance of powerup appearing
            if powerup == 0:
                if len(powerups.sprites()) == self.MAX_POWERUPS:
                    powerups.remove(powerups.sprites()[0])
                self.spawn_powerup()
            else: #If no powerup, increase the chances of one appearing
                self.chance -= 1

            obstacles.update()
            players.update(self.ball)
            ball.update(self.player1, self.player2, powerups, obstacles)
            powerups.update()
            poweruptexts.update()

            self.screen.blit(self.bg, (0, 0))
            powerups.draw(self.screen)
            obstacles.draw(self.screen)
            poweruptexts.draw(self.screen)
            players.draw(self.screen)
            ball.draw(self.screen)
            self.display_score()
            pygame.display.flip()

            winner = self.checkForWinner()
            if winner:
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                self.play_sound(self.winnerSound)
                result = self.endGame(winner)
                return result

    def exit(self):
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    game = Game("PowerPong")
    game.main()
