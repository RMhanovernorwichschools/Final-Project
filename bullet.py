from ggame import App, RectangleAsset, CircleAsset, Sprite, LineStyle, Color
from math import radians, sin, cos, degrees

#So radians(90) means to the right, radians (180) is up, so 0 should be down and 270 left. 

black = Color(0, 1)
noline = LineStyle(0, black)

class ShooterTest(App):
    def __init__(self):
        super().__init__()
        ShooterTest.listenMouseEvent('click', self.mouseClick)
    
    def mouseClick(self, event):
        char=Char(event.x,event.y)
        
    def step(self):
        for x in self.getSpritesbyClass(Char):
            x.step()
        for x in self.getSpritesbyClass(Bullet):
            x.step()
        
class Bullet(Sprite):
    asset=CircleAsset(3, noline, black)
    def __init__(self, x,y, direc):
        super().__init__(Bullet.asset)
        self.x=x
        self.y=y
        self.rotation=direc
    
    def step(self):
        if self.x<myapp.width and self.y<myapp.height and self.y>0 and self.x>0:
            self.x+=(3*sin(self.rotation))
            self.y+=(3*cos(self.rotation))
        else:
            print('Hit!')
            self.destroy()
        

class Char(Sprite):
    asset=RectangleAsset(15,15,noline, black)
    def __init__(self, x,y):
        super().__init__(Char.asset)
        self.x=x
        self.y=y
        self.rotation=radians(180)
        self.vx=0
        self.vy=0
        self.rch=0
        ShooterTest.listenKeyEvent('keydown', 'a', self.tl)
        ShooterTest.listenKeyEvent('keyup', 'a', self.ct)
        ShooterTest.listenKeyEvent('keydown', 'd', self.tr)
        ShooterTest.listenKeyEvent('keyup', 'd', self.ct)
        ShooterTest.listenKeyEvent('keydown', 'space', self.shoot)
        
    def step(self):
        self.rotation+=self.rch
        self.vx=sin(self.rotation)
        self.vy=cos(self.rotation)
        self.x+=self.vx
        self.y+=self.vy
        
    def tl (self, event):
        self.rch=0.03
    def tr (self, event):
        self.rch=-0.03
    def ct(self, event):
        self.rch=0
        
    def shoot(self, event):
        Bullet(self.x, self.y, self.rotation)

myapp=ShooterTest()
myapp.run()
