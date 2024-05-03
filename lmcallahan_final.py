"""
MAIN
Liam Callahan
4/19/2024
"""
import pygame, simpleGE, random


class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        #attributes
        self.colorRect("red", (25, 25))
        self.position = (50, 440)
        self.movespeed = 10
        self.jumpsnd=simpleGE.Sound("jump_01.wav")
        self.inAir = True
    def process(self):
        #key.inputs
        if self.isKeyPressed(pygame.K_a):
            self.x -= self.movespeed
        if self.isKeyPressed(pygame.K_d):
            self.x += self.movespeed
        if self.isKeyPressed(pygame.K_w):  
             if not self.inAir:
                self.dy = -20
                self.inAir = True
        #gravity
        if self.inAir==True:
            self.gravity = self.addForce(-1, 90)
        if self.y > 455:
            self.inAir = False
            self.y = 455
            self.dy = 0
        #check.bounds
        if self.right > 640:
            self.x=615
        if self.left < 0:
            self.x=20
        if self.top < 0:
            self.y=20
        #platforms
        for platform in self.scene.platforms:
            if self.collidesWith(platform):
                if self.dy > 0:
                        self.landsnd.play()
                        self.bottom = platform.top
                        self.inAir=False


#platforms

class Platform_green(simpleGE.Sprite):
    def __init__(self, scene, position):
        super().__init__(scene)
        #attributes
        self.position = (position)
        self.colorRect("dark green", (100, 15))
        self.speed = -1
        self.timer=simpleGE.Timer()
    def process(self):
        #movement
        self.dx= self.speed
        if self.timer.getElapsedTime() >= 2:
            self.speed-=.01
            self.timer.getTimeLeft=0
    def reset(self):
        self.y = (random.randrange(50, 460))

#Labels
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time: 0"
        self.center = (500, 30)


class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        #attributes
        self.background.fill("light blue")
        self.setCaption("oddle.jump")

        #timer
        self.timer_main=simpleGE.Timer()
        self.platform_timer=simpleGE.Timer()
       
        #sprites
        self.player=Player(self)
        self.timer=LblTime()
        
        
        #platforms
        self.platform=Platform_green
        self.platforms=[]
        for i in range(8):
            plat_x=(random.randrange(90, 580))
            plat_y=(random.randrange(50, 460))
            self.platforms.append(Platform_green(self, (plat_x, plat_y)))
        #all
        self.sprites=[self.player,
                      self.platforms,
                      self.timer
                      ]
    def process(self):
        for platform in self.platforms:
            if platform.left==0:
                platform.reset()
        if self.timer_main.getElapsedTime()>=3:
            if self.player.y>=450:
                print(f"Time: {self.timer_main.getElapsedTime():.2f}")
                self.stop()
        self.timer.text = f"time: {self.timer_main.getElapsedTime():.2f}"

class Intro(simpleGE.Scene):
        def __init__(self):
            super().__init__()
            self.background.fill("light blue")
            self.response = "play"
            self.Instructions = simpleGE.MultiLabel()
            self.Instructions.center = (320, 240)
            self.Instructions.size = (500, 250)
            self.Instructions.textLines = [
                "you are the square",
                "A: left",
                "D: right",
                "W: jump",
                "don't hit the bottom"
            ]
        
            self.btnPlay = simpleGE.Button()
            self.btnPlay.text = "Play"
            self.btnPlay.center=(100,400)
            self.btnQuit = simpleGE.Button()
            self.btnQuit.text = "Quit"
            self.btnQuit.center=(540, 400)
            
            self.sprites = [self.Instructions,
                            self.btnPlay,
                            self.btnQuit,
            ]
        def process(self):
            if self.btnPlay.clicked:
                self.response = "play"
                self.stop()
            if self.btnQuit.clicked:
                self.response = "quit"
                self.stop()
#running
def main():
    keepgoing=True
    while keepgoing:
        intro=Intro()
        intro.start()
        if intro.response == "play":
            game = Game()
            game.start()
        else:
            keepgoing=False

if __name__ == "__main__":
    main()