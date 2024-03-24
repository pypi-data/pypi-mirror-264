# 平方根
def sqrt(x):
    return x**(1/2) if (x>=0) else abs(x)**(1/2)


# 標本平均
def avg(xs):
    return sum(xs) / len(xs)


# 標本分散
def div(xs):
    xs_avg = avg(xs)
    result = 0
    for x in xs:
        result += (x-xs_avg)**2
    
    return result

# 標本標準偏差
def st_div(xs):
    return sqrt(div(xs))

