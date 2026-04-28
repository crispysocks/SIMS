#1，1，2，3，5，8，13，21
def fib(n):
    a,b=1,1
    for i in range(n):
        yield a
        a,b=b,a+b

for num in fib(10):
    print(num,end=' ')
