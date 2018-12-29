dam=float(input('Damage: '))
aim=float(input('Aim time: '))
mdps=dam/aim
acc=float(input('Accuracy: '))
eva=float(input('Agility/dodge: '))
accel=float(input('Acceleration: '))
maxvel=float(input('Maximum velocity: '))
endur=float(input('Time at full speed: '))
dccel=float(input('Decceleration: '))
minvel=float(input('Jogging Pace: '))
cau=float(input('Caution: '))
hp=float(input('Total hit points: '))

dist=0
vel=0
state='accel'
score=0

def analyze(risk):
    return(((risk/hp)/(2*mdps/500))**((100-cau)/40))
    
e1_state='fire'
e1_wait=0
e1_load=5
e2_state='wait'
e2_wait=0.5
e2_load=5.5
e3_state='wait'
e3_wait=1.0
e3_load=6

for x in range(0,301):
    edps=0
    if e1_state=='fire':
        edps+=50/7
    if e2_state=='fire':
        edps+=50/7
    if e3_state=='fire':
        edps+=50/7
    
    sec=x/10
    if state=='accel':
        vel+=accel
        if vel>=maxvel:
            vel=maxvel
            state='sprint'
            tire_time=x/10+endur
    elif state=='sprint' and x/10>tire_time:
        state='decel'
        vel-=dccel
    elif state=='decel':
        vel-=dccel
        if vel<=minvel:
            vel=minvel
            state='jog'
    if state=='analyze':
        print(analyze(edps))
        if analyze(edps)<=0.5:
            score+=dam*acc/100
            state='wait'
            wait_time=(x/10)+aim
    dist+=vel
    if dist>=10 and state!='wait':
        state='wait'
        wait_time=(x/10)+aim
        vel=0
    elif state=='wait' and x/10>=wait_time:
        state='analyze'
    
    if x/10>=e1_load:
        e1_state='load'
        e1_wait=x/10+2
        e1_load=x/10+7
    elif e1_wait<=x/10:
        if e1_state=='load':
            e1_state='fire'
            e1_wait+=0.5
        elif e1_state=='fire':
            score-=(5*((100-eva)/100))/hp
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
            score-=(5*((100-eva)/100))/hp
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
            score-=(5*((100-eva)/100))/hp
            e3_wait+=0.5
            
print(score)
