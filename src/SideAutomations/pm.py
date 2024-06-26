import os, json, sys
from turtle import color


class Colors:
    # ANSI escape codes for colors
    reset = "\033[0m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    white = "\033[37m"
    bright_black = "\033[90m"
    bright_red = "\033[91m"
    bright_green = "\033[92m"
    bright_yellow = "\033[93m"
    bright_blue = "\033[94m"
    bright_magenta = "\033[95m"
    bright_cyan = "\033[96m"
    bright_white = "\033[97m"
    
class PacketManager:
     # Example commands in JSON format
    
    def __init__(self,file_loc,cmd):
        with open(file_loc,"r") as cf:
            data = json.load(cf)

        version_lang = data["config"]["Infiniti2"]

        version_main = data["config"]["Infiniti/"]["main"]
        version_env = data["config"]["Infiniti/"]["env"]
        version_base = data["config"]["Infiniti/"]["base"]
        
        version_ranges_main = data["config"]["@Infiniti/main"]
        version_ranges_env = data["config"]["@Infiniti/env"]
        version_ranges_base = data["config"]["@Infiniti/base"]
        
        versions_to_validate = [version_ranges_main,version_ranges_env,version_ranges_base]
        versions_already_have = [version_main,version_env,version_base]

        ### CHECK FOR VERSIONS ###
            
        raw_cu = versions_already_have
        raw_gt = versions_to_validate

        

        #print(f"{raw_cu} && {raw_cu[1]}")

        ### PROCESS SOME COMMANDS ###

        key = cmd.split(" ")

        try:
            if key[0] == "infiniti":
                if key[1] == "-vr":
                    if key[2] == "-a":
                        h1 = "package"
                        x = 1
                        print(f"{Colors.bright_black}╭─────┬─────────┬─────────────┬───────────┬──────────╮")
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}###{Colors.reset} {Colors.bright_black}│{Colors.reset} {Colors.bright_magenta}{h1:<7}{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}Status{Colors.reset}      {Colors.bright_black}│ {Colors.bright_magenta}Supported{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}Required{Colors.reset} {Colors.bright_black}│")
                        print(f"{Colors.bright_black}├─────┼─────────┼─────────────┼───────────┼──────────┤")
                        for i in range(len(raw_gt)):
                            V = raw_cu[i].replace("v","")
                            G = raw_gt[i].replace("^","")

                            ve = int(V)
                            vg = int(G)

                            ido = ""

                            #print(f"{V} && {G}")
                            if i == 0 : ido = f"{Colors.bright_magenta}main   {Colors.reset}"
                            if i == 1 : ido = f"{Colors.bright_magenta}env    {Colors.reset}"
                            if i == 2 : ido = f"{Colors.bright_magenta}base   {Colors.reset}"




                            if ve - vg < 0:
                                print(f"{Colors.bright_black}│ {Colors.bright_magenta}{x:<3}{Colors.reset} {Colors.bright_black}│ {ido:<7} {Colors.bright_black}│ {Colors.bright_magenta}unsupported {Colors.bright_black}│ {Colors.bright_magenta}v{ve:<8} {Colors.bright_black}│ {Colors.bright_magenta}v{vg:<7} {Colors.bright_black}│")
                            else:
                                print(f"{Colors.bright_black}│ {Colors.bright_magenta}{x:<3}{Colors.reset} {Colors.bright_black}│ {ido:<7} {Colors.bright_black}│ {Colors.bright_magenta}supported   {Colors.bright_black}│ {Colors.bright_magenta}v{ve:<8} {Colors.bright_black}│ {Colors.bright_magenta}v{vg:<7} {Colors.bright_black}│")
                            x = x +1
                        print(f"{Colors.bright_black}╰─────┴─────────┴─────────────┴───────────┴──────────╯")
                    if key[2] == "-A":
                        h1 = "package"
                        x = 1
                        print(f"{Colors.bright_black}╭─{Colors.bright_magenta}ANALYTICS{Colors.bright_black}───────────────────────────────────────────────────────────────╮")
                        __in = []
                        __out = []
                        for i in range(len(raw_gt)):
                            V = raw_cu[i].replace("v","")
                            G = raw_gt[i].replace("^","")

                            ve = int(V)
                            vg = int(G)

                            ido = ""


                            if ve - vg < 0:
                                __out.append("anathor one")
                            else:
                                __in.append("anathor one")

                            ### ANALYTICS ###

                            
                            x = x +1

                        _profit = len(__in)
                        _loss = len(__out)
                        _all    = _profit + _loss
                                
                        _p_age_profit = _profit / _all * 100
                        _p_age_loss   = _loss / _all * 100
                            
                        ### STATEMENT ###
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}({_profit}/{_all}) files are upto date, which is around {_p_age_profit}% of the whole dir {Colors.bright_black}     │")
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}({_loss}/{_all}) files need an update, around {_p_age_loss}% of the files are out of support {Colors.bright_black}│")

                        print(f"{Colors.bright_black}╰─────────────────────────────────────────────────────────────────────────╯")
                elif key[1] == "-ss":        
                    if key[2] == "-a":
    
                        # Extract the script names from the infiniti data
                        script_names = list(data['scripts'].keys())

                        # Write out the names of every script in the specified format

                        h1 = "Scripts"
                        h2 = "Types"

                        print(f"{Colors.bright_black}╭─────┬─────────────────────────────────────────────────────────┬────────╮")
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}###{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h1:<55}{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h2}{Colors.reset}  {Colors.bright_black}│")
                        print(f"{Colors.bright_black}├─────┼─────────────────────────────────────────────────────────┼────────┤")

                        for idx, script_name in enumerate(script_names, start=1):
                            ext = ""
        
                            if   script_name.endswith(".skiy"): ext = f"{Colors.bright_red}SKIY  {Colors.reset}"
                            elif script_name.endswith(".infy"): ext = f"{Colors.bright_magenta}INFY  {Colors.reset}"
                            elif script_name.endswith(".infy2"): ext = f"{Colors.bright_magenta}INFY2 {Colors.reset}"
                            elif script_name.endswith(".pack"): ext = f"{Colors.bright_yellow}PACKET{Colors.reset}"
                            else: ext = f"{Colors.bright_magenta}@@@@  {Colors.reset}"

                            print(f"{Colors.bright_black}│ {Colors.bright_magenta}{idx:<4}{Colors.reset}{Colors.bright_black}│ {Colors.bright_magenta}{script_name:<55} {Colors.bright_black}│ {ext:<13} {Colors.bright_black}│")

                        print(f"{Colors.bright_black}╰─────┴─────────────────────────────────────────────────────────┴────────╯")
                    elif key[2] == "-A":
    
                        # Extract the script names from the infiniti data
                        script_names = list(data['scripts'].keys())

                        # Write out the names of every script in the specified format

                        h1 = "Scripts"
                        h2 = "Types"

                        print(f"{Colors.bright_black}╭─{Colors.bright_magenta}ANALYTICS{Colors.bright_black}──────────────────────────────────────────────────────────────────╮")
                        
                        _skiy = []
                        _infy = []
                        _infy2 = []
                        _pack = []
                        _unknoun = []    
                        
                        for idx, script_name in enumerate(script_names, start=1):
                            ext = ""

        
                            if   script_name.endswith(".skiy"): _skiy.append("anathor one")
                            elif script_name.endswith(".infy"): _infy.append("anathor one")
                            elif script_name.endswith(".infy2"): _infy2.append("anathor one")
                            elif script_name.endswith(".pack"): _pack.append("anathor one")
                            else: _unknoun.append("anathor one")
                            
                        len_skiy = len(_skiy)
                        len_infy = len(_infy)
                        len_infy2 = len(_infy2)
                        len_pack = len(_pack)
                        len_unknoun = len(_unknoun)
                        _all    = len_pack + len_infy + len_infy2 + len_skiy + len_unknoun
                         

                        ### STATEMENT ###

                        for _ in range(1,6):
                            if _ == 1:
                                _name = "PySkilya"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_skiy}/{_all}) {_name} files found with extension (.skiy), {len_skiy/_all*100:.2f}% all togather.{Colors.bright_black}  │")
                            elif _ == 2:
                                _name = "Infiniti"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_infy}/{_all}) {_name} files found with extension (.infy), {len_infy/_all*100:.2f}% all togather.{Colors.bright_black}    │")
                            elif _ == 3:
                                _name = "Infiniti2"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_infy2}/{_all}) {_name} files found with extension (.infy2), {len_infy2/_all*100:.2f}% all togather.{Colors.bright_black} │")
                            elif _ == 4:
                                _name = "Packet"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_pack}/{_all}) {_name} files found with extension (.pack), {len_pack/_all*100:.2f}% all togather.{Colors.bright_black}    │")
                            elif _ == 5:
                                _name = "Unknoun"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_unknoun}/{_all}) {_name} files found, {len_unknoun/_all*100:.2f}% all togather.{Colors.bright_black}                           │")
                        
                        print(f"{Colors.bright_black}╰────────────────────────────────────────────────────────────────────────────╯")
                elif key[1] == "-cf":
                    if key[2] == "-a":
        
                        # Extract the script names from the infiniti data
                        script_names = list(data['codefiles'].keys())

                        # Write out the names of every script in the specified format

                        h1 = "CodeDependency"
                        h2 = "Types"

                        print(f"{Colors.bright_black}╭─────┬─────────────────────────────────────────────────────────┬─────────╮")
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}###{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h1:<55}{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h2}{Colors.reset}   {Colors.bright_black}│")
                        print(f"{Colors.bright_black}├─────┼─────────────────────────────────────────────────────────┼─────────┤")

                        for idx, script_name in enumerate(script_names, start=1):
                            ext = ""
            
                            if   script_name.endswith(""): ext = f"{Colors.bright_magenta}Python {Colors.reset}"
                            else: ext = f"{Colors.bright_magenta}@@@@   {Colors.reset}"

                            print(f"{Colors.bright_black}│ {Colors.bright_magenta}{idx:<4}{Colors.reset}{Colors.bright_black}│ {Colors.bright_magenta}{script_name:<55} {Colors.bright_black}│ {ext:<13} {Colors.bright_black}│")

                        print(f"{Colors.bright_black}╰─────┴─────────────────────────────────────────────────────────┴─────────╯")
                elif key[1] == "-dir":
                    if key[2] == "-a":
        
                        # Extract the script names from the infiniti data
                        script_names = list(data['dirmap'].keys())

                        # Write out the names of every script in the specified format

                        h1 = "File"
                        h2 = "Types"

                        print(f"{Colors.bright_black}╭─────┬─────────────────────────────────────────────────────────────────────────────────┬───────────────╮")
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}###{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h1:<79}{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h2}{Colors.reset}         {Colors.bright_black}│")
                        print(f"{Colors.bright_black}├─────┼─────────────────────────────────────────────────────────────────────────────────┼───────────────┤")
        
                        for idx, script_name in enumerate(script_names, start=1):
                            ext = ""
            
                            if "abc" == "abc":
                               f_w_h = script_name.split(".")
                               if len(f_w_h) > 2 or ".git" in script_name:
                                    f_w_h = ".*.."
                               elif "zJunk" in script_name:
                                    f_w_h = "Junk"
                            else:
                                f_w_h = script_name.split(".")
                            
                            if len(f_w_h) > 1:
                                ext = f_w_h[1]
                            else:
                                ext = "@@@@"

                            print(f"{Colors.bright_black}│ {Colors.bright_magenta}{idx:<4}{Colors.reset}{Colors.bright_black}│ {Colors.bright_magenta}{script_name:<79} {Colors.bright_black}│ {Colors.bright_magenta}{ext:<13}{Colors.reset} {Colors.bright_black}│")

                        print(f"{Colors.bright_black}╰─────┴─────────────────────────────────────────────────────────────────────────────────┴───────────────╯")
                    elif key[2] == "-A":
    
                        # Extract the script names from the infiniti data
                        script_names = list(data['dirmap'].keys())

                        # Write out the names of every script in the specified format

                        print(f"{Colors.bright_black}╭─{Colors.bright_magenta}ANALYTICS{Colors.bright_black}──────────────────────────────────────────────────────────────────╮")
                        
                        _skiy = []
                        _infy = []
                        _infy2 = []
                        _pack = []

                        _python = []
                        _md = []

                        _unknoun = []    
                        
                        for idx, script_name in enumerate(script_names, start=1):
                            ext = ""

        
                            if   script_name.endswith(".skiy"): _skiy.append("anathor one")
                            elif script_name.endswith(".infy"): _infy.append("anathor one")
                            elif script_name.endswith(".infy2"): _infy2.append("anathor one")
                            elif script_name.endswith(".pack"): _pack.append("anathor one")
                            elif script_name.endswith(".py"): _python.append("anathor one") #new
                            elif script_name.endswith(".md"): _md.append("anathor one") #new
                            elif script_name.endswith(".MD"): _md.append("anathor one") #new
                            else: _unknoun.append("anathor one")
                            
                        len_skiy = len(_skiy)
                        len_infy = len(_infy)
                        len_infy2 = len(_infy2)
                        len_pack = len(_pack)

                        len_python = len(_python)
                        len_md = len(_md)

                        len_unknoun = len(_unknoun)
                        _all    = len_pack + len_infy + len_infy2 + len_skiy + len_unknoun + len_md + len_python
                         

                        ### STATEMENT ###

                        for _ in range(1,11):
                            if _ == 1:
                                _name = "PySkilya"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_skiy}/{_all}) {_name} files found with extension (.skiy), {len_skiy/_all*100:.2f}% all togather.{Colors.bright_black} │")
                            elif _ == 2:
                                _name = "Infiniti"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_infy}/{_all}) {_name} files found with extension (.infy), {len_infy/_all*100:.2f}% all togather.{Colors.bright_black}   │")
                            elif _ == 3:
                                _name = "Infiniti2"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_infy2}/{_all}) {_name} files found with extension (.infy2), {len_infy2/_all*100:.2f}% all togather.{Colors.bright_black} │")
                            elif _ == 4:
                                _name = "Packet"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_pack}/{_all}) {_name} files found with extension (.pack), {len_pack/_all*100:.2f}% all togather.{Colors.bright_black}   │")
                            elif _ == 5:
                                _name = "Python"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_python}/{_all}) {_name} files found with extension (.py), {len_python/_all*100:.2f}% all togather.{Colors.bright_black}     │")
                            elif _ == 6:
                                _name = "md"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_md}/{_all}) {_name} files found with extension (.md|.MD), {len_md/_all*100:.2f}% all togather.{Colors.bright_black}       │")
                            elif _ == 7:
                                _name = "Unknoun"
                                print(f"{Colors.bright_black}│{Colors.bright_magenta} ({len_unknoun}/{_all}) {_name} files found, {len_unknoun/_all*100:.2f}% all togather.{Colors.bright_black}                         │")
                            
                        print(f"{Colors.bright_black}╰────────────────────────────────────────────────────────────────────────────╯")        
                    if key[1] == "-a":
                        # Extract the infiniti data
                        config_data = data['config']

                        # Write out the names and versions of every script in the specified format
                        h1 = "Version"
                        h2 = "Package"

                        print(f"{Colors.bright_black}╭─────┬────────────────────────────────┬────────────╮")
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}###{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h2:<30}{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h1:<10}{Colors.reset} {Colors.bright_black}│")
                        print(f"{Colors.bright_black}├─────┼────────────────────────────────┼────────────┤")

                        idx = 1
                        for script_name, version in config_data.items():
                            if isinstance(version, dict):  # Handle nested dictionaries
                                for sub_name, sub_version in version.items():
                                    full_name = f"{script_name}{sub_name}"
                                    print(f"{Colors.bright_black}│ {Colors.bright_magenta}{idx:<4}{Colors.reset}{Colors.bright_black}│ {Colors.bright_magenta}{full_name:<30} {Colors.bright_black}│ {Colors.bright_magenta}{sub_version:<10} {Colors.bright_black}│")
                                    idx += 1
                            else:
                                print(f"{Colors.bright_black}│ {Colors.bright_magenta}{idx:<4}{Colors.reset}{Colors.bright_black}│ {Colors.bright_magenta}{script_name:<30} {Colors.bright_black}│ {Colors.bright_magenta}{version:<10} {Colors.bright_black}│")
                                idx += 1

                        print(f"{Colors.bright_black}╰─────┴────────────────────────────────┴────────────╯")
                    if key[2] == "-A":
                        h1 = "package"
                        x = 1
                        print(f"{Colors.bright_black}╭─{Colors.bright_magenta}ANALYTICS{Colors.bright_black}───────────────────────────────────────────────────────────────╮")
                        __in = []
                        __out = []
                        for i in range(len(raw_gt)):
                            V = raw_cu[i].replace("v","")
                            G = raw_gt[i].replace("^","")

                            ve = int(V)
                            vg = int(G)

                            ido = ""


                            if ve - vg < 0:
                                __out.append("anathor one")
                            else:
                                __in.append("anathor one")

                            ### ANALYTICS ###

                            
                            x = x +1

                        _profit = len(__in)
                        _loss = len(__out)
                        _all    = _profit + _loss
                                
                        _p_age_profit = _profit / _all * 100
                        _p_age_loss   = _loss / _all * 100
                            
                        ### STATEMENT ###
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}({_profit}/{_all}) files are upto date, which is around {_p_age_profit}% of the whole dir {Colors.bright_black}     │")
                        print(f"{Colors.bright_black}│ {Colors.bright_magenta}({_loss}/{_all}) files need an update, around {_p_age_loss}% of the files are out of support {Colors.bright_black}│")

                        print(f"{Colors.bright_black}╰─────────────────────────────────────────────────────────────────────────╯")
            if key[0] == "help":
                commands = [
                        {
                            "name": "1.1",
                            "usage": "infiniti -vr -a",
                            "description": "To check all the versions and their supportablity. (table)"
                        },
                        {
                            "name": "1.2",
                            "usage": "infiniti -vr -A",
                            "description": "To check all the versions and their supportablity. (analitics)"
                        },
                        {
                            "name": "2.1",
                            "usage": "infiniti -ss -a",
                            "description": "To list all the registered scripts. (table) (in config.json)"
                        },
                        {
                            "name": "2.2",
                            "usage": "infiniti -ss -A",
                            "description": "To list all the registered scripts. (analitics) (in config.json)"
                        },
                        {
                            "name": "3.1",
                            "usage": "infiniti -dir -a",
                            "description": "To list all contents of the main /SRC dir. (table)"
                        },
                        {
                            "name": "3.2",
                            "usage": "infiniti -dir -A",
                            "description": "To list all contents of the main /SRC dir. (analitics)"
                        },
                        {
                            "name": "4.1",
                            "usage": "infiniti -cf -a",
                            "description": "To list all code files which runs the whole Infiniti Project."
                        },
                        {
                            "name": "4.1",
                            "usage": "help",
                            "description": "To list all the help content (this table)."
                        },
                    ]
                h1 = "Command Decscription"
                h2 = "Usage"
                print(f"{Colors.bright_black}╭─────┬───────────────────────────────────────────────────────────────────┬──────────────────────────╮")
                print(f"{Colors.bright_black}│ {Colors.bright_magenta}###{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h1:<65}{Colors.reset} {Colors.bright_black}│ {Colors.bright_magenta}{h2:<24}{Colors.reset}{Colors.bright_black} │")
                print(f"{Colors.bright_black}├─────┼───────────────────────────────────────────────────────────────────┼──────────────────────────┤")
                for idx, command, in enumerate(commands, 1):
                    print(f"{Colors.bright_black}│ {Colors.bright_magenta}{idx:<4}{Colors.reset}{Colors.bright_black}│ {Colors.bright_magenta}{command['description']:<65} {Colors.bright_black}│ {command['usage']:<24} {Colors.bright_black}│")
                print(f"{Colors.bright_black}╰─────┴───────────────────────────────────────────────────────────────────┴──────────────────────────╯")
            if key[0] == "ipm":
               
        except Exception as exceptionssss:
            print(f"error -> {exceptionssss}")
            
#obj = PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json","infiniti -vr -a")
#obj = PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json","infiniti -vr -A")

#obj = PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json","infiniti -ss -a")
#obj = PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json","infiniti -ss -A")

#obj = PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json","infiniti -cf -a")

#obj = PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json","infiniti -dir -a")
#obj = PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json","infiniti -dir -A")

import sys

import sys

def main():
    try:
        # Assuming sys.argv[0] is the script name, so starting from sys.argv[1]
        # Joining all arguments from sys.argv[1:] with space
        args = ' '.join(sys.argv[1:])
        PacketManager("E:/enchant/sbin/Infiniti-Lang/all/mip/Infiniti2/sbin/config.json", args)
    except Exception as eee:
        print(eee)

if __name__ == "__main__":
    main()
    print(f"{Colors.reset}")

