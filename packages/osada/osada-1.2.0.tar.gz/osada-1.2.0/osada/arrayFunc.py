import random


# １次元数直列の生成
def array(inf, sup, number:int=2):
    if(number < 2): return [inf]
    number = abs(int(number-1))
    diff = (sup-inf)/number
    return [inf+(diff*i) for i in range(number+1)]


# １次元乱数直線の生成
def randomArray(inf, sup, number:int=1, isint:bool=False):
    if isint:
        return [random.randint(inf, sup) for _ in range(number)]
    else:
        return [random.random()*(sup-inf) + inf for _ in range(number)]
