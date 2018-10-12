import random

greetings=['Hey.', 'Hi!']
howyou=['How are you?', "How's it going?", "Is everything going well?"]
neutrals=['Oh. Okay.', 'Huh.', 'Okay.', 'Hm.']
agrees=['Yeah.', "That's what I'd thought.", 'Uh huh.', 'Yeah... good.']

adverbs=['pretty', 'fairly', 'very', 'extremely', 'sorta', 'kinda', 'mostly', 'rather', 'really']
positive=['good', 'great', 'awesome', 'cool', 'amazing', 'superb']
negative=['bad', 'terrible', 'awful', 'lame', 'horrible', 'poorly', 'badly']
emotions=['happy', 'sad', 'bored', 'excited', 'tired', 'mad', 'angry', 'cheerful']

message='Hey! My name is January.'
tot='none'
userstate='unknown'
assign=0
newtopic='false'

def yn_check(response):
    for arp in response:
        if arp=='yes' or arp=='yeah' or arp=='yup' or arp=='yep' or arp=='ya' or arp=='uh-huh' or arp=='of' or arp=='quite':
            return 1
        elif arp=='no' or arp=='nah' or arp=='nope'or arp=='not':
            return -1
        else:
            return 0

def topic_check(response):
    topic='none'
    ttw=''
    mood='neutral'
    tone='neutral'
    mtw=''
    for arp in response:
        if arp=='school' or arp=='schoolwork' or arp=='homework':
            topic='school'
            ttw=arp
        elif arp=='dog' or arp=='dogs' or arp=='puppy':
            topic='dog'
            ttw=arp
        elif arp=='sunny' or arp=='cloudy' or arp=='windy' or arp=='wind' or arp=='winds' or arp=='rain' or arp=='rainy' or arp=='cloud' or arp=='clouds' or arp=='weather' or arp=='fog' or arp=='foggy' or arp=='mist' or arp=='misty':
            topic='weather'
            ttw=arp
    for arp in response:
        if question==1 and arp=='you':
            mood='ques_jan'
            tone='ques'
            mtw=''
        elif arp=='awful' or arp=='stress' or arp=='stressful' or arp=='terrible' or arp=='miserable':
            mood='unhappy'
            tone='neg'
            mtw=arp
        elif arp=='sad' or arp=='cry' or arp=='lonely':
            mood='sad'
            tone='neg'
            mtw=arp
        elif arp=='tired' or arp=='exhausted' or arp=='sleepy' or arp=='fatigued':
            mood='tired'
            tone='neg'
            mtw=arp
        elif arp=='excited' or arp=='anticipate' or arp=='forward' or arp=='anticipating' or arp=='eager':
            mood='excited'
            tone='pos'
            mtw=arp
    return (topic, ttw, mood, tone, mtw)

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
        if string[x]!='.' and string[x]!=',' and string[x]!=':'and string[x]!="'" and string[x]!='"' and string[x]!='?' and string[x]!='!' and string[x]!='/':
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
    
    for x in words:
        if x=='huh' or x=='um' or x=='january' or x=='m' or x=='hm' or x=='jan' or x=='uh':
            words.remove(x)
        
    print(words)
    message1=message
    
    if len(words)==1 and words[0]=='ugh':
        message="Wait, what's wrong?"
    elif len(words)>1 and words[0]=='you':
        for x in words:
            for n in positive:
                if x==n:
                    message='Thank you.'
    elif len(words)==1 and words[0]=='what':
        messages=['Did I say something weird?', 'Was that strange of me to say?', 'Sorry, did I just say something off?']
        message=random.choice(messages)
        tot='self_failure'
    elif len(words)>1 and (words[0]=='its' or words[0]=='thats'):
        if words[1]=='okay' or words[1]=='fine' or words[1]=='cool':
            message='Yeah. Okay.'
            tot='none'
        else:
            for x in positive:
                if words[1]==x:
                    message=random.choice(agrees)
                else:
                    message='Hm... {0}?'.format(words[1])
    elif tot=='none' and len(words)==1 and (words[0]=='okay' or words[0]=='fine' or words[0]=='sure' or words[0]=='right'):
        messages=['Yeah. Okay.', 'M-hm.', 'Right.', '...yeah.']
        message=random.choice(messages)
        tot='none'
    elif words[0]=='wait' or words[0]=='stop':
        message="Sorry. I'm stopped."
        tot='none'
    elif tot=='confirmation':
        if yn_check(words)==1:
            message=random.choice(agrees)
        elif yn_check(words)==0:
            message=random.choice(neutrals)
        else:
            message='Oh.'
    elif len(words)==1 and yn_check(words)==1:
        messages=['Right.', '...', 'So...', 'Uh huh.']
        message=random.choice(messages)
    elif len(words)==1 and yn_check(words)==-1:
        messages=['No?', 'Uh... hm.', 'So... am I wrong then?', 'Huh. I guess not. Maybe.']
        message=random.choice(messages)
    elif words[0]=='hi' or words[0]=='hello' or words[0]=='greetings' or words[0]=='heya' or words[0]=='hiya' or words[0]=='howdy' or words[0]=='hey':
        message=random.choice(greetings)
        if random.randint(1,2)==1:
            tot="howareyou"
            message+=' '+random.choice(howyou)
    elif tot=='none' and (words[0]=='cool' or words[0]=='awesome' or words[0]=='great' or words[0]=='nice'):
        agreement=['Probably.', 'Pretty {0}.'.format(words[0]), 'Fairly {0}.'.format(words[0]), 'Yeah, pretty {0}.'.format(words[0])]
        message=random.choice(agreement)
    elif words[0]=='how' or words[0]=='hows' and len(words)>2:
        mash=words[1]+words[2]
        if mash=='areyou' or mash=='areya' or mash=='ru' or mash=='areu':
            message="I'm fine, thanks."
        elif mash=='arethings' or mash=='isit' or mash=='arethings' or words[1]=='it' or mash=='goesit':
            message="Good."
        if userstate=='unknown':
            message+=' How about you?'
            tot='howareyou'
    elif (len(words)>1 and words[0]=='im') or (len(words)>2 and words[0]=='i' and (words[1]=='feel' or words[1]=='am')):
        for x in words:
            for n in emotions:
                if x==n:
                    tot='userstate'
                    if topic_check(words)[3]=='neg':
                        messages=['{0}. That really sucks.'.format(n), 'Oh no, why {0}?'.format(n)]
                        message=random.choice(messages)
                    elif topic_check(words)[3]=='pos':
                        messages=['{0}, huh? Well, good.'.format(n), 'Nice to hear.']
                        message=random.choice(messages)
                    else:
                        messages=['{0}, huh?'.format(n), 'Why {0}?'.format(n)]
                        message=random.choice(messages)
    elif tot=='howareyou':
        negate='false'
        for x in words:
            if x=='you':
                andme=1
            else:
                andme=0
            if x=='not':
                negate='true'
        for x in words:
            for n in positive:
                if x==n or yn_check(words)==1:
                    if negate=='false':
                        userstate='good'
                        message="I'm glad."
                        if andme==1:
                            message+=" And I'm doing pretty well, thanks."
                            tot='none'
                        else:
                            newtopic='true'
                            assign=random.randint(1,2)
                    else:
                        userstate='bad'
                        message="Oh no! What's wrong?"
                        tot='userstate'
        for x in words:
            for n in negative:
                if x=='bad' or x=='awful' or x=='terrible' or x=='lame' or x=='boring' or x==n or yn_check(words)==-1:
                    if negate=='false':
                        userstate='bad'
                        message="Oh no! What's wrong?"
                        tot='userstate'
                    else:
                        userstate='neutral'
                        message=""
                        if andme==1:
                            message+="Yeah, I'm about the same."
                            tot='none'
                        else:
                            newtopic='true'
                            assign=random.randint(1,2)
        for x in words:
            if x=='fine' or x=='okay' or x=='alright' or x=='ok' or x=='enough':
                if negate=='false':
                    userstate='neutral'
                    message=""
                    if andme==1:
                        message+="Yeah, I'm about the same."
                        tot='none'
                    else:
                        newtopic='true'
                        assign=random.randint(1,2)
                else:
                    userstate='bad'
                    message="Oh no! What's wrong?"
                    tot='userstate'
        if len(words)==1 and message==message1:
            message='{0}, huh? How come?'.format(words[0])
            tot='userstate'
    elif tot=='chocolate':
        for x in words:
            if x=='favorite' or x=='favourite':
                message='My favorite kind is probably white chocolate.'
            elif x=='vanilla':
                message='I mean... vanilla is good too. Just not as good as chocolate.'
            elif x=='why':
                y=random.randint(1,3)
                if y==1:
                    message="I think I like white best because... I don't know. It's creamy?"
                    tot='confirmation'
                elif y==2:
                    message="White chocolate is just so good! I dunno why."
                elif y==3:
                    message="Uh... Well, haven't you ever had any?"
                    tot='confirmation'
            elif x=='you' and question==1:
                message='I like chocolate. I really like chocolate.'
            elif yn_check(words)==1:
                message='Good. I like chocolate, too.'
            elif yn_check(words)==0:
                message=random.choice(neutrals)
            elif yn_check(words)==-1:
                message='...oh.'
    elif tot=='self_failure':
        if yn_check(words)==1:
            messages=["Oh. I'm so sorry.", "Sorry, I didn't mean to.", "Okay. I'll try to not do it again."]
            message=random.choice(messages)
            tot='none'
        elif yn_check(words)==-1:
            messages=["I'm relieved. I though from your reaction that maybe I had.", "Oh, okay. Good."]
            message=random.choice(messages)
            tot='none'
        else:
            message='Um... Can we maybe change the subject? Uh...'
            newtopic='true'
            assign=random.randint(1,2)
    elif tot=='ghostworld':
        unsure='false'
        for x in range(len(words)-1):
            if words[x]=='dont' and words[x+1]=='know':
                unsure='true'
            elif words[x]=='not' and words[x+1]=='sure':
                unsure='true'
            elif words[x]=='no' and words[x+1]=='idea':
                unsure='true'
        for x in words:
            if words[x]=='dunno' or words[x]=='confused':
                unsure='true'
        if unsure=='true':
            messages=["I guess it's hard to imagine, isn't it?", "I guess I wouldn't really know how I would act either.", "That makes sense. It's a weird scenario."]
            message=random.choice(messages)
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

    if message==message1:
        print(topic_check(words))
        
                
print(message)
