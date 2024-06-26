import json


def loads(sson_string):
    """
    Loads SSON data from a string.

    Args:
        self
        sson_string (str): SSON string to be loaded.

    Returns:
        Parsed SSON data.
    """
    sson_data = {}
    for line in str(sson_string).split('\n'):
        if not line or line.startswith('#'):
            continue
            
        datas = line.split(';')
            
        for dat in datas:  
            if not dat or dat.startswith('#'):
                continue
            
            if len(dat.split(":")) == 2:
                parts = dat.split(":")
                if "[" in dat:
                    pass
                else:
                    key = parts[0]
                    valueof = parts[1]
                    sson_data[str(key)] = str(valueof)
            else:
                parts = dat.split(":")
                if "[" in parts[1]:
                    if "[" in parts[1]:
                        heading = str(parts[0])
                        str_parts = str(parts)
                        valueof =str_parts.split(",")

                    F = str(valueof).replace("{","").replace("}","").replace("[","").replace("]","").replace("'","")

                    #print(f"F: {F}")
                    
                    x = 0

                    #print(f"{key} : {resdata} ")

                    valueof[0] = ""

                    dattoresend = ""                      

                    for _ in valueof:
                        if _ == "":
                            pass
                        else:
                            x += 0.5
                            resval = _.replace("{","").replace("}","").replace("[","").replace("]","").replace("'","").replace("#.#",f" @@num")
                            #print(f"*** >>>",resval)
                            dattoresend += resval
                        #print(x)

                    realdat = dattoresend.split(" ")
                    
                    abc = 0
                    charlovck = False

                    jmbldat = ""

                    for __ in realdat:
                        if charlovck:
                            resval2 = __.replace("@@num",f" {str(int(abc))}:")
                        else:
                            resval2 = __.replace("@@num",f",{str(int(abc))}:")
                        #print(resval2)
                        abc += 0.5
                        jmbldat += resval2
                        charlovck = True
                        
                    
                    anadat = jmbldat.split(" ")
                    
                    pakadat = ""
                    
                    for ___ in anadat:
                        if ___ == "":
                            pass
                        else:
                            fusdat = f"{___};"
                            pakadat += fusdat
                            #print(fusdat)

                    #print(pakadat)
                    valdat = loads(pakadat)
                    #print(heading)
                    sson_data[str(heading)] = valdat

                    
                    
            # else:
            #     print(f"Ignoring invalid line: {line}")
    return sson_data

print(loads("name:hamza;age:16;#fgsgdjafdsj;hamza:hamzahamzahamza;people:[#.#:hamza,#.#:mark,#.#:jarvis];"))