from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame, CircleAsset
from math import radians, sin, cos, atan, degrees

black = Color(0, 0.3)
noline = LineStyle(0, black)

class Bullet(Sprite):
    asset=CircleAsset(2, noline, black)
    def __init__(self, x,y, direc, damage):
        super().__init__(Bullet.asset)
        self.x=x
        self.y=y
        self.rotation=direc
        self.damage=damage
    
    def step(self):
        if self.x<myapp.width and self.y<myapp.height and self.y>0 and self.x>0:
            self.x+=(3*sin(self.rotation))
            self.y+=(3*cos(self.rotation))
        else:
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
        
    def direct(self, event):
        self.targetx=event.x-30
        self.targety=event.y-30
        self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
        if self.targetx<self.x:
            self.turn+=radians(180)
        
    def step(self):
        if self.state=="idle" or self.state=='motion':
            self.x+=(self.v*cos(self.turn))
            self.y+=(self.v*sin(self.turn))
            if self.x<self.targetx+2 and self.x>self.targetx-2 and self.y<self.targety+2 and self.y>self.targety-2 and self.enemy=="None":
                self.v=0
                self.state='idle'
            elif self.enemy!="None" and self.x<self.targetx+30 and self.x>self.targetx-30 and self.y<self.targety+30 and self.y>self.targety-30:
                self.v=0
                self.state='ready'
            elif self.x<self.targetx+28 and self.x>self.targetx-28 and self.y<self.targety+28 and self.y>self.targety-28:
                self.v=3
                self.state='motion'
            else:
                self.state='motion'
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
        #Enemy hitbox is as follows: Starts 21 to right of and 6 below spawn point. Stretches 36 wide and 57 tall
    
    def step(self):
        if self.state=='Seeking':
            self.pick_target()
        elif self.state=='Firing':
            self.pick_target()
            self.v=0
            if self.enemy=='None':
                self.state='Seeking'
            else:
                self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
                print('bang')
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
            self.setImage(self.f)
            self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
            if self.targetx<self.x:
                self.turn+=radians(180)
            self.x+=(self.v*cos(self.turn))
            self.y+=(self.v*sin(self.turn))
            if self.x<self.targetx+25 and self.x>self.targetx-25 and self.y<self.targety+25 and self.y>self.targety-25 and self.state=='Seeking':
                self.state='Firing'
                self.v=0
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
                
    def pick_target(self):
            self.enemy="None"
            d2=200**2
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
        a=Member(1,1,1,1,1, (500,0))
        
    def step(self):
        for char in self.getSpritesbyClass(Member):
            char.step()
        for char in self.getSpritesbyClass(Enemy):
            char.step()

myapp=Game()
myapp.run()
