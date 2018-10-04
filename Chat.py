string=input("Please enter a string of text (the bigger the better): ")
sl=len(string)

lowercase=list('abcdefghijklmnopqrstuvwxyz')
uppercase=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

characters=[]
print_b=''

for x in range(0,sl):
    for n in range(len(uppercase)):
        if x==uppercase[n]:
            x=lowercase[n]
    characters.append(string[x])


space_loci=[]
for x in range(0,sl):
    if characters[x]==' ':
        space_loci.append(x)

reverse_space_loci=space_loci[len(space_loci):0:-1]
reverse_space_loci.append(space_loci[0])

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