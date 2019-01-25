'''IMPORTANT NOTES:
A / damage done(*5): is ratio of dps divided by 50
B / damage taken(*5): is % of damage taken by an enemy firing from all(0) to none(1)
C / perception(*2): is % of time when hiding enemy is found from always(1) to never(0)
D / stealth(*2): is % of time when enemy while mem is hiding from never(1) to always(0)
E / done damage control(*3): is ratio of dps divided by n in transition from best to worst case scenario in five steps
F / taken damage control(*3): is % of damage taken by enemy in transition to best to worst case scenario in five steps
G / aid to mems(*5): is change in mems damage(done and taken) (three steps, 1,2,4 mems) from *1(0) to *2.5(1)
'''

#damage per shot in hp
dam=20
#time to aim/shoot (time between deciding to fire and doing so) in seconds
rof=0.4
#shots fired before load necessary
ammo=20
#time it takes to load after full shots have been fired
loadt=1
#the special ability that the mem can use
buff='none'

if buff=='none':
    A=(dam*ammo)/((rof*ammo)+loadt)
    A/=50
print('damage done sector = '+str(A))

'''dam=float(input('Damage: '))
aim=float(input('Aim time: '))
mdps=dam/aim
acc=float(input('Accuracy: '))
eva=float(input('Agility/dodge: '))
accel=float(input('Acceleration: '))
maxvel=float(input('Maximum velocity: '))
endur=float(input('Time at full speed: '))
dccel=float(input('Decceleration: '))
minvel=float(input('Jogging Pace: '))
hp=float(input('Total hit points: '))
#should have an end score of about -2.3

saved sets below
    dam:20  aim:1   acc:80  eva:35  accel:0.1   maxvel:1.2  minvel:0.1  dec:0.2 endur:10    hp:500  score=8.4
    dam:4   aim:0.1 acc:92  eva:9   accel:0.3   maxvel:1.8  minvel:0.5  dec:0.1 endur=5     hp:349  score=-2.30198


dist=0
vel=0
state='accel'
score=0
posscore=0
negscore=0

d=5

e1_state='fire'
e1_wait=0
e1_load=5
e2_state='wait'
e2_wait=0.2
e2_load=5.5
e3_state='wait'
e3_wait=0.5
e3_load=5.5


for x in range(0,601):
    edps=0
    if e1_state=='fire':
        edps+=10*d/7
    if e2_state=='fire':
        edps+=10*d/7
    if e3_state=='fire':
        edps+=10*d/7
    edps*=(100-eva)/100
    
    sec=x/10
    if state=='accel':
        vel+=accel
        if vel>=maxvel:
            vel=maxvel
            state='sprint'
            print('reached full speed at '+str(sec)+' sec')
            tire_time=x/10+endur
    elif state=='sprint' and sec>tire_time:
        state='decel'
        vel-=dccel
        print('slowing at '+str(sec)+' sec')
    elif state=='decel':
        vel-=dccel
        if vel<=minvel:
            vel=minvel
            state='jog'
            print('jogging at '+str(sec)+' sec')
    dist+=vel
    if dist>=100 and vel!=0:
        print('arrived at '+str(sec)+' sec')
        state='wait'
        wait_time=sec+aim
        vel=0
    elif state=='wait' and sec>=wait_time:
        state='fire'
    if state=='fire':
        posscore+=(dam*acc/100)/500
        state='wait'
        wait_time=sec+aim
    
    if x/10>=e1_load:
        e1_state='load'
        e1_wait=sec+2
        e1_load=sec+7
    elif e1_wait<=x/10:
        if e1_state=='load':
            e1_state='fire'
            e1_wait+=0.5
        elif e1_state=='fire':
            if state!='hide':
                negscore-=(d*((100-eva)/100))/hp
            e1_wait+=0.5
    
    if x/10>=e2_load:
        e2_state='load'
        e2_wait=x/10+2
        e2_load=x/10+7
    elif e2_wait<=x/10:
        if e2_state=='load' or e2_state=='wait':
            e2_state='fire'
            e2_wait+=0.5
        elif e2_state=='fire':
            if state!='hide':
                negscore-=(d*((100-eva)/100))/hp
            e2_wait+=0.5
            
    if x/10>=e3_load:
        e3_state='load'
        e3_wait=x/10+2
        e3_load=x/10+7
    elif e3_wait<=x/10:
        if e3_state=='load' or e3_state=='wait':
            e3_state='fire'
            e3_wait+=0.5
        elif e3_state=='fire':
            if state!='hide':
                negscore-=(d*((100-eva)/100))/hp
            e3_wait+=0.5
        
print(posscore)
print(negscore)
print(100*(posscore+negscore))
'''
