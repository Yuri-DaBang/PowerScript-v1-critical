import time , datetime


def ave(arg):
    w = list(arg)
    x = len(w)
    y = 0
    
    for _ in w:
        y = y + float(str(_))
        
    z = y / x
    return (z)

def main(times):
    start_time = datetime.datetime.now()

    abc = []


    for _ in range(times):
	    abc.append(_)

    #print(ave(abc))

    end_time = datetime.datetime.now()

    print(f"Total time taken: {end_time-start_time}")   
    return (end_time-start_time).seconds

tot = []

for _ in range(100):
     aved = main(999999)
     tot.append(aved)
     
#print(tot)

print(ave(tot))

