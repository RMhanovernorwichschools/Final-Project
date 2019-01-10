import random

Names=['Willow', 'Lisbet', 'Cameron', 'Mariette', 'Annie', 'Luna', 'Celia']
Scents=['pine', 'lavender', 'lemon', 'soap', 'fish']
Shoes=['hiking shoes', 'worn sneakers', 'winter boots', 'rainboots', 'trail-runners']
BirthMons=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
Coats=['hoodie', 'sweater', 'raincoat', 'down jacket', 'sports coat', 'denim jacket']
Colors=['navy blue', 'pale blue', 'white', 'grey', 'black', 'beige']

lists=[Names, Scents, Shoes, BirthMons, Coats, Colors]
max=10

for x in lists:
    random.shuffle(x)
    if len(x)<max:
        max=len(x)

while True:
    item_num=int(input('How many items do you want the puzzle to contain? '))
    if item_num<=max:
        break
    else:
        print("Sorry, can't do that many.")
        
trait_list=list(input('''Now carefully enter the traits of the items using the following rules.
  -do not repeat traits
  -separate each trait with a /
  -choose from the following traits: color, coat, scent, shoe, name, month'''))
for x in trait_list:
    if x=='?' or x=='!' or x=='.' or x==' ':
        trait_list.remove(x)
  
traits=[]
split_loci=[]
for x in range(len(trait_list)):
    if trait_list[x]=='/':
        split_loci.append(x)
word=''
for x in range(0,split_loci[0]):
    word+=trait_list[x]
traits.append(word)
for a in range(len(split_loci)-1):
    word=''
    for x in range(split_loci[a]+1,split_loci[a+1]):
        word+=trait_list[x]
    traits.append(word)
word=''
for x in range(split_loci[-1]+1,len(trait_list)):
    word+=trait_list[x]
traits.append(word)

traits_fin=[]
for x in range(len(traits)):
    if traits[x]=='color':
        traits_fin.append([traits[x], Colors])
    elif traits[x]=='coat':
        traits_fin.append([traits[x], Coats])
    elif traits[x]=='scent':
        traits_fin.append([traits[x], Scents])
    elif traits[x]=='shoe':
        traits_fin.append([traits[x], Shoes])
    elif traits[x]=='name':
        traits_fin.append([traits[x], Names])
    elif traits[x]=='month':
        traits_fin.append([traits[x], BirthMons])
        
items=[]
class item():
    def __init__(self, n, title):
        self.loci=title
        self.name=Names[n]
        self.scent=Scents[n]
        self.shoe=Shoes[n]
        self.birthmon=BirthMons[n]
        self.coat=Coats[n]
        self.color=Colors[n]
        items.append(self)
        
    def return_list(self):
        message=[self.loci]
        for x in traits_fin:
            message.append(x[1][self.loci])
        return message

for x in range(item_num):
    a=item(x,x)
    print(a.return_list())
    
clues=[]
    
def generate_clue(x,fac,sep):
    global clues
    clue=[]
    f3=''
    if sep==0:
        p1='The girl in the {0} position'.format(x)
        f1=['loci', x]
    elif sep==1 or sep==2 or sep==3:
        a=random.choice(traits_fin)
        while a==fac:
            a=random.choice(traits_fin)
        if a[0]=='name':
            p1=a[1][x]
        elif a[0]=='month':
            p1='The girl born in {0}'.format(a[1][x])
        elif a[0]=='shoe' or a[0]=='color':
            p1='The girl wearing {0}'.format(a[1][x])
        elif a[0]=='scent':
            p1='The girl who smells of {0}'.format(a[1][x])
        elif a[0]=='coat':
            p1='The girl wearing the {0}'.format(a[1][x])
        f1=[a[0], a[1][x]]
    if sep==1 or sep==0:
        variety='link'
        if fac[0]=='name':
            p2=" is "+fac[1][x]
        elif fac[0]=='month':
            p2=' was born in {0}'.format(fac[1][x])
        elif fac[0]=='shoe' or fac[0]=='color':
            p2=' wears {0}'.format(fac[1][x])
        elif fac[0]=='scent':
            p2=' sort of smells like {0}'.format(fac[1][x])
        elif fac[0]=='coat':
            p2=' is wearing a {0}'.format(fac[1][x])
        f2=[fac[0], fac[1][x]]
    elif sep==3:
        variety='nonlink'
        y=x
        while y==x:
            y=random.choice(items).loci
        if fac[0]=='name':
            p2=" is not "+fac[1][y]
        elif fac[0]=='month':
            p2=" wasn't born in {0}".format(fac[1][y])
        elif fac[0]=='shoe' or fac[0]=='color':
            p2=" doesn't wear {0}".format(fac[1][y])
        elif fac[0]=='scent':
            p2=" doesn't smell like {0}".format(fac[1][y])
        elif fac[0]=='coat':
            p2=' is not wearing a {0}'.format(fac[1][y])
        f2=[fac[0], fac[1][y]]
    elif sep==2:
        b=random.randint(0,2)
        if x==items[-1].loci and b==1:
            b=random.randint(0,1)*2
        elif x==items[0].loci and b==2:
            b=random.randint(0,1)
        if b==0:
            p2=' is next to'
            if (random.randint(0,1)==0 and x!=items[0].loci) or x==items[-1].loci:
                partner=x-1
            else:
                partner=x+1
            variety='side'
        elif b==1:
            p2=' is exactly to the left of'
            partner=x+1
            variety='left'
        else:
            p2=' is exactly to the right of'
            partner=x-1
            variety='right'
        a=random.choice(traits_fin)
        if a[0]=='name':
            p3=a[1][partner]
        elif a[0]=='month':
            p3='the girl born in {0}'.format(a[1][partner])
        elif a[0]=='shoe' or a[0]=='color':
            p3='the girl wearing {0}'.format(a[1][partner])
        elif a[0]=='scent':
            p3='the girl who smells of {0}'.format(a[1][partner])
        elif a[0]=='coat':
            p3='the girl wearing the {0}'.format(a[1][partner])
        f2=[a[0], a[1][partner]]
        p2=p2+' '+p3
    clue=[variety, f1, f2, f3,p1+p2]
    clues.append(clue)

def sort_clues(lis):
    global clues
    for x in lis:
        m=0
        for a in lis:
            if x[4]==a[4]:
                remfrom(x,clues)
                m=1
            if m==0 and x[0]=='link' and a[0]=='link' and ((x[1][1]==a[1][1] and x[2][1]==a[2][1]) or (x[1][1]==a[2][1] and x[2][1]==a[1][1])):
                remfrom(x,clues)
                m=1
            if m==0 andx[0]=='side' and (a[0]=='left' or a[0]=='right') and ((x[1][1]==a[1][1] and x[2][1]==a[2][1]) or (x[1][1]==a[2][1] and x[2][1]==a[1][1])):
                remfrom(x,clues)
                m=1
            if m==0 and x[0]=='left' and a[0]=='right' and x[1][1]==a[2][1] and a[1][1]==x[2][1]:
                if random.randint(0,1)==0:
                    remfrom(x,clues)
                    m=1
                else:
                    remfrom(x,clues)
                    m=1
            if m==0 and x[0]=='link' and a[0]=='unlink' and (x[2][0]==a[2][0] and x[1][1]==a[1][1]) or (x[2][0]==a[1][0] and x[1][1]==a[2][1]):
                remfrom(x,clues)
                m=1

options=[]
for x in traits_fin:
    option=[]
    ref=x[1]
    for a in items:
        option.append(ref[a.loci])
    options.append(option)

def remfrom(it,lis):
    for x in lis:
        if x==it:
            lis.remove(it)

def gen_pos():
    global possibilities
    possibilities=[]
    indivposs=[]
    for a in options[0]:
        fa=a
        for b in options[1]:
            fb=b
            if len(options)>2:
                for c in options[2]:
                    fc=c
                    if len(options)>3:
                        for d in options[3]:
                            fd=d
                            if len(options)>4:
                                for e in options[4]:
                                    fe=e
                                    if len(options)>5:
                                        for f in options[5]:
                                            ff=f
                                            indivposs.append([fa,fb,fc,fd,fe,ff])
                                    else:
                                        indivposs.append([fa,fb,fc,fd,fe])
                            else:
                                indivposs.append([fa,fb,fc,fd])
                    else:
                        indivposs.append([fa,fb,fc])
            else:
                indivposs.append([fa,fb])
    for a in indivposs:
        it1=[0]
        for x in a:
            it1.append(x)
        for b in indivposs:
            it2=[1]
            for x in b:
                it2.append(x)
            if len(items)>2:
                for c in indivposs:
                    it3=[2]
                    for x in c:
                        it3.append(x)
                    if len(items)>3:
                        for d in indivposs:
                            it4=[3]
                            for x in d:
                                it4.append(x)
                            if len(items)>4:
                                for e in indivposs:
                                    it5=[4]
                                    for x in e:
                                        it5.append(x)
                                    possibilities.append([it1, it2,it3,it4,it5])
                            else:
                                possibilities.append([it1, it2,it3,it4])
                    else:
                        possibilities.append([it1, it2,it3])
            else:
                possibilities.append([it1, it2])
    for a in range(len(traits_fin)):    
        for combo in possibilities:
            for indiv in combo:
                for i in combo:
                    for x in range(1,(len(indiv))):
                        if i[x]==indiv[x] and indiv[0]!=i[0]:
                            remfrom(combo, possibilities)
    return(possibilities)
                            
def ready(opt, clue):
    workingposs=opt
    for a in clue:
        if a[0]=='side':
            for x in workingposs:
                accept=0
                for y in range(len(x)-1):
                    for c in x[y]:
                        for d in x[y+1]:
                            if (c==a[1][1] and d==a[2][1]) or (d==a[1][1] and c==a[2][1]) and c!=d:
                                accept=1
                if accept==0:
                    remfrom(x,workingposs)
        elif a[0]=='right':
            for x in workingposs:
                accept=0
                for y in range(len(x)-1):
                    for c in x[y]:
                        for d in x[y+1]:
                            if (d==a[1][1] and c==a[2][1]) and c!=d:
                                accept=1
                if accept==0:
                    remfrom(x,workingposs)
        elif a[0]=='left':
            for x in workingposs:
                accept=0
                for y in range(len(x)-1):
                    for c in x[y]:
                        for d in x[y+1]:
                            if (c==a[1][1] and d==a[2][1]) and c!=d:
                                accept=1
                if accept==0:
                    remfrom(x,workingposs)
        elif a[0]=='link':
            for x in workingposs:
                accept=0
                for y in x:
                    for n in y:
                        for n1 in y:
                            if (n==a[1][1] and n1==a[2][1]):
                                accept=1
                if accept==0:
                    remfrom(x,workingposs)
        elif a[0]=='unlink':
            for x in workingposs:
                accept=1
                for y in x:
                    for n in y:
                        for n1 in y:
                            if (n==a[1][1] and n1==a[2][1]):
                                accept=0
                if accept==0:
                    remfrom(x,workingposs)
    return(len(workingposs))

for x in range(10):
    generate_clue(random.choice(items).loci, random.choice(traits_fin), random.randint(1,3))
    
sort_clues(clues)
sort_clues(clues)
for a in clues:
    print(a[4])

r=0
while (ready(gen_pos(),clues)) !=1:
    r+=1
    generate_clue(random.choice(items).loci, random.choice(traits_fin), random.randint(1,3))
    sort_clues(clues)
    print(ready(gen_pos(),clues))
    if r==12:
        break

for a in clues:
    print(a[4])