from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame, CircleAsset
from math import radians, sin, cos, atan, degrees
import time

black = Color(0, 0.3)
noline = LineStyle(0, black)
white = Color(0xFFFFFF, 1)

class Cover(Sprite):
    asset=ImageAsset('images/Rocks.png', Frame(0,0,195,190), 3, 'vertical')
    def __init__(self, position, frame):
        super().__init__(Cover.asset, position)
        self.setImage(frame)
        self.scale=0.4

class Bullet(Sprite):
    asset=CircleAsset(3, noline, white)
    def __init__(self, x,y, targetx, targety, damage, source):
        super().__init__(Bullet.asset)
        self.x=x+45
        self.y=y+30
        self.source=source
        self.targetx=targetx+20
        self.targety=targety+30
        self.rotation=atan((self.targety-self.y)/(self.targetx-self.x))
        if self.targetx<self.x:
            self.rotation+=radians(180)
        self.damage=damage
    
    def step(self):
        if self.source=='E':
            for char in myapp.getSpritesbyClass(Member):
                if self.x>char.x+21 and self.x<char.x+57 and self.y>char.y+6 and self.y<char.y+63:
                    char.hit(self.damage)
                    self.source='None'
        if self.x<myapp.width and self.y<myapp.height and self.y>0 and self.x>0:
            self.x+=(6*cos(self.rotation))
            self.y+=(6*sin(self.rotation))
        else:
            self.source='None'
        if self.source=='None':
            self.destroy()

class Member(Sprite):
    asset=ImageAsset("images/Member_A.png", Frame(0,0,127,115), 8, 'horizontal')
    def __init__(self, damage, caution, evasion, talk, health, position):
        super().__init__(Member.asset, position)
        self.scale=0.6
        self.hp=health
        self.damage=damage
        self.dodge=evasion
        self.comm=talk
        self.caution=caution
        self.targetx=self.x
        self.targety=self.y
        self.turn=0
        self.v=1
        self.f=0
        self.enemy="None"
        self.state='idle'
        Game.listenMouseEvent('click', self.direct)
        #Enemy hitbox is as follows: Starts 21 to right of and 6 below spawn point. Stretches 36 wide and 57 tall
        
    def direct(self, event):
        self.targetx=event.x-35
        self.targety=event.y-28
        self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
        if self.targetx<self.x+20:
            self.turn+=radians(180)
            
    def hit(self, dam):
        self.hp-=dam
        if self.hp<=0:
            self.state='dead'
        print(self.hp)
        
    def step(self):
        if self.state=="idle" or self.state=='motion':
            self.x+=(self.v*cos(self.turn))
            self.y+=(self.v*sin(self.turn))
            if self.x<self.targetx+2 and self.x>self.targetx-2 and self.y<self.targety+2 and self.y>self.targety-2 and self.enemy=="None":
                self.v=0
                self.state='idle'
            elif self.enemy!="None" and self.x<self.targetx+60 and self.x>self.targetx-60 and self.y<self.targety+60 and self.y>self.targety-60:
                self.v=0
                self.state='ready'
            else:
                self.state='motion'
                self.select_enemy()
                self.v+=0.3
                if self.v>3:
                    self.v=3
                elif self.v<0 and self.enemy=="None":
                    self.v=0
                    self.state='idle'
                elif self.v>0 and self.enemy!="None":
                    self.v=0
                    self.state='ready'
            if self.state=='motion' and cos(self.turn)>=0:
                self.f+=1
                if self.f>1:
                    self.f=0
            elif self.state=='motion' and cos(self.turn)<0:
                if self.f==6:
                    self.f=7
                else:
                    self.f=6
            self.setImage(self.f)
        elif self.state=='ready':
            d2=999999999999999999999999
            for spot in myapp.getSpritesbyClass(Cover):
                y=spot.y-self.y
                x=spot.x-self.x
                d1=x**2+y**2
                if d1<d2:
                    self.targetx=spot.x +5
                    self.targety=spot.y +5
            self.state='attackmodemotion'
        elif self.state=='attackmodemotion':
            if self.x<self.targetx+2 and self.x>self.targetx-2 and self.y<self.targety+2 and self.y>self.targety-2 and self.enemy=="None":
                self.v=0
                self.state='attackmodefire'
            else: 
                self.x+=(self.v*cos(self.turn))
                self.y+=(self.v*sin(self.turn))
                self.v+=0.3
                if self.v>3:
                    self.v=3
                if cos(self.turn)>=0:
                    self.f+=1
                    if self.f>1:
                        self.f=0
                elif cos(self.turn)<0:
                    if self.f==6:
                        self.f=7
                    else:
                        self.f=6
                self.setImage(self.f)
        elif self.state=='attackmodefire':
            print('BANG!')
        elif self.state=='dead':
            self.setImage(3)
        
    def select_enemy(self):
        self.enemy="None"
        d2=66**2
        for enemy in myapp.getSpritesbyClass(Enemy):
            y=enemy.y-self.y
            x=enemy.x-self.x
            d1=x**2+y**2
            if d1<d2:
                self.enemy=enemy
            if self.enemy!="None":
                self.targetx=enemy.x 
                self.targety=enemy.y

class Enemy(Sprite):
    asset=ImageAsset("images/enemy_wheels.png", Frame(0,0,158,133), 7, 'horizontal')
    def __init__(self):
        super().__init__(Enemy.asset)
        self.hp=200
        self.turn=0
        self.f=0
        self.targetx=self.x
        self.targety=self.y
        self.scale=0.5
        self.v=0
        self.enemy="None"
        self.state='Seeking'
        self.damage=10
        self.wait=0
        #Member hitbox is as follows: Starts 25.5 to right of and 6 below spawn point. Stretches 29 wide and 50 tall
    
    def step(self):
        if self.state=='Seeking':
            self.pick_target(250)
        elif self.state=='Firing':
            self.pick_target(100)
            self.v=0
            if self.enemy=='None':
                self.state='Seeking'
            else:
                self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
                if time.time()>self.wait:
                    Bullet(self.x, self.y, self.targetx, self.targety, self.damage, 'E')
                    self.wait=time.time()+2
                if sin(self.turn)<0:
                    self.f=4
                else:
                    self.f=2
        if self.v>0:
            if cos(self.turn)>=0:
                self.f+=1
                if self.f>1:
                    self.f=0
            elif cos(self.turn)<0:
                if self.f==5:
                    self.f=6
                else:
                    self.f=5
            if self.f==2:
                self.f=0
            self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
            if self.targetx<self.x:
                self.turn+=radians(180)
            self.x+=(self.v*cos(self.turn))
            self.y+=(self.v*sin(self.turn))
            if self.x<self.targetx+70 and self.x>self.targetx-70 and self.y<self.targety+70 and self.y>self.targety-70 and self.state=='Seeking':
                self.state='Firing'
                self.v=0
                self.wait=time.time()
            elif self.x<self.targetx+2 and self.x>self.targetx-2 and self.y<self.targety+2 and self.y>self.targety-2:
                self.v=0
            elif self.x<self.targetx+28 and self.x>self.targetx-28 and self.y<self.targety+28 and self.y>self.targety-28:
                self.v=3
            else:
                self.v+=0.1
                if self.v>1.8:
                    self.v=1.8
                elif self.v<0:
                    self.v=0
        self.setImage(self.f)
                
    def pick_target(self, d):
            self.enemy="None"
            d2=d**2
            for enemy in myapp.getSpritesbyClass(Member):
                y=enemy.y-self.y
                x=enemy.x-self.x
                d1=x**2+y**2
                if d1<d2:
                    self.enemy=enemy
                    self.targetx=enemy.x
                    self.targety=enemy.y
                    d2=d1
                    self.v=1

class Game(App):
    def __init__(self):
        super().__init__()
        m = ImageAsset("images/map_base.jpg")
        am=Sprite(m)
        am.scale=2.2
        b=Enemy()
        a=Member(1,1,1,1,200, (500,0))
        c=Cover((100,100), 0)
        c1=Cover((500,200), 1)
        
    def step(self):
        for char in self.getSpritesbyClass(Member):
            char.step()
        for char in self.getSpritesbyClass(Enemy):
            char.step()
        for x in self.getSpritesbyClass(Bullet):
            x.step()

myapp=Game()
myapp.run()
