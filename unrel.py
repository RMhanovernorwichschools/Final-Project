'''IMPORTANT NOTES:
A / damage done(*5): is ratio of dps divided by 50
B / damage taken(*5): is % of damage taken by an enemy firing from all(0) to none(1)
C / stealth(*2): is % of time when enemy while mem is hiding from never(1) to always(0)
D / perception(*2): is % of time when hiding enemy is found from always(1) to never(0)
E / done damage control(*3): is ratio of dps divided by n in transition from best to worst case scenario in five steps
F / taken damage control(*3): is % of damage taken by enemy in transition to best to worst case scenario in five steps
G / aid to mems(*5): is change in mems damage(done and taken) (three steps, 1,2,4 mems) from *1(0) to *2.5(1)
'''

def contain (it,lt):
    checks=0
    for x in lt:
        if x==it:
            return True
        else:
            checks+=1
    if checks==len(lt):
        return False
        
def ID_trueacc (gacc):
    tofina=[]
    for x in [0,20,40,60,80,100]:
        e1=0.5**(1.03**(gacc-x))
        tofina.append(e1)
    return (sum(tofina)/len(tofina))
    
def ID_trueeva (geva):
    tofine=[]
    for x in [0,20,40,60,80,100]:
        e1=0.5**(1.03**(x-geva))
        tofine.append(e1)
    return (sum(tofine)/len(tofine))
    
def ID_truestel (ear, eye):
    tofins=[]
    for x in [0,20,40,60,80,100]:
        chance_notheard=0.5**(1.05**(x-(ear+5)))
        eye_miss = 0.8**(1.05**(x-(eye+5)))
        alerted_found = (1-eye_miss) + 0.5
        if alerted_found>1:
            alerted_found=1
        otherwise_found=(alerted_found-0.45)
        if otherwise_found<0:
            otherwise_found=0
        fully_found=(1-chance_notheard)*alerted_found
        a=fully_found
        fully_found+=(chance_notheard  * otherwise_found)
        alerted=(1-chance_notheard)*(1-alerted_found)
        undetec=chance_notheard*(1-otherwise_found)
        score=(1*fully_found)+(0.5*alerted)+(0*undetec)
        tofins.append(score)
    return 1-(sum(tofins)/len(tofins))

def ID_trueper (ear, eye):
    tofinp=[]
    for x in [0,20,40,60,80,100]:
        chance_notheard=0.5**(1.05**(ear-x))
        chance_notseen = 0.8**(1.05**(eye-x))
        chance_missed = chance_notheard *chance_notseen
        tofinp.append(1-chance_missed)
    return (sum(tofinp)/len(tofinp))
        

#the special ability that the mem can use
buff_A=['SE_acc', 'SE_rof']
buff_B='none'
buff_C='none'
buff_D='none'
buff_E='none'
buff_F='none'
buff_G='none'

#damage per shot in hp
dam=20
#accuracy on average
acc=60
#time to aim/shoot (time between deciding to fire and doing so) in seconds
rof=0.4
#shots fired before load necessary
ammo=20
#time it takes to load after full shots have been fired
loadt=1

A_acc=1-ID_trueacc(acc)
preA_1=(A_acc)*(dam*ammo)/((rof*ammo)+loadt)
preA_1/=50
if buff_A=='none':
    A=preA_1
else:
    #seconds load time for buff
    A_buffload=8
    #seconds for which buff lasts
    A_bufflen=2.1
    
    if contain ('SE_acc', buff_A):
        #% increase to accuracy
        accbuff=-50
        modacc=A_acc*(1+accbuff/100)
    else:
        modacc=A_acc
    if contain ('SE_dam', buff_A):
        #% increase to damage
        dambuff=40
        moddam=dam*(1+dambuff/100)
    else:
        moddam=dam
    if contain('SE_rof',buff_A):
        #% decrease to time it takes to fire
        rofbuff=80
        modrof=rof*(1-rofbuff/100)
    else:
        modrof=rof
    preA_2=(modacc)*(moddam*ammo)/((modrof*ammo)+loadt)
    preA_2/=50
    A=((preA_1*A_buffload)+(preA_2*A_bufflen))/(A_buffload+A_bufflen)
print('damage done sector = '+str(A))


#% chance of dodging each shot
dodge=50
#total hp
hp=500

B_dam=1-ID_trueeva(dodge)
pre_B=(hp-(400*B_dam))/hp
if buff_B=='none':
    B=pre_B
else:
    #seconds load time for buff
    A_buffload=8
    #seconds for which buff lasts
    A_bufflen=2.1
    
    if contain('SE_eva',buff_B):
        #% increase to evasion
        evabuff=60
        modeva=dodge*evabuff/100
    else:
        modeva=dodge
    if contain('SE_toughness',buff_B):
        #% decrease from 100% of damage taken per point dealt
        tufbuff=0.45
    else:
        tufbuff=0
        
    post_B_dam=1-ID_trueeva(modeva)
    dam_taken_buff=(400*post_B_dam)*(1-tufbuff)
    post_B=(hp-dam_taken_buff)/hp
    B=((pre_B*buffload)+(post_B*bufflen))/(bufflen+buffload)
    
print('damage taken sector = '+str(B))


#score for quietness while sneaking (around 0 to 100)
stel_sound=50
#score for visual discretion whle sneaking (around 0 to 100)
stel_visi=65

if buff_C=='none':
    C=ID_truestel(stel_sound, stel_visi)
print('stealth sector = '+str(C))


#score for visual perception (seeing things hard to see 0 to 100)
vis=50
#score for auditory perception (hearing things hard to hear 0 to 100)
ear=50
#% resistance to darkness debuff
night_vis=0.1
#% resistance to fog/other blockage debuff
bad_vis=0.05
#% resistance to distracting sounds, etc.
bad_ear=0
#The way visibility decreases is by 0 (where chance to see is x1.00) to 1 (where chance to see if x0.00)
#If bad_vis is 50%, for example, then a fog of factor 0.5 will only lead a x0.75 chance to see instead of a x0.50

if buff_D=='none':
    D_1=ID_trueper(ear,vis)
    D_emer=[]
    for x in [0.1,0.2,0.5,0.8,0.9]:
        vis_obstruct_dark=1-(x*(1-night_vis))
        vis_obstruct_etc=1-(x*(1-bad_vis))
        vis_obstruct=vis_obstruct_etc*vis_obstruct_dark
        ear_obstruct=1-(x*(1-bad_ear))
        c_hear=ear_obstruct*ear
        c_see=vis_obstruct*vis
        D_emer.append(ID_trueper(c_hear,c_see))
    D_2= sum(D_emer)/len(D_emer)
D = ((D_1+D_2)/2)
print('perception sector = '+str(D))


#how efficacy decreases as hp does, first with rate (efficacy = eff*(hp/total)^damcontrol) then bonus_a (ex. +50% or +10% efficacy)
#next component is bonus_b which is stronger b/c not percent)
dam_control=[1,0.6,0.15]
#specifically the things that decrease with damage done are accuracy to 0 and rof turns to 1.5x
#this improves as [a,b,c] where a decreases and b and c increase

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
        mod_acc=1-ID_trueacc(mod_acc)
        E_sub=(mod_acc)*(dam*ammo)/((mod_rof*ammo)+loadt)
        E_sub/=50
        E_list.append(E_sub)
E = (sum(E_list)/len(E_list))/A
print ('done damage control sector = '+str(E))


#similar to done damage control, but only evasion is affected to 0, with rate, bonus_a and bonus_b
eva_control=[1,0.6,0.05]

if buff_F=='none':
    F_list=[]
    for x in (0.8,0.6,0.4,0.2,0.05):
        me=(x+(eva_control[1]*x)+eva_control[2])
        if me>1:
            me=1
        mod_eva=(dodge)*(me**eva_control[0])
        F_sub=(ID_trueeva(mod_eva))/ID_trueeva(dodge)
        F_list.append(F_sub)
F = sum(F_list)/len(F_list)
print ('taken damage control sector = '+str(F))

if buff_G=='none':
    G=0
print ('aid to mem sector = '+str(G))

final=(5*A+5*B+2*C+2*D+3*E+3*F+5*G)/25
print('overall = '+str(final))
