string=list(input("Please enter a string of text (the bigger the better): "))
sl=len(string)

lowercase=list('abcdefghijklmnopqrstuvwxyz')
uppercase=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

characters=[]
words=[]
print_b=''

for x in range(0,sl):
    if string[x]!='.' and string[x]!=',' and string[x]!=':':
        characters.append(string[x])
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
print(wordnum)

wordnum_list=list(range(wordnum))

for x in wordnum_list:
    word=''
    if x==0:
        start=0
        fin=space_loci[0]
    elif x==len(wordnum_list)-1:
        start=space_loci[x]
        fin=sl-1
    else:
        start=space_loci[x]+1
        fin=space_loci[x+1]
    for n in range(start, fin):
        word+=(characters[n])
    words.append(word)
    

fin=sl
for x in reverse_space_loci:
    start=x+1
    for n in range(start,fin):
        print_b=print_b+characters[n]
    fin=x
    print_b=print_b+characters[x]
for n in range(0,fin):
    print_b=print_b+characters[n]
    
print(print_b)