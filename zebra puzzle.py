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
    clue=[]
    f3=''
    if sep==0:
        p1='The girl in the {0} position'.format(x)
        f1=['loci', x]
    elif sep==1 or sep==2:
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
    elif sep==2:
        b=random.randint(0,2)
        if x==items[-1].loci and b==1:
            b=random.randint(0,1)*2
        elif x==items[0].loci and b==2:
            b=random.randint(0,1)
        if b==0:
            p2=' is next to'
            if random.randint(0,1)==0 or x!=items[0].loci:
                partner=x-1
            else:
                partner=x+1
            variety='side'
        elif b==1:
            p2=' is to the left of'
            partner=x+1
            variety='left'
        else:
            p2=' is to the right of'
            partner=x-1
            variety='right'
        a=random.choice(traits_fin)
        if a[0]=='name':
            p3=a[1][partner]
        elif a[0]=='month':
            p3='the girl born in {0}'.format(a[1][partner])
        elif a[0]=='shoe' or a[0]=='color':
            p3=' the girl wearing {0}'.format(a[1][partner])
        elif a[0]=='scent':
            p3='the girl who smells of {0}'.format(a[1][partner])
        elif a[0]=='coat':
            p3='the girl wearing the {0}'.format(a[1][partner])
        f2=[a[0], a[1][partner]]
        p2=p2+' '+p3
    clue=[variety, f1, f2, f3,p1+p2]
    print(clue)
    clues.append(clue)
        
options=[]
for x in traits_fin:
    option=[]
    ref=x[1]
    for a in items:
        option.append(ref[a.loci])
    options.append(option)
    
print(options)
    
generate_clue(items[0].loci, random.choice(traits_fin), 2)
generate_clue(random.choice(items).loci, traits_fin[-1], 1)
generate_clue(items[-1].loci, random.choice(traits_fin), 1)
