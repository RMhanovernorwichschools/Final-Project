import random

Names=['Willow', 'Lisbet', 'Cameron', 'Mariette', 'Annie', 'Luna']
Scents=['pine', 'lavender', 'lemon', 'soap', 'fish']
Shoes=['hiking shoes', 'worn sneakers', 'winter boots', 'rainboots', 'trail-runners']
BirthMons=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
Coats=['hoodie', 'sweater', 'raincoat', 'down jacket', 'sports coat']
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
    
print(traits)

class item():
    def __init__(self, n, title):
        self.loci=x
        self.name=Names[n]
        self.scent=Scents[n]
        self.shoe=Shoes[n]
        self.birthmon=BirthMons[n]
        self.coat=Coats[n]
        self.color=Colors[n]

for x in range(item_num):
    a=item(x,x)
    print([a.loci, a.color, a.shoe])
