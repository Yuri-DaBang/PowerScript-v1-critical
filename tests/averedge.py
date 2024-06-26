import math

def ave(arg):
    w = list(arg)
    x = len(w)
    y = 0
        
    for _ in w:
        y = y + _
            
    z = y / x
    return z


print(ave([1,2,2,2,2,2,3]));
            