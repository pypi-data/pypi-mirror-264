def per(x,y,z=100): #Percentage Function
    return round((x/y)*z)

def qe(a,b,c): # This Function use the built in cmath library,,, Make sure to import it first
    import cmath
    d=pow(b,2)-4*a*c
    x1=(-b+cmath.sqrt(d))/2*a
    x2=(-b-cmath.sqrt(d))/2*a
    list=[x1,x2]
    return list

def fnn(n): #Natural Numbers Upto N
    i=1
    list=[]
    while i<=n:
        list.append(i)
        i+=1
    return list
def fen(n):#Print Even Numbers Upto N
    i=2
    list=[]
    while i<=n:
        if i%2==0:
            list.append(i)
            i=i+1
        else:
            i=i+1

    return list

def fon(n):#Print Even Numbers Upto N
    i=2
    list=[]
    while i<=n:
        if i%2==0:
            i=i+1
        else:
            list.append(i)
            i=i+1

    return list

def fsn(n):
    i=0
    sum=0
    while i<=n:
        sum=sum+i
        i+=1
    return sum

def fson(n):#Print sum of Odd Numbers Upto N
    i=1
    i2=0
    
    while i<=n:
        if i%2==0:
            i=i+1
        else:
            sum=i+i2
            i=i+1
            i2=sum        
    return sum

def fsen(n):#Print sum of Even Numbers Upto N
    i=1
    i2=0
    sum=0
    while i<=n:
        if i%2!=0:
            i=i+1
        else:
            sum=i+i2
            i=i+1
            i2=sum
            
    return sum

def frnn(n): #Print natural numbers up to n in reverse order.
    list=[]
    i=1
    while n>=i:
        list.append(n)
        n=n-1
    return list

def fib(n):
    fib_series = []
    a, b = 0, 1
    while a <= n:
        fib_series.append(a)
        a, b = b, a + b
    return fib_series

def cev(x):
    if x%2==0:
        return True
    else:
        return False

def cod(x):
    if x%2!=0:
        return True
    else:
        return False

def gtable(N):
    list=[]
    for i in range(1, 11):
        result = N * i
        list.append(result)
    return list

def add(*inp):
    sum=0
    for i in inp:
        sum=sum+i
    return sum

def sub(x,y):
    return x-y 

def mul(*inp):
    mp=1
    for i in inp:
        mp=mp*i
    return mp

def dev(x,y):
    if y==0:
        print("Error: Can't Devided by Zero")
    else:    
        return x/y

def spodev(list):
    odd=[]
    even=[]
    for chk in list:
        if chk%2==0:
            even.append(chk)
        else:
            odd.append(chk)
    return even,odd

