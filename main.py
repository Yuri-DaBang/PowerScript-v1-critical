# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import argparse
import pathlib

import datetime , time , sys

from exceptions import InterpretError
from lexer import FarrRegexLexer
from parser import FarrParser
from interpreter import FarrInterpreter



######################
### COLORS LIBRARY ###
######################

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

def run_file(filepath: str) -> None:

    """Executes the code from a file."""
    return FarrInterpreter().interpret(
        FarrParser().parse(
            FarrRegexLexer().tokenize(pathlib.Path(filepath).read_text())
        )
    )



def run_cmd(code: str) -> None:
    """Executes code provided as a string."""
    return FarrInterpreter().interpret(
        FarrParser().parse(FarrRegexLexer().tokenize(code))
    )


def repl() -> None:
    """Runs the codes in an interactive mode."""
    lexer = FarrRegexLexer()
    parser = FarrParser()
    interpreter = FarrInterpreter()

    while True:
        try:
            interpreter._interpret(
                parser.parse(lexer.tokenize(input('Infiniti3 $> ')))
            )
        except (KeyboardInterrupt, EOFError):
            print('Exiting REPL...')
            break
        except InterpretError as e:
            if isinstance(e.error, SystemExit):
                raise e.error
            print(f'Error: {e.error}')
        except BaseException as e:
            print(f'Error: {e}')
    return None

import os

def main() -> None:
    print(f"> {sys.argv[0]} ... {sys.argv[1]} ... {sys.argv[2]}")
    #os.system("pip install sklearn")
    if sys.argv[1] == 'run':
        start_time = datetime.datetime.now()
        print(f"{Colors.bright_green}@Starting {Colors.green}{start_time}{Colors.reset}\n")
        run_file(sys.argv[2])
        end_time = datetime.datetime.now()
        print(f"\n{Colors.bright_green}@Ending {Colors.green}{end_time}{Colors.reset}")

        time_difference_ns = end_time - start_time
        time_difference_sec = time_difference_ns.total_seconds()   # Convert nanoseconds to seconds
        
        #print(f"{start_time} ... {end_time}")
        print(f"\nTotal time taken: {time_difference_sec}")
        
    elif sys.argv[1] == 'cmd':
        run_cmd(sys.argv[2])
    elif sys.argv[1] == 'shell':
        repl()
    else:
        print("error: not a known command")
    return None


if __name__ == '__main__':
    main()
