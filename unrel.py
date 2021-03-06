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
buff_A='rof buff and dam buff'
buff_B='none'
buff_C='none'
buff_D='percep debuff'
buff_E='none'
buff_F='none'
buff_G='none'

#damage per shot in hp
dam=8
#accuracy on average
acc=39
#time to aim/shoot (time between deciding to fire and doing so) in seconds
rof=0.15
#shots fired before load necessary
ammo=30
#time it takes to load after full shots have been fired
loadt=0.6

A_acc=1-ID_trueacc(acc)
preA_1=(A_acc)*(dam*ammo)/((rof*ammo)+loadt)
preA_1/=50
if buff_A=='none':
    A=preA_1
else:
    #seconds load time for buff
    A_buffload=7
    #seconds for which buff lasts
    A_bufflen=3
    
    #effect to accuracy (adds, multiplies, etc.)
    def A_sab(x):
        return x
    #effect detriment to enems evasion
    def A_eed(x):
        return x
    A_tofina=[]
    for x in [0,20,40,60,80,100]:
        e1=0.5**(1.03**(A_sab(acc)-A_eed(x)))
        A_tofina.append(e1)
    modacc= 1-(sum(A_tofina)/len(A_tofina))
    #effect to own damage
    def A_sdb(x):
        return x+5
    #effect detriment to enems toughness (example, 0.1 means they take 1.1 dam for every 1 dealt.)
    A_tuff_debuff=0
    moddam=A_sdb(dam) * (1+A_tuff_debuff)
    #effect to rof
    def A_srb(x):
        return x*0.5
    modrof=A_srb(rof)
    #additional damage done by separate attack and %chance of this attack succeeding (ex. grenade fire, modacc for normal chance)
    A_addidam=[0,modacc]
    addidam= A_addidam[0]*A_addidam[1]
    
    preA_2=( (modacc)*(moddam*ammo)/((modrof*ammo)+loadt) ) + addidam/A_bufflen
    preA_2/=50
    A=((preA_1*A_buffload)+(preA_2*A_bufflen))/(A_buffload+A_bufflen)
print('damage done sector = '+str(A))


#% chance of dodging each shot
dodge=91
#total hp
hp=290

B_dam=1-ID_trueeva(dodge)
pre_B=(hp-(400*B_dam))/hp
if buff_B=='none':
    B=pre_B
else:
    #seconds load time for buff
    B_buffload=1
    #seconds for which buff lasts
    B_bufflen=0
    
    #effect to evasion
    def B_seb(x):
        return x
    #effect detriment to enems acc
    def B_ead(x):
        return x
    B_tofine=[]
    for x in [0,20,40,60,80,100]:
        e1=0.5**(1.03**(B_ead(x)-B_seb(dodge)))
        B_tofine.append(e1)
    modeva = (sum(B_tofine)/len(B_tofine))
    #effect on own toughness (decrease from 100% of damage taken per point dealt)
    tufbuff=0
    #effect detriment on enems rof (note - cannot exceed 0.4)
    def B_erd(x):
        return x
    #effect detriment on enems damage (note - cannot exceed 10)
    def B_edd(x):
        return x
    #own self-heal ability (number of hp that can be restored)
    B_heal=0
        
    post_B_dam=1-modeva
    B_enemdam=(B_edd(10)/B_erd(0.4))*16
    dam_taken_buff=(B_enemdam*post_B_dam)*(1-tufbuff)
    post_B=(B_heal+hp-dam_taken_buff)/hp
    B=((pre_B*B_buffload)+(post_B*B_bufflen))/(B_bufflen+B_buffload)
    
print('damage taken sector = '+str(B))


#score for quietness while sneaking (around 0 to 100)
stel_sound=15
#score for visual discretion whle sneaking (around 0 to 100)
stel_visi=15

C_default=ID_truestel(stel_sound, stel_visi)
if buff_C=='none':
    C=C_default
else:
    #time in secs for which buff lasts
    C_bufflen=0
    #time in secs which buff requires to be ready
    C_buffload=1
    
    #effect on own visual stealth (how easy to see)
    def C_svs(x):
        return x
    #effect on own auditory stealth (how easy to hear)
    def C_sss(x):
        return x
    #effect on enems visual perception
    def C_evp(x):
        return x/1.4 - 5
    #effect on enems auditory perception
    def C_esp(x):
        return x-55
        
    C_tofins=[]
    for x in [0,20,40,60,80,100]:
        chance_notheard=0.5**(1.05**(C_esp(x)-(C_sss(stel_sound)+5)))
        eye_miss = 0.8**(1.05**(C_evp(x)-(C_svs(stel_visi)+5)))
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
        C_tofins.append(score)
    C_buff = 1-(sum(C_tofins)/len(C_tofins))
    
    C=((C_buff*C_bufflen)+(C_default*C_buffload))/(C_bufflen+C_buffload)
    
print('stealth sector = '+str(C))


#score for visual perception (seeing things hard to see 0 to 100)
vis=18
#score for auditory perception (hearing things hard to hear 0 to 100)
ear=7
#% resistance to darkness debuff
night_vis=0
#% resistance to fog/other blockage debuff
bad_vis=0
#% resistance to distracting sounds, etc.
bad_ear=0
#The way visibility decreases is by 0 (where chance to see is x1.00) to 1 (where chance to see if x0.00)
#If bad_vis is 50%, for example, then a fog of factor 0.5 will only lead a x0.75 chance to see instead of a x0.50

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
D_default = ((D_1+D_2)/2)

if buff_D=='none':
    D = D_default
else:
    #time in secs for which buff lasts
    D_bufflen=3
    #time in secs which buff requires to be ready
    D_buffload=7
    
    #effect on visual perception
    def D_vis(x):
        return x/2
    #effect on auditory perception
    def D_ear(x):
        return x-10
    #effect on enem visual stealth 
    def D_evs(x):
        return x
    #effecton enem auditory stealth 
    def D_ess(x):
        return x
        
    def D_bufffind(ear,eye):
        D_tofinp=[]
        for x in [0,20,40,60,80,100]:
            chance_notheard=0.5**(1.05**(ear-D_ess(x)))
            chance_notseen = 0.8**(1.05**(eye-D_evs(x)))
            chance_missed = chance_notheard *chance_notseen
            D_tofinp.append(1-chance_missed)
        return (sum(D_tofinp)/len(D_tofinp))
    D_buff_1=D_bufffind(D_ear(ear),D_vis(vis))
    
    DB_emer=[]
    for x in [0.1,0.2,0.5,0.8,0.9]:
        vis_obstruct_dark=1-(x*(1-night_vis))
        vis_obstruct_etc=1-(x*(1-bad_vis))
        vis_obstruct=vis_obstruct_etc*vis_obstruct_dark
        ear_obstruct=1-(x*(1-bad_ear))
        c_hear=ear_obstruct*D_ear(ear)
        c_see=vis_obstruct*D_vis(vis)
        DB_emer.append(D_bufffind(c_hear,c_see))
    D_buff_2= sum(DB_emer)/len(DB_emer)
    D_buff = ((D_buff_1+D_buff_2)/2)
    D=((D_buff*D_bufflen)+(D_default*D_buffload))/(D_bufflen+D_buffload)
    
print('perception sector = '+str(D))

#how efficacy decreases as hp does, first with rate (efficacy = eff*(hp/total)^damcontrol) then bonus_a (ex. +50% or +10% efficacy)
#next component is bonus_b which is stronger b/c not percent)
dam_control=[1.1,1.2,0.6]
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
E = (sum(E_list)/len(E_list))
E_gen= E/A
print ('done damage control sector = '+str(E)+' ('+str(E_gen)+')')


#similar to done damage control, but only evasion is affected to 0, with rate, bonus_a and bonus_b
eva_control=[1.2,0.8,0]

if buff_F=='none':
    F_list=[]
    for x in (0.8,0.6,0.4,0.2,0.05):
        me=(x+(eva_control[1]*x)+eva_control[2])
        if me>1:
            me=1
        mod_eva=(dodge)*(me**eva_control[0])
        F_sub=ID_trueeva(mod_eva)
        F_list.append(F_sub)
F = sum(F_list)/len(F_list)
F_gen = F/ID_trueeva(dodge)
print ('taken damage control sector = '+str(F)+' ('+str(F_gen)+')')

if buff_G=='none':
    G=0
else:
    G_default_1=(400*(1-ID_trueeva(50)))/500
    #effect to mem evasion (function applied to x is how they will affect the mem's evasion, for example, *2 or +20)
    def G_meb(x):
        return x
    #effect to mem hp (same as above)
    def G_hpb(x):
        return x
    #effect to enem damage (same as above)
    def G_damd(x):
        return x
    #effect to enemy accuracy
    def G_accd(x):
        return x
    
    G_tofine=[]
    for x in [0,20,40,60,80,100]:
        e1=0.5**(1.03**((G_accd(x))-(G_meb(50))))
        G_tofine.append(e1)
    G_eva_return = (sum(G_tofine)/len(G_tofine))
    G_buff_1=((G_damd(400))*(1-G_eva_return))/(G_hpb(500))
    
    #how long is the buff active? (seconds)
    GA_bufflen=0
    #how long does it take to load/prepare? (seconds)
    GA_buffload=1
    G_1=(GA_bufflen*(G_default_1-G_buff_1))/((GA_bufflen+GA_buffload)*G_default_1)
    
    G_default_2=12*((1-ID_trueacc(50))*100/2.8)/300
    #effect to mem accuracy (function applied to x is how they will affect the mem's acc, for example, *2 or +20)
    def G_mab(x):
        return x
    #effect to mem damage (same as above)
    def G_damb(x):
        return x
    #effect to enem evasion (same as above)
    def G_eed(x):
        return x/2 -15
    #effect to enemy health
    def G_hpd(x):
        return x
        
    G_tofind=[]
    for x in [0,20,40,60,80,100]:
        e1=0.5**(1.03**(G_mab(50)-G_eed(x)))
        G_tofind.append(e1)
    G_acc_return = (sum(G_tofind)/len(G_tofind))
    G_buff_2=12*((1-G_acc_return)*5*G_damb(20)/2.8)/G_hpd(300)
    
    #how long is the buff active? (seconds)
    GB_bufflen=4.5
    #how long does it take to load/prepare? (seconds)
    GB_buffload=10
    G_2=(G_buff_2-G_default_2)*GB_bufflen/(G_default_2*(GB_bufflen+GB_buffload))
    
    G_default_3=ID_truestel(50,65)
    #effect to mem visi stealth (function applied to x is how they will affect the mem's acc, for example, *2 or +20)
    def G_mvsb(x):
        return x
    #effect to mem sound stealth (same as above)
    def G_mssb(x):
        return x
    #effect to enem sound perception (same as above)
    def G_essd(x):
        return x-55
    #effect to enemy sight perception
    def G_evsd(x):
        return (x/1.4)-5
    
    G_tofins=[]
    for x in [0,20,40,60,80,100]:
        chance_notheard=0.5**(1.05**(G_essd(x)-G_mssb(50)-5))
        eye_miss = 0.8**(1.05**((G_evsd(x)-G_mvsb(65))-5))
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
        G_tofins.append(score)
    G_buff_3 = 1-(sum(G_tofins)/len(G_tofins))
    
    #how long is the buff active? (seconds)
    GC_bufflen=9
    #how long does it take to load/prepare? (seconds)
    GC_buffload=12
    G_3=(G_buff_3-G_default_3)*GC_bufflen/(G_default_3*(GC_bufflen+GC_buffload))
    
    G_default_4A=ID_trueper(50,50)
    GA_emer=[]
    for x in [0.1,0.2,0.5,0.8,0.9]:
        vis_obstruct_dark=1-(x*(1-0.1))
        vis_obstruct_etc=1-(x*(1-0.05))
        vis_obstruct=vis_obstruct_etc*vis_obstruct_dark
        ear_obstruct=1-(x*(1-0.01))
        c_hear=ear_obstruct*50
        c_see=vis_obstruct*50
        GA_emer.append(ID_trueper(c_hear,c_see))
    G_default_4B= sum(GA_emer)/len(GA_emer)
    G_default_4=(G_default_4A+G_default_4B)/2
    #effect on visual perception (works as described above)
    def G_mvpb(x):
        return x
    #effect to mem auditory perception (same as above)
    def G_mspb(x):
        return x*1.3 +15
    #effect to mems sound distraction resistance (should be decimals)
    def G_msprb(x):
        return x
    #effect to mems visual distraction/blockage resistance (should be decimals)
    def G_mvprb(x):
        return x
    #effect to enem visual stealth (same as above)
    def G_evpd(x):
        return x
    #effect to enemy auditory stealth
    def G_espd(x):
        return x
    
    def G_percep(a,b):
        G_tofinp=[]
        for x in [0,20,40,60,80,100]:
            chance_notheard=0.5**(1.05**(G_mspb(a)-G_espd(x)))
            chance_notseen = 0.8**(1.05**(G_mvpb(b)-G_evpd(x)))
            chance_missed = chance_notheard *chance_notseen
            G_tofinp.append(1-chance_missed)
        return(sum(G_tofinp)/len(G_tofinp))
    G_buff_4A=G_percep(50,50)
    G_emer=[]
    for x in [0.1,0.2,0.5,0.8,0.9]:
        vis_obstruct_dark=1-(x*(1-G_mvprb(0.1)))
        vis_obstruct_etc=1-(x*(1-G_mvprb(0.05)))
        vis_obstruct=vis_obstruct_etc*vis_obstruct_dark
        ear_obstruct=1-(x*(1-G_msprb(0.01)))
        c_hear=ear_obstruct*50
        c_see=vis_obstruct*50
        G_emer.append(G_percep(c_hear,c_see))
    G_buff_4B= sum(G_emer)/len(G_emer)
    G_buff_4=(G_buff_4A+G_buff_4B)/2
    
    #how long is the buff active? (seconds)
    GD_bufflen=1
    #how long does it take to load/prepare? (seconds)
    GD_buffload=0
    G_4=(G_buff_4-G_default_4)*GD_bufflen/(G_default_4*(GD_bufflen+GD_buffload))
    
    G=(3*G_1+3*G_2+G_3+G_4)/8
    
    #how many mems total can it affect?
    G_buff_range=3
    
    if G_buff_range>2:
        G*=1
    elif G_buff_range==2:
        G*=0.917
    elif G_buff_range==1:
        G*=0.75
    else:
        G*=0.5
        
print ('aid to mem sector = '+str(G))

final=(5*A+5*B+2*C+2*D+3*E+3*F+10*G)/30
print('overall = '+str(final))

''' Below are combinations that lead to the desired final score of around 0.3398539295292792
|||||COMBO ONE
#the special ability that the mem can use
buff_A=['acc loss', 'rof boost']
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
    #seconds load time for buff
    A_buffload=8
    #seconds for which buff lasts
    A_bufflen=2.1
    #effect to accuracy (adds, multiplies, etc.)
    def A_sab(x):
        return x-50
    #effect to rof
    def A_srb(x):
        return x*0.15
#% chance of dodging each shot
dodge=50
#total hp
hp=500
#score for quietness while sneaking (around 0 to 100)
stel_sound=50
#score for visual discretion whle sneaking (around 0 to 100)
stel_visi=65
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
#how efficacy decreases as hp does, first with rate (efficacy = eff*(hp/total)^damcontrol) then bonus_a (ex. +50% or +10% efficacy)
#next component is bonus_b which is stronger b/c not percent)
dam_control=[1,0.6,0.15]
#similar to done damage control, but only evasion is affected to 0, with rate, bonus_a and bonus_b
eva_control=[1,0.6,0.05]
|||||

|||||COMBO TWO
#the special ability that the mem can use
buff_A='none'
buff_B='none'
buff_C='enem percep debuff'
buff_D='percep boost'
buff_E='none'
buff_F='none'
buff_G=['enem percep debuff', 'percep boost']

#damage per shot in hp
dam=12
#accuracy on average
acc=80
#time to aim/shoot (time between deciding to fire and doing so) in seconds
rof=0.74
#shots fired before load necessary
ammo=15
#time it takes to load after full shots have been fired
loadt=1.15
#% chance of dodging each shot
dodge=80
#total hp
hp=265
#score for quietness while sneaking (around 0 to 100)
stel_sound=98
#score for visual discretion whle sneaking (around 0 to 100)
stel_visi=78
    #time in secs for which buff lasts
    C_bufflen=9
    #time in secs which buff requires to be ready
    C_buffload=12
    #effect on enems visual perception
    def C_evp(x):
        return x/1.4 - 5
    #effect on enems auditory perception
    def C_esp(x):
        return x-55
#score for visual perception (seeing things hard to see 0 to 100)
vis=95
#score for auditory perception (hearing things hard to hear 0 to 100)
ear=100
#% resistance to darkness debuff
night_vis=0.65
#% resistance to fog/other blockage debuff
bad_vis=0.6
#% resistance to distracting sounds, etc.
bad_ear=0.8
    #time in secs for which buff lasts
    D_bufflen=9
    #time in secs which buff requires to be ready
    D_buffload=12
    #effect on visual perception
    def D_vis(x):
        return (x*1.1)
    #effect on auditory perception
    def D_ear(x):
        return x+51
#how efficacy decreases as hp does, first with rate (efficacy = eff*(hp/total)^damcontrol) then bonus_a (ex. +50% or +10% efficacy)
#next component is bonus_b which is stronger b/c not percent)
dam_control=[0.5,0.8,0.4]
#similar to done damage control, but only evasion is affected to 0, with rate, bonus_a and bonus_b
eva_control=[0.7,0.7,0.06]
    #effect to enem sound perception (same as above)
    def G_essd(x):
        return x-55
    #effect to enemy sight perception
    def G_evsd(x):
        return (x/1.4)-5
    #how long is the buff active? (seconds)
    GC_bufflen=9
    #how long does it take to load/prepare? (seconds)
    GC_buffload=12
    #effect to mem auditory perception (same as above)
    def G_mspb(x):
        return x*1.3 +15
    #how long is the buff active? (seconds)
    GD_bufflen=1
    #how long does it take to load/prepare? (seconds)
    GD_buffload=0
#how many mems total can G_buffs affect?
G_buff_range=3
||||||
'''