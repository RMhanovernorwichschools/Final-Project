import random as rd
import copy

'''Format should really be you input final result and generates clues based on that, so I'm going to do that with
a sample one here, and we can work on people typing their own with it later.'''

class puzzle_base:
    def __init__(self,rs,ans):
        self.keys=[(x,rs[x]) for x in range(len(rs))]+[(len(rs),'position')]
        self.chars=copy.deepcopy(ans)
        for x in range(len(ans)):
            ans[x].append(x)
        self.all_ans=ans
        self.options=[]
        for x in self.keys:
            if x[1]=='position':
                break
            portion=[]
            for y in self.chars:
                portion.append(y[x[0]])
            self.options.append(portion)
    
    def clue(specific, char):
        if specific==0:
            if rd.randint(0,1)==1:
                typ='equal'
                p1=rd.choice
            else:
                typ='distin'
            
        

Names=['Willow', 'Lisbet', 'Cameron', 'Mariette', 'Annie', 'Luna', 'Celia']
Scents=['pine', 'lavender', 'lemon', 'soap', 'fish']
Shoes=['hiking shoes', 'worn sneakers', 'winter boots', 'rainboots', 'trail-runners']
BirthMons=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
Coats=['hoodie', 'sweater', 'raincoat', 'down jacket', 'sports coat', 'denim jacket']
Colors=['navy blue', 'pale blue', 'white', 'grey', 'black', 'beige']

sample=puzzle_base(['name', 'coat', 'color', 'scent', 'hobby'], [['Willow', 'raincoat', 'white', 'pine', 'piano'], 
              ['Cameron', 'hoodie', 'navy blue', 'cinnamon', 'reading'], ['June', 'fleece', 'grey', 'lavender', 'singing'], 
              ['Sam', 'fur coat', 'tan', 'fish', 'sewing']])
              
print(sample.options)