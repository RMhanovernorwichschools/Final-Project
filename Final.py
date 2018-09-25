from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame
from math import radians, sin, cos

class Member(Sprite):
    asset=ImageAsset("images/beach-ball-575425_640.png")
    def __init__(self, damage, caution, evasion, talk, health):
        super().__init__(Member.asset)
        self.scale=0.1
        self.hp=health
        self.damage=damage
        self.dodge=evasion
        self.comm=talk
        self.caution=caution
        self.targetx=self.x
        self.targety=self.y
        Game.listenMouseEvent('click', self.direct)
        
    def direct(self, event):
        self.targetx=event.x
        self.targety=event.y
        
    def step(self):
        self.x=(self.x+self.targetx+self.x)/3
        self.y=(self.y+self.targety+self.y)/3
        
class Enemy(Sprite):
    asset=ImageAsset("images/enemy_wheels.png", Frame(0,0,159,133), 4, 'horizontal')
    def __init__(self):
        super().__init__(Enemy.asset)
        self.hp=200
        self.direction=0

class Game(App):
    def __init__(self):
        super().__init__()
        m = ImageAsset("images/map_base.jpg")
        am=Sprite(m)
        am.scale=2.2
        a=Member(1,1,1,1,1)
        b=Enemy()
        
    def step(self):
        for char in self.getSpritesbyClass(Member):
            char.step()

myapp=Game()
myapp.run()