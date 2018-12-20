from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame, CircleAsset, TextAsset
from math import radians, sin, cos, atan, degrees
import time, random

black = Color(0, 0.3)
noline = LineStyle(0, black)
white = Color(0xFFFFFF, 1)

class Cover(Sprite):
    def __init__(self, position, frame, asset):
        super().__init__(asset, position)
        self.setImage(frame)
        self.scale=0.52
        self.state='free'
        self.claimed=0
    
    def step(self):
        if self.claimed==1:
            self.state='taken'
        else:
            self.state='free'
        m=0
        for x in myapp.getSpritesbyClass(Member):
            if x.spot==''or x.state=='dead' or x.state=='unprep':
                m+=1
            for a in myapp.getSpritesbyClass(Member):
                if a!=x and a.spot!=''and a.spot==x.spot and x.prog=='b' and a.prog=='b':
                    a.spot=''
                    a.state='unprep'
        if m==3:
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
    def __init__(self, damage, caution, evasion, talk, health, position, nam, t):
        super().__init__(nam, position)
        self.scale=0.75
        self.title=t
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
        if (self.state=='unprep' or self.state=='attackmode' or (self.state=='firing'and self.prog!='b')) or self.comm==0:
            if self.spot!='' and (self.x>self.spot.x+4 or self.x<self.spot.x-4) and (self.x>self.spot.x+4 or self.x<self.spot.x-4):
                self.spot.claimed=0
            self.targetx=event.x-35
            self.targety=event.y-28
            self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
            if self.targetx<self.x:
                self.turn+=radians(180)
            
    def hit(self, dam):
        self.hp-=dam
        if self.hp<=0:
            self.hp=0
            self.state='dead'
        
    def step(self):
        if self.comm==0:
            self.state='unprep'
            self.enemy='None'
        for m in myapp.getSpritesbyClass(Member):
            while m.targetx>self.targetx-20 and m.targetx<self.targetx+20 and m.targety>self.targety-15 and m.targety<self.targety+15 and self.x!=m.x:
                self.targetx+=(random.randint(-5,5))
        if self.targetx!=self.x:
            self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
            if self.targetx<self.x:
                self.turn+=radians(180)
        self.x+=(self.v*cos(self.turn))
        self.y+=(self.v*sin(self.turn))
        if self.x<self.targetx+2 and self.x>self.targetx-2 and self.y<self.targety+2 and self.y>self.targety-2 and self.enemy=="None" and self.state!='hiding':
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
            self.spot.state='taken'
            if self.enemy=='None':
                self.state='unprep'
            else:
                if self.targetx!=self.x:
                    self.turn=atan((self.targety-self.y)/(self.targetx-self.x))
                    if self.targetx<self.x:
                        self.turn+=radians(180)
                if time.time()>self.wait and self.comm!=0:
                    self.state='firing'
        elif self.state=='firing':
            self.select_enemy()
            if time.time()>self.wait:
                Bullet(self.x, self.y, self.targetx, self.targety, self.damage, 'M')
                wait=(self.dodge)*(1.2**(random.randint(-4,4)/3.8))
                self.wait=time.time()+wait
                if self.prog!='b':
                    self.wait+=0.8
                    self.spot.state='free'
                elif self.prog=='b':
                    self.spot.state='taken'
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
                    self.state='ready'
        elif self.state=='dead':
            self.f=3
        else:
            if self.state=='unprep' and self.comm!=0:
                self.select_enemy()
            self.v+=0.3
            if self.v>3:
                self.v=3
            elif self.v<0 and self.enemy=="None":
                self.v=0
            elif self.v<0 and self.enemy!="None" and self.comm!=0:
                self.v=0
                self.state='ready'
        if self.state=='ready':
            sp=0
            d2=180**2
            for spot in myapp.getSpritesbyClass(Cover):
                y=(spot.y+5)-self.y
                x=(spot.x+5)-self.x
                d1=x**2+y**2
                if d1<d2 and spot.state=='free':
                    self.targetx=spot.x +5
                    self.targety=spot.y +12
                    sp=1
                    self.spot=spot
                    d2=d1
            if sp==1:
                self.spot.claimed=1
                self.spot.state='taken'
                self.state='hiding'
                self.prog='b'
            else:
                self.state='firing'
                self.prog='a'
        if self.v>0 and cos(self.turn)>=0:
            self.f+=0.25
            if self.f>1.5:
                self.f=0
        elif self.v>0 and cos(self.turn)<0:
            if self.f<6 or self.f>7:
                self.f=6
            else:
                self.f+=0.25
        if self.f==int(self.f):
            self.setImage(self.f)
        
    def select_enemy(self):
        self.enemy="None"
        d2=180**2
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
        self.hp=190
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
                if self.targetx<self.x:
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
        if self.hp<0:
            self.hp=0

class Game(App):
    def __init__(self):
        super().__init__()
        Aasset=ImageAsset("images/Member_A.png", Frame(0,0,127,115), 8, 'horizontal')
        Basset=ImageAsset("images/Member_B.png", Frame(0,0,127,115), 8, 'horizontal')
        Casset=ImageAsset("images/Member_C.png", Frame(0,0,127,115), 8, 'horizontal')
        Dasset=ImageAsset("images/Member_D.png", Frame(0,0,127,115), 8, 'horizontal')
        #Cover images is 812 wide and 191*4 down)
        rock=ImageAsset('images/Cover.png', Frame(0,0,203,191), 3, 'vertical')
        pillar=ImageAsset('images/Cover.png', Frame(203,0,203,191), 3, 'vertical')
        box=ImageAsset('images/Cover.png', Frame(406,0,203,191), 3, 'vertical')
        etc=ImageAsset('images/Cover.png', Frame(609,0,203,191), 3, 'vertical')
        self.state='none'
        self.labels=[]
        instructions=['These are the instructions. Press enter to continue.', 'If, at any point, you want to skip the instructions, type "s" then press enter.', 'This game allows you to control three characters and use them to defeat enemies in various levels.', 'To control the characters, click any location on the map. They will go to that location.', 'If they are busy (hiding, shooting at any enemy, etc.) then they will not respond.', 'If you want them to respond even while they are busy, use your "control keys".', 'There is a different control key for each character. The first uses the control key "a", the second uses "b", and the third uses "c".', 'To use the control key, merely hold it down. While you are holding it, the character will ignore nearby enemies and focus only on your instructions.', 'When you release the key, they will resume paying attention to enemies nearby.', 'Have fun! Press enter to select your level.']
        for a in instructions:
            if input(a)=='s':
                break
        select=0
        while select==0:
            stage=input('''Select your level. 
                Enter t for tutorial
                1 for level 1
                2 for level 2
                or 3 for level 3 
                
                
                ''')
            if stage=='t':
                select=1
                m = ImageAsset("images/map_base.jpg")
                am=Sprite(m)
                am.scale=1.2
                c=Cover((100,100), 2, etc)
                c1=Cover((500,200), 0, rock)
                b=Enemy((0,0))
                e=Enemy((300,300))
                coor_a=(500,0)
                coor_b=(500,200)
                coor_c=(500,400)
            elif stage=='1':
                select=1
                m = ImageAsset("images/map_base2.jpg")
                am=Sprite(m)
                am.scale=1.2
                c=Cover((100,290), 2, etc)
                c1=Cover((700,360), 1, rock)
                c2=Cover((304, 390), 0, rock)
                c3=Cover((500, 30), 2, rock)
                e=Enemy((800,0))
                e1=Enemy((782,15))
                e2=Enemy((802,30))
                coor_a=(0,0)
                coor_b=(0,10)
                coor_c=(0,21)
            elif stage=='2':
                select=1
                m = ImageAsset("images/map_base3.jpg")
                am=Sprite(m)
                am.scale=1.1
                c=Cover((10,100), 0, pillar)
                c1=Cover((120,105), 1, pillar)
                c2=Cover((600, 50), 0, pillar)
                c3=Cover((800, 300), 2, box)
                coor_a=(500,0)
                coor_b=(550,0)
                coor_c=(450,50)
                e=Enemy((800,0))
                e1=Enemy((10,250))
                e2=Enemy((400,300))
                e3=Enemy((800,400))
                e3.hp=40
                e3.scale=0.58
            elif stage=='3':
                select=1
                m = ImageAsset("images/map_base4.jpg")
                am=Sprite(m)
                am.scale=1.1
                c=Cover((10,0), 0, etc)
                c1=Cover((550,300), 1, rock)
                c2=Cover((480, 320), 1, etc)
                c2.scale=0.47
                e1=Enemy((400,50))
                e2=Enemy((500,50))
                e=Enemy((450, 20))
                e.hp=250
                e.scale=0.8
                coor_a=(0,251)
                coor_b=(400,252)
                coor_c=(800,253)
            else:
                print("Sorry, didn't understand. Try again.")
        self.akey='False'
        self.bkey='False'
        self.ckey='False'
        select=0
        while select==0:
            char=input('''Select a type for the first position:
  a is generally balanced
  b is slow but powerful
  c is quick with light damage
  d has high damage and low hp
  
  
  
  ''')
            if char=='a':
                Member(10,1.5,1,1,190, coor_a, Aasset, 'a')
                select=1
            elif char=='b':
                Member(18,0.5,2.5,1,185, coor_a, Basset, 'a')
                select=1
            elif char=='c':
                Member(7,2,0.3,1,180, coor_a, Casset, 'a')
                select=1
            elif char=='d':
                Member(33,1.1,0.8,1,50, coor_a, Dasset, 'a')
                select=1
            else:
                print("Sorry, I don't understand.")
        while select==1:
            char=input('''Select a type for the second position:
 (see desc above) 
 
 
 ''')
            if char=='a':
                Member(10,1.5,1,1,190, coor_b, Aasset, 'b')
                select=2
            elif char=='b':
                Member(18,0.5,2.5,1,185, coor_b, Basset, 'b')
                select=2
            elif char=='c':
                Member(7,2,0.3,1,180, coor_b, Casset, 'b')
                select=2
            elif char=='d':
                Member(33,1.1,0.8,1,50, coor_b, Dasset, 'b')
                select=2
            else:
                print("Sorry, I don't understand.")
        while select==2:
            char=input('''Select a type for the third (and final) position:
 (see desc. above) 
 
 
 ''')
            if char=='a':
                a=Member(10,1.5,1,1,190, coor_c, Aasset, 'c')
                select=0
            elif char=='b':
                a=Member(18,0.5,2.5,1,185, coor_c, Basset, 'c')
                select=0
            elif char=='c':
                a=Member(7,2,0.3,1,180, coor_c, Casset, 'c')
                select=0
            elif char=='d':
                Member(33,1.1,0.8,1,50, coor_c, Dasset, 'c')
                select=0
            else:
                print("Sorry, I don't understand.")
        #Aasset attributes are as follows: (11,1.5,0.7,1,200)
        #Basset attributes are as follows: (20,0.5,2.5,1,170)
        #Casset attributes are as folloes: (7,2,0,3,1,180)
        for x in self.getSpritesbyClass(Member):
            pic=TextAsset(str(x.hp),
            style='bold 16px Times',
            fill=Color(0x070E68, 0.9))
            pict=Sprite(pic,(x.x+33,x.y+80))
            self.labels.append([pict, x, x.hp, 'M'])
        for x in self.getSpritesbyClass(Enemy):
            pic=TextAsset(str(x.hp),
            style='bold 16px Helvetica',
            fill=Color(0x8C2727, 0.9))
            pict=Sprite(pic,(x.x+33,x.y+80))
            self.labels.append([pict, x, x.hp, 'E'])
        
        Game.listenKeyEvent('keydown', 'a', self.a_down)
        Game.listenKeyEvent('keyup', 'a', self.a_up)
        Game.listenKeyEvent('keydown', 'b', self.b_down)
        Game.listenKeyEvent('keyup', 'b', self.b_up)
        Game.listenKeyEvent('keydown', 'c', self.c_down)
        Game.listenKeyEvent('keyup', 'c', self.c_up)
    
    def a_down(self, event):
        self.akey='True'
    def a_up(self, event):
        self.akey='False'
    def b_down(self, event):
        self.bkey='True'
    def b_up(self, event):
        self.bkey='False'
    def c_down(self, event):
        self.ckey='True'
    def c_up(self, event):
        self.ckey='False'
        
    def step(self):
        for x in self.labels:
            if x[2]!=x[1].hp:
                x[0].destroy()
                if x[1].hp>0:
                    if x[3]=='M':
                        pic=TextAsset(str(x[1].hp), 
                        style='bold 16px Times',
                        fill=Color(0x070E68, 0.9))
                    else:
                        pic=TextAsset(str(x[1].hp), 
                        style='bold 16px Helvetica',
                        fill=Color(0x8C2727, 0.9))
                    pict=Sprite(pic,(x[1].x+33,x[1].y+84))
                    a=x[3]
                    self.labels.append([pict, x[1], x[1].hp, a])
                self.labels.remove(x)
            else:
                x[0].x=x[1].x+40
                x[0].y=x[1].y+84
        mems=0
        memdeath=0
        enems=0
        enemdeath=0
        for char in self.getSpritesbyClass(Member):
            if (char.title=='a' and self.akey=='True') or (char.title=='b' and self.bkey=='True') or (char.title=='c' and self.ckey=='True'):
                char.comm=0
            else:
                char.comm=1
            mems+=1
            if char.state!='dead':
                char.step()
            else:
                char.setImage(3)
                char.spot.claimed=0
                memdeath+=1
        for char in self.getSpritesbyClass(Enemy):
            enems+=1
            if char.state=='dead':
                enemdeath+=1
                char.v=0
                char.setImage(3)
            else:
                char.step()
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
