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
#reasonable range runs from 5 to 67, so converts from 0,100 range
cau=(cau*62/100)+5
hp=float(input('Total hit points: '))

dist=0
vel=0
state='accel'
score=0
posscore=0
negscore=0

e1_state='fire'
e1_wait=0
e1_load=5
e2_state='wait'
e2_wait=2.0
e2_load=7.0
e3_state='wait'
e3_wait=5.0
e3_load=10.0


    for x in range(0,301):
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
                tire_time=x/10+endur
        elif state=='sprint' and sec>tire_time:
            state='decel'
            vel-=dccel
        elif state=='decel':
            vel-=dccel
            if vel<=minvel:
                vel=minvel
                state='jog'
        if state=='fire':
            posscore+=(dam*acc/100)/500
            state='wait'
            wait_time=sec+aim
        dist+=vel
        if dist>=10 and vel!=0:
            state='wait'
            wait_time=sec+aim
            vel=0
        elif state=='wait' and sec>=wait_time:
            state='fire'
        
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
print(posscore+negscore)
