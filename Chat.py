import random

greetings=['Hey.', 'Hi!']
howyou=['How are you?', "How's it going", "Is everything going well?"]
neutrals=['Oh. Okay.', 'Huh.', 'Okay.', 'Hm.']
agrees=['Yeah.', "That's what I'd thought.", 'Uh huh.', 'Yeah... good.']

adverbs=['pretty', 'fairly', 'very', 'extremely', 'sorta', 'kinda', 'mostly', 'rather', 'really']
psotive=['good', 'great', 'awesome', 'cool', 'amazing', 'superb']

message='Hey! My name is January.'
tot='none'
userstate='unknown'
assign=0
newtopic='false'

def yn_check(response):
    for arp in response:
        if arp=='yes' or arp=='yeah' or arp=='yup' or arp=='yep' or arp=='ya' or arp=='uh-huh' or arp=='of':
            return 1
        elif arp=='no' or arp=='nah' or arp=='nope'or arp=='not':
            return -1
        else:
            return 0

for x in range(6):
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
    
    if len(words)==1 and words[0]=='ugh':
        message="Wait, what's wrong?"
    if len(words)>1 and words[0]=='its':
        if words[1]=='okay' or words[1]=='fine' or words[1]=='cool':
            Message='Yeah. Okay.'
            tot='none'
            newtopic='true'
            assign=random.randint(1,2)
        else:
            for x in positive:
                if words[1]==x:
                    message=random.choice(agrees)
                else:
                    message='Hm... {0}?'.format(words[1])
    elif tot=='confirmation':
        if yn_check(words)==1:
            message=random.choice(agrees)
        elif yn_check(words)==0:
            message=random.choice(neutrals)
        else:
            message='Oh.'
    elif tot=='none':
        if words[0]=='hi' or words[0]=='hello' or words[0]=='greetings' or words[0]=='heya' or words[0]=='hiya' or words[0]=='howdy' or words[0]=='hey':
            message=random.choice(greetings)
            if random.randint(1,2)==1:
                tot="howareyou"
                message+=' '+random.choice(howyou)
        if words[0]=='cool' or words[0]=='awesome' or words[0]=='great' or words[0]=='nice':
            agreement=['Probably.', 'Pretty {0}.'.format(words[0]), 'Fairly {0}.'.format(words[0]), 'Yeah, pretty {0}.'.format(words[0])]
            message=random.choice(agreement)
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
        global rep
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
        if rep=='good' or rep=='great' or rep=='yeah' or rep=='yes' or rep=='yup' or rep=='yep' or yn_check(words)==1:
            userstate='good'
            message="I'm glad."
            newtopic='true'
            assign=random.randint(1,2)
        elif rep=='fine' or rep=='okay' or rep=='alright' or rep=='ok' or rep=='enough':
            userstate='neutral'
            message=""
            newtopic='true'
            assign=random.randint(1,2)
        elif rep=='bad' or rep=='awful' or rep=='terrible' or rep=='lame' or rep=='boring' or yn_check(words)==-1:
            userstate='bad'
            message="Oh no! What's wrong?"
            tot='userstate'
        else:
            for x in words:
                if x=='well' or x=='cool' or x=='good' or x=='great':
                    message='Nice.'
                    tot='none'
                if x=='bad' or x=='not':
                    message="Oh... that's too bad. How come?"
                    tot='userstate'
                else:
                    message=random.choice(neutrals)
                    tot='none'
    elif tot=='chocolate':
        for x in words:
            if x=='favorite' or x=='favourite':
                message='My favorite kind is probably white chocolate.'
            if x=='vanilla':
                message='I mean... vanilla is good too. Just not as good as chocolate.'
            if x=='why':
                y=random.randint(1,3)
                if y==1:
                    message="I think I like white best because... I don't know. It's creamy?"
                    tot='confirmation'
                elif y==2:
                    message="White chocolate is just so good! I dunno why."
                elif y==3:
                    message="Uh... Well, haven't you ever had any?"
                    tot='confirmation'
            elif yn_check(words)==1:
                message='Good. I like chocolate, too.'
            elif yn_check(words)==0:
                message=random.choice(neutrals)
                tot='none'
            elif yn_check(words)==-1:
                message='...oh.'
                tot='none'
    else:
        message="Sorry... I'm confused."
        tot='none'
    if newtopic=='true':
        if assign==1:
            message=message+' Um... do you like chocolate?'
            tot='chocolate'
        elif assign==2:
            message=message+' Can I ask a random question? If everyone on earth disappeared except for you, what would you do?'
            tot='ghostworld'
        newtopic='false'
        
                
print(message)
            