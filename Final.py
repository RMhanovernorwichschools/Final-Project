from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame, CircleAsset
from math import radians, sin, cos, atan, degrees
import time, random

black = Color(0, 0.3)
noline = LineStyle(0, black)
white = Color(0xFFFFFF, 1)

class Cover(Sprite):
    asset=ImageAsset('images/Rocks.png', Frame(0,0,195,190), 3, 'vertical')
    def __init__(self, position, frame):
        super().__init__(Cover.asset, position)
        self.setImage(frame)
        self.scale=0.45
        self.state='free'
        self.claimed=0
    
    def step(self):
        for m in myapp.getSpritesbyClass(Member):
            if m.x>self.x-4 and m.x<self.x+4 and m.y>self.y-4 and m.y<self.y+4 or self.claimed==1:
                self.state='taken'
            else:
                self.state='free'

class Bullet(Sprite):
    asset=CircleAsset(3, noline, white)
    def __init__(self, x,y, targetx, targety, damage, source):
        super().__init__(Bullet.asset)
        self.x=x+45
        self.y=y+30
        self.source=source
        self.targetx=targetx+35
        self.targety=targety+30
        self.rotation=atan((self.targety-self.y)/(self.targetx-self.x))
        if self.targetx<self.x:
            self.rotation+=radians(180)
        self.damage=damage
    
    def step(self):
        if self.source=='E':
            for char in myapp.getSpritesbyClass(Member):
                if self.x>char.x+30 and self.x<char.x+62 and self.y>char.y+5 and self.y<char.y+75 and char.state!='hidden' and char.state!='dead':
                    char.hit(self.damage)
                    self.source='None'
        elif self.source=='M':
            for char in myapp.getSpritesbyClass(Enemy):
                if self.x>char.x+30 and self.x<char.x+75 and self.y>char.y+5 and self.y<char.y+80 and char.state!='dead':
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
    def __init__(self, damage, caution, evasion, talk, health, position, nam):
        super().__init__(nam, position)
        self.scale=0.75
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
        self.state='unprep'
        self.prog='b'
        self.spot=''
        self.wait=time.time()
        Game.listenMouseEvent('click', self.direct)
        #Enemy hitbox is as follows: Starts 21 to right of and 6 below spawn point. Stretches 36 wide and 57 tall
        
    def direct(self, event):
        if self.state!='ready' and self.state!='hiding':
            self.targetx=event.x-35
            self.targety=event.y-28
            self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
            if self.targetx<self.x:
                self.turn+=radians(180)
            
    def hit(self, dam):
        self.hp-=dam
        if self.hp<=0:
            self.state='dead'
        elif self.hp<35:
            print('Warning: hp={0}'.format(self.hp))
        
    def step(self):
        for m in myapp.getSpritesbyClass(Member):
            while m.targetx>self.targetx-20 and m.targetx<self.targetx+20 and m.targety>self.targety-15 and m.targety<self.targety+15 and self.x!=m.x:
                self.targetx+=(random.randint(-5,5))
        if self.targetx!=self.x:
            self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
            if self.targetx<self.x:
                self.turn+=radians(180)
        self.x+=(self.v*cos(self.turn))
        self.y+=(self.v*sin(self.turn))
        if self.x<self.targetx+2 and self.x>self.targetx-2 and self.y<self.targety+2 and self.y>self.targety-2 and self.enemy=="None":
            self.v=0
            self.state='unprep'
            self.select_enemy()
        elif self.x<self.targetx+3 and self.x>self.targetx-3 and self.y<self.targety+3 and self.y>self.targety-3 and self.state=='hiding':
            self.v=0
            self.state='hidden'
            self.wait=time.time()
        elif self.state=="attackmode" and self.x<self.targetx+60 and self.x>self.targetx-60 and self.y<self.targety+60 and self.y>self.targety-60:
            self.v=0
            self.state='ready'
        elif self.state=='hidden':
            self.v=0
            self.f=4
            self.select_enemy()
            if self.enemy=='None':
                self.state='unprep'
                self.spot.claimed=0
            else:
                if self.targetx!=self.x:
                    self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
                    if self.targetx<self.x:
                        self.turn+=radians(180)
                if time.time()>self.wait:
                    self.state='firing'
        elif self.state=='firing':
            self.select_enemy()
            if time.time()>self.wait:
                Bullet(self.x, self.y, self.targetx, self.targety, self.damage, 'M')
                wait=(self.dodge)*(1.2**(random.randint(-4,4)/3.8))
                self.wait=time.time()+wait
                if self.prog!='b':
                    self.wait+=0.8
                self.state='delay'
                if cos(self.turn)<0:
                    self.f=5
                else:
                    self.f=2
        elif self.state=='delay':
            if time.time()>self.wait:
                if self.prog=='b': 
                    self.state='hidden'
                    self.wait=time.time()+self.caution
                else:
                    self.state='unprep'
        elif self.state=='dead':
            self.f=3
        else:
            if self.state=='unprep':
                self.select_enemy()
            self.v+=0.3
            if self.v>3:
                self.v=3
            elif self.v<0 and self.enemy=="None":
                self.v=0
            elif self.v<0 and self.enemy!="None":
                self.v=0
                self.state='ready'
        if self.state=='ready':
            sp=0
            d2=200**2
            for spot in myapp.getSpritesbyClass(Cover):
                y=spot.y-self.y
                x=spot.x-self.x
                d1=x**2+y**2
                if d1<d2 and spot.state=='free':
                    self.targetx=spot.x +5
                    self.targety=spot.y +5
                    sp=1
                    self.spot=spot
                    spot.claimed=1
                d2=d1
            if sp==1:
                self.state='hiding'
                self.prog='b'
            else:
                self.state='firing'
                self.prog='a'
        if self.v>0 and cos(self.turn)>=0:
            self.f+=1
            if self.f>1:
                self.f=0
        elif self.v>0 and cos(self.turn)<0:
            if self.f==6:
                self.f=7
            else:
                self.f=6
        self.setImage(self.f)
        
    def select_enemy(self):
        self.enemy="None"
        d2=160**2
        for enemy in myapp.getSpritesbyClass(Enemy):
            y=enemy.y-self.y
            x=enemy.x-self.x
            d1=x**2+y**2
            if d1<d2 and enemy.state!='dead':
                self.targetx=enemy.x +6
                self.targety=enemy.y +6
                self.enemy=enemy
                d2=d1
        if self.enemy!="None":
            if self.state=='unprep':
                self.state='attackmode'

class Enemy(Sprite):
    asset=ImageAsset("images/enemy_wheels.png", Frame(0,0,158,133), 7, 'horizontal')
    def __init__(self, position):
        super().__init__(Enemy.asset, position)
        self.hp=200
        self.turn=0
        self.f=0
        self.targetx=self.x
        self.targety=self.y
        self.scale=0.64
        self.v=0
        self.enemy="None"
        self.state='Seeking'
        self.damage=10
        self.wait=0
        self.m=0
        self.c=0
        #Member hitbox is as follows: Starts 25.5 to right of and 6 below spawn point. Stretches 29 wide and 50 tall
    
    def step(self):
        if self.state=='Seeking':
            self.pick_target(250)
            if self.enemy=='None':
                self.v=1
                if self.wait==0 or time.time()>self.wait:
                    self.wait=time.time()+3
                    self.m=radians(random.randint(-360,360))
                    self.state='Moving'
        elif self.state=='Firing':
            self.pick_target(100)
            self.v=0
            if self.enemy=='None':
                self.state='Seeking'
            else:
                self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
                if time.time()>self.wait and self.enemy.state!='hidden':
                    Bullet(self.x, self.y, self.targetx, self.targety, (self.damage+random.randint(-3,3)), 'E')
                    self.wait=time.time()+2
                if cos(self.turn)<0:
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
            if self.x!=self.targetx:
                self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
            if self.targetx<self.x:
                self.turn+=radians(180)
            if self.state=='Moving':
                self.turn=self.m
                if time.time()>self.wait:
                    self.state='Seeking'
            if self.x+(self.v*cos(self.turn))>myapp.width-50 or self.x+(self.v*cos(self.turn))<-21 or self.y+(self.v*sin(self.turn))>myapp.height-50 or self.y+(self.v*sin(self.turn))<-15:
                if self.c==0:
                    self.turn+=radians(180)
                    self.m+=radians(180)
                    self.c=1
            else:
                self.c=0
            self.x+=(self.v*cos(self.turn))
            self.y+=(self.v*sin(self.turn))
            if self.x<self.targetx+70 and self.x>self.targetx-70 and self.y<self.targety+70 and self.y>self.targety-70 and self.state=='Seeking':
                self.state='Firing'
                self.v=0
                self.wait=time.time()
            elif self.x<self.targetx+2 and self.x>self.targetx-2 and self.y<self.targety+2 and self.y>self.targety-2 and self.state!='Moving':
                self.v=0
            elif self.x<self.targetx+28 and self.x>self.targetx-28 and self.y<self.targety+28 and self.y>self.targety-28:
                self.v=3
            else:
                self.v+=0.1
                if self.v>1.8:
                    self.v=1.8
                elif self.v<0:
                    self.v=0
        if self.state=='dead':
            self.f=3
        self.setImage(self.f)
                
    def pick_target(self, d):
            self.enemy="None"
            d2=d**2
            for enemy in myapp.getSpritesbyClass(Member):
                y=enemy.y-self.y
                x=enemy.x-self.x
                d1=x**2+y**2
                if d1<d2 and enemy.state!='dead':
                    self.enemy=enemy
                    self.targetx=enemy.x +5
                    self.targety=enemy.y +5
                    d2=d1
                    self.v=1
                    
    def hit(self, dam):
        self.hp-=dam
        if self.hp<=0:
            self.state='dead'
        elif self.hp<30:
            print('Close: enemy hp={0}'.format(self.hp))
        if self.hp<0:
            self.hp=0

class Game(App):
    def __init__(self):
        super().__init__()
        Aasset=ImageAsset("images/Member_A.png", Frame(0,0,127,115), 8, 'horizontal')
        Basset=ImageAsset("images/Member_B.png", Frame(0,0,127,115), 8, 'horizontal')
        Casset=ImageAsset("images/Member_C.png", Frame(0,0,127,115), 8, 'horizontal')
        m = ImageAsset("images/map_base.jpg")
        am=Sprite(m)
        am.scale=2.2
        self.state='none'
        select=0
        while select=0:
            stage=input('''Select your level. 
                Enter t for tutorial
                1 for level 1
                2 for level 2
                or 3 for level 3 '''
            if stage=='t':
                select=1
                c=Cover((100,100), 2)
                c1=Cover((500,200), 1)
                b=Enemy((0,0))
                e=Enemy((300,300))
            elif stage=='1':
                print('In progress')
                select=1
            elif stage=='2':
                print('Working on it')
                select=1
            elif stage=='3':
                print('Soon')
                select=1
            else:
                print("Sorry, didn't understand. Try again.")
        a=Member(11,1.5,0.7,1,200, (500,0), Aasset)
        d=Member(7,2,0.31,1,180, (500,200), Casset)
        #Aasset attributes are as follows: (11,1.5,0.7,1,200)
        #Basset attributes are as follows: (20,0.5,2.5,1,180)
        #Casset attributes are as folloes: (7,2,0,31,1,180)
        
    def step(self):
        mems=0
        memdeath=0
        enems=0
        enemdeath=0
        for char in self.getSpritesbyClass(Member):
            mems+=1
            if char.state!='dead':
                char.step()
            else:
                char.setImage(3)
                memdeath+=1
        for char in self.getSpritesbyClass(Enemy):
            enems+=1
            char.step()
            if char.state=='dead':
                enemdeath+=1
        for x in self.getSpritesbyClass(Bullet):
            x.step()
        for x in self.getSpritesbyClass(Cover):
            x.step()
        if self.state=='none':
            if memdeath==mems:
                print('You lose.')
                self.state='loss'
            elif enemdeath==enems:
                print('You win!')
                self.state='win'

myapp=Game()
myapp.run()
