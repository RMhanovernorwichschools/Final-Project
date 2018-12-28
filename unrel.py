dam=float(input('Damage: '))
aim=float(input('Aim time: '))
mdps=dam/aim
acc=float(input('Accuracy: '))
eva=float(input('Agility/dodge: '))
accel=float(input('Acceleration: '))
maxvel=float(input('Maximum velocity: '))
cau=float(input('Caution: '))

dist=0
vel=0
state='accel'
score=0

def analyze(risk):
    return((risk/mdps)**(cau/100))
    
e1_state='fire'
e1_wait=0
e1_load=5
e2_state='wait'
e2_wait=0.5
e2_load=5.5
e3_state='wait'
e3_wait=1.0
e3_load=6

for x in range(0,201):
    edps=10
    sec=x/10
    if state=='accel':
        vel+=accel
        if vel>=maxvel:
            vel=maxvel
            state='sprint'
    
    if state=='analyze':
        if analyze(edps)<=0.5:
            score+=dam*acc/100
            state='wait'
            wait_time=(x/10)+aim
    dist+=vel
    if dist>=10:
        state='analyze'
        vel=0
    if state=='wait' and x>=wait_time:
        state='analyze'
    if x/10>e1_load:
        e1_state='load'
        e1_wait=x/10+2
        e1_load=x/10+7
    elif e1_wait<=x/10:
        if e1_state=='load':
            e1_state='fire'
        elif e1_state=='fire':
            score-=5*((100*eva)/100)
            e1_wait+=0.5
    print(score)
    
