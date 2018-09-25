from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame
from math import radians, sin, cos, atan, degrees

black = Color(0, 0.3)
noline = LineStyle(0, black)

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
        self.turn=0
        self.vx=1
        self.vy=1
        Game.listenMouseEvent('click', self.direct)
        
    def direct(self, event):
        self.targetx=event.x
        self.targety=event.y
        self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
        print(degrees(self.turn))
        
    def step(self):
        self.x+=(self.vx*cos(self.turn))
        self.y+=(self.vy*sin(self.turn))
        if self.x==self.targetx and self.y==self.targety:
            self.vx=0
            self.vy=0
        else:
            self.vx=2
            self.vy=2
        
class Enemy(Sprite):
    asset=ImageAsset("images/enemy_wheels.png", Frame(0,0,159,133), 4, 'horizontal')
    def __init__(self):
        super().__init__(Enemy.asset)
        self.hp=200
        self.direction=0
        self.f=0
        self.targetx=self.x
        self.targety=self.y
        self.scale=0.5
        #Enemy hitbox is as follows: Starts 21 to right of and 6 below spawn point. Stretches 36 wide and 57 tall
    
    def step(self):
        self.f+=1
        if self.f==2:
            self.f=0
        self.setImage(self.f)

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
        for char in self.getSpritesbyClass(Enemy):
            char.step()

myapp=Game()
myapp.run()