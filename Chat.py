import random

greetings=['Hey.', 'Hi!', 'Hey, how are you?']

message='Hey! My name is January.'
tot='none'

for x in (1,2):
    question=0
    string=list(input(message))
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
            start=space_loci[-1]
            fin=sl
        else:
            start=space_loci[x-1]+1
            fin=space_loci[x]
        for n in range(start, fin):
            word+=(characters[n])
        words.append(word)
        
    print(words)
    
    if tot='none':
        if len(words)==1:
            if words[0]=='hi' or words[0]=='hello' or words[0]=='greetings' or words[0]=='heya' or words[0]=='hiya' words[0]=='howdy':
                message=random.choice(greetings)
            if words[0]=='cool' or words[0]=='awesome' or words[0]=='great' or words[0]=='nice':
                agreement=['Probably.', 'Pretty {0}.'format(words[0]), 'Fairly {0}.'format(words[0]), 'Yeah, pretty {0}.'format(words[0])']
                message=random.choice(agreement)
            