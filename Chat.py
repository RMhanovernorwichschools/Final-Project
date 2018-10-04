import random

greetings=['Hey.', 'Hi!']
howyou=['How are you?', "How's it going", "Is everything going well?"]
neutrals=['Oh. Okay.', 'Huh.', 'Okay.', 'Hm.']

adverbs=['pretty', 'fairly', 'very', 'extremely', 'sorta', 'kinda', 'mostly', 'rather', 'really']

message='Hey! My name is January.'
tot='none'
userstate='unknown'
assign=0
newtopic='false'

def yn_check(response):
    for arp in response:
        if arp=='yes' or arp=='yeah' or arp=='yup' or arp=='yep' or arp=='ya' or or arp=='uh-huh' or arp=='of':
            return 1
        elif arp=='no' or arp=='nah' or arp=='nope'or arp=='not':
            return -1
        else:
            return 0

for x in (1,2):
    question=0
    string=list(input(message+'''
'''))
    sl=len(string)
    
    lowercase=list('abcdefghijklmnopqrstuvwxyz')
    uppercase=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    characters=[]
    words=[]
    print_b=''
    
    for x in range(0,sl):
        if string[x]!='.' and string[x]!=',' and string[x]!=':'and string[x]!="'" and string[x]!='"' and string[x]!='?':
            characters.append(string[x])
        elif string[x]=='?':
            sl-=1
            question=1
        else:
            sl-=1
    for x in range(0,sl):
        for n in range(len(uppercase)):
            if characters[x]==uppercase[n]:
                characters[x]=lowercase[n]
    
    space_loci=[]
    for x in range(0,sl):
        if characters[x]==' ':
            space_loci.append(x)
            
    wordnum=len(space_loci)+1
    wordnum_list=list(range(wordnum))
    
    for x in wordnum_list:
        word=''
        if x==0:
            start=0
            if wordnum==1:
                fin=len(characters)
            else:
                fin=space_loci[0]
        elif x==len(wordnum_list)-1:
            start=space_loci[-1]+1
            fin=sl
        else:
            start=space_loci[x-1]+1
            fin=space_loci[x]
        for n in range(start, fin):
            word+=(characters[n])
        words.append(word)
        
    print(words)
    
    if len(words)==1 and word[0]=='ugh':
        message="Wait, what's wrong?"
    elif tot=='none':
        if len(words)==1:
            if words[0]=='hi' or words[0]=='hello' or words[0]=='greetings' or words[0]=='heya' or words[0]=='hiya' or words[0]=='howdy' or words[0]=='hey':
                message=random.choice(greetings)
                if random.randint(1,2)==1:
                    userstate="howareyou"
                    message+=' '+random.choice(howyou)
            if words[0]=='cool' or words[0]=='awesome' or words[0]=='great' or words[0]=='nice':
                agreement=['Probably.', 'Pretty {0}.'.format(words[0]), 'Fairly {0}.'.format(words[0]), 'Yeah, pretty {0}.'.format(words[0])]
                message=random.choice(agreement)
        elif len(words)==3:
            if words[0]=='how' or words[0]=='hows':
                mash=words[1]+words[2]
                if mash=='areyou' or mash=='areya' or mash=='ru' or mash=='areu':
                    message="I'm fine, thanks."
                elif mash=='arethings' or mash=='isit' or mash=='arethings' or words[1]=='it' or mash=='goesit':
                    message="Good."
                if userstate=='unknown':
                    message+=' How about you?'
                    tot='howareyou'
    elif tot=='howareyou':
        if len(words)==1:
            rep=words[0]
        elif len(words)==2:
            for x in adverbs:
                if words[0]=='im' or words[0]==adverbs:
                    rep=words[1]
        elif len(words)==3:
            for x in adverbs:
                if words[0]=='im' and words[1]==x:
                    rep=words[2]
        if rep=='good' or rep=='great' or rep=='yeah' or rep=='yes' or rep=='yup' or rep=='yep':
            userstate='good'
            message="I'm glad."
            newtopic='true'
            assign=random.randint(1,2)
    elif tot=='chocolate':
        if yn_check(words)==1:
            message='Good. I like chocolate, too.'
        elif yn_check(words)==0:
            message=random.choice(neutrals)
        else:
            message='...oh.'
    else:
        message=="Sorry... I'm confused."
    if newtopic=='true':
        if assign==1:
            message=message+' Um... do you like chocolate?'
            tot='chocolate'
        elif assign==2:
            message=message+' Can I ask a random question? If everyone on earth disappeared except for you, what would you do?'
            tot='ghostworld'
        newtopic='false'
        
                
print(message)
            