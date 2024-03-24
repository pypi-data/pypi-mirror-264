message="Bonjour tout le monde"

def entete(s):
    sep="-"*100
    print(sep)
    n=int(100/2-len(s)//2-3)
    print("|", " "*n, s, " "*n, "|")
    print(sep)

def avg(L):
    return sum(L)/len(L)


def factorielle(n):
    f=1
    for k in range(2,n+1):
        f=f*k
    print("la factorielle est :",f)

def PGCD(m,n=1):
    a=m
    b=n
    while a%n:
        r=a%b
        a=b
        b=r
    return b
