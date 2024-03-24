from .colorPrint import *



## =====================================================================
## 


def func_floor(func):
    
    def wrapper(*args, **kwargs):

        reward = func(*args, **kwargs)
        if isinstance(reward, tuple):
            reward = [Mahjong.floor(r / 100) * 100 for r in reward]
        else:
            reward = Mahjong.floor(reward / 100) * 100

        return reward
    
    return wrapper


class Mahjong:


    FLOOR = [8000, 12000, 12000, 16000, 16000, 16000, 24000, 24000, 32000]


    @staticmethod
    def floor(x):
        
        diff = x % 1
        x = int(x) + (diff != 0)

        return x


    @func_floor
    def calc_reward(fu, han, oya=False, tsumo=False):
        
        if fu <= 10: return 0
        if han == 1 and fu <= 20: return 0
        if han == 2 and fu <= 10: return 0
        
        if not tsumo and fu == 20: return 0
        
        if han == 4 and fu >= 40: han = 5
        
        if han > 4:
            
            if han > 13: han = 13
                
            reward = Mahjong.FLOOR[han-5]
            
            if tsumo:
                if oya:
                    return reward//2
                else:
                    return reward//4, reward//2
            else:
                if oya:
                    return reward*1.5
                else:
                    return reward
        
        
        if tsumo:
            
            if oya:
                reward = fu * (2 ** (han + 2)) * 2
                return reward
            else:
                reward = fu * (2 ** (han + 2))
                return reward, reward*2

        else:
            
            if oya:
                reward = fu * (2 ** (han + 4)) * 1.5
                return reward
            else:
                reward = fu * (2 ** (han + 4))
                return reward



    ## =====================================================================
    ## 

    @staticmethod
    def quiz():

        import random
        import time
        
        print(f'''
        {"="*30}
        点数計算 
        {"="*30}
        ''')
        
        
        while True:

            try:
                
                han = random.randint(1, 6)
                fu = random.randint(2, 5) * 10
                
                if han == 6:
                    han = random.randint(6, 11)
                
                tsumo = random.choice([True, False])
                oya = random.choice([True, False, False, False])

                if not tsumo and fu == 20: continue

                reward = Mahjong.calc_reward(fu, han, oya, tsumo)

                if not reward: continue
                
                cprint(f'{("子親")[oya]} {["ロン", "ツモ"][tsumo]}')
                time.sleep(0.5)
                cprint(f'{fu}符 {han}飜 ')
                time.sleep(0.5)
                inp = input(f'> ')


                if inp == 'q': break
                
                inp = inp.split(' ')
                cprint(inp)
                
                is_correct = False
                
                try:   
                    if len(inp) == 1:
                        inp = int(inp[0])
                        is_correct = inp == reward
                        
                    elif len(inp) == 2:
                        inp = tuple(map(int, inp))
                        is_correct = sum(map(lambda x: x[0] == x[1], zip(inp, reward))) == 2
                        
                    else:
                        pass
                except:
                    pass
                
                
                cprint(f'{["NG", "OK"][is_correct]}', ['red', 'green'][is_correct])
                
                time.sleep(1)
                    
                if not is_correct:
                    cprint(f'正解: {reward}')
                    time.sleep(1)    

                cprint(f'\n{"="*30}\n')


            except KeyboardInterrupt:
                break
            
