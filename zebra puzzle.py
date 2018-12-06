import random

Names=['Willow', 'Lisbet', 'Cameron', 'Mariette', 'Annie']
Scents=['pine', 'lavender', 'lemon', 'soap', 'fish']
Shoes=['dinosaur boots', 'worn sneakers', 'winter boots', 'black rainboots', 'no shoes']
BirthMons=['January', 'February', 'March', 'April', 'May']
Coats=['hoodie', 'sweater', 'raincoat', 'down jacket', 'sports coat']
Colors=['navy blue', 'pale blue', 'white', 'grey', 'black']

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

class item():
    def __init__(self, n):
        self.name=Names[n]
        self.scent=Scents[n]
        self.shoe=Shoes[n]
        self.birthmon=BirthMons[n]
        self.coat=Coats[n]
        self.color=Colors[n]

for x in range(item_num):
    a=item(x)
    print(a.name+', wearing the '+a.color+' '+a.coat+', was born in '+a.birthmon)