'''IMPORTANT NOTES:
A / damage done(*5): is ratio of dps divided by 50
B / damage taken(*5): is % of damage taken by an enemy firing from all(0) to none(1)
C / stealth(*2): is % of time when enemy while mem is hiding from never(1) to always(0)
D / perception(*2): is % of time when hiding enemy is found from always(1) to never(0)
E / done damage control(*3): is ratio of dps divided by n in transition from best to worst case scenario in five steps
F / taken damage control(*3): is % of damage taken by enemy in transition to best to worst case scenario in five steps
G / aid to mems(*5): is change in mems damage(done and taken) (three steps, 1,2,4 mems) from *1(0) to *2.5(1)
'''

#the special ability that the mem can use
buff_A='none'
buff_B='none'
buff_C='none'
buff_D='none'
buff_E='none'
buff_F='none'

#damage per shot in hp
dam=20
#accuracy on average
acc=75
#time to aim/shoot (time between deciding to fire and doing so) in seconds
rof=0.4
#shots fired before load necessary
ammo=20
#time it takes to load after full shots have been fired
loadt=1

if buff_A=='none':
    A=(acc/100)*(dam*ammo)/((rof*ammo)+loadt)
    A/=50
print('damage done sector = '+str(A))


#% chance of dodging each shot
dodge=50
#total hp
hp=500

if buff_B=='none':
    enemshots=400*(dodge/100)
    enemshots=400-enemshots
    B=1-(enemshots/hp)
print('damage taken sector = '+str(B))


#% chance of being seen when enemy is not on alert
visi=0.33
#%chance of being seen when enemy is on alert
al_visi=(visi**(1/2))*1.5
if al_visi>1:
    al_visi=1
#% chance of alerting enemy while moving with sound
stealth=0.4

if buff_C=='none':
    C=1-((stealth*al_visi)+(stealth*0.5*(1-al_visi))+((1-stealth)*visi))
print('stealth sector = '+str(C))


#increased (or decreased) likelihood to spot hidden enemies
vis=0
#increased (or decreased) likelihood to hear enemies moving
ear=0
#% resistance to darkness debuff
night_vis=0.1
#% resistance to fog/other blockage debuff
bad_vis=0.05
#The way visibility decreases is by 0 (where chance to see is x1.00) to 1 (where chance to see if x0.00)
#If bad_vis is 50%, for example, then a fog of factor 0.5 will only lead a x0.75 chance to see instead of a x0.50

if buff_D=='none':
    D_1=(0.5+ear)+(1-(0.5+ear))*(0.5+vis)
    D_emer=[]
    for x in [0.1,0.2,0.5,0.9]:
        vis_obstruct=(1-x)+(night_vis+bad_vis)/2
        if vis_obstruct>1:
            vis_obstruct=1
        D_emer.append(D_1*vis_obstruct)
    D_2= sum(D_emer)/len(D_emer)
D = ((D_1+D_2)/2)
print('perception sector = '+str(D))


#how efficacy decreases as hp does, first with rate (efficacy = eff*(hp/total)^damcontrol) then bonus_a (ex. +50% or +10% efficacy)
#next component is bonus_b which is stronger b/c not percent)
dam_control=[1,0.6,0.2]
#specifically the things that decrease with damage done are accuracy to 0 and rof turns to 1.5x

if buff_E=='none':
    E_list=[]
    for x in (0.8,0.6,0.4,0.2,0.05):
        mr=((1-x)-(dam_control[1]*(1-x))-dam_control[2])
        if mr<0:
            mr=0
        mod_rof=rof*1 + rof*0.5*(mr**dam_control[0])
        ma=(x+(dam_control[1]*x)+dam_control[2])
        if ma>1:
            ma=1
        mod_acc=acc*(ma**dam_control[0])
        E_sub=(mod_acc/100)*(dam*ammo)/((mod_rof*ammo)+loadt)
        E_sub/=50
        E_list.append(E_sub)
E = sum(E_list)/len(E_list)
print ('done damage control sector = '+str(E))


#similar to done damage control, but only evasion is affected to 0, with rate, bonus_a and bonus_b
eva_control=[1,0.6,0.2]

if buff_F=='none':
    F_list=[]
    for x in (0.8,0.6,0.4,0.2,0.05):
        me=(x+(eva_control[1]*x)+eva_control[2])
        if me>1:
            me=1
        mod_eva=(dodge/100)*(me**eva_control[0])
        F_enemdam=400*mod_eva
        F_enemdam=400-F_enemdam
        F_sub=1-(F_enemdam/hp)
        F_list.append(F_sub)
F = sum(F_list)/len(F_list)
print ('taken damage control sector = '+str(F))


final=(5*A+5*B+2*C+2*D+3*E+3*F)/20
print('overall = '+str(final))

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
