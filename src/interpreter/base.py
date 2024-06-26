
import sys
import re
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional, Any, Dict

from exceptions import (
    BreakError,
    ContinueError,
    ReturnError,
    InterpretError,
)
from parser.nodes import ASTNode, ModuleNode

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

######################
#### BASE LIBRARY ####
######################


@dataclass
class Environment:
    """Manage scopes and their possible parents.

    Attributes:
        symbols: Current environment data independent of the parent.
        parent: An optional parent.
    """

    symbols: Optional[Dict[str, Any]] = field(
        default_factory=dict, kw_only=True
    )
    parent: Optional['Environment'] = field(default=None, kw_only=True)

    def __deepcopy__(self, memo: Dict[int, Any]) -> 'Environment':
        """Returns a deep copy of the environment."""
        if id(self) in memo:
            return memo[id(self)]
        copied_environment = self.__class__(symbols=self.symbols.copy(), parent=self.parent)  # type: ignore[union-attr]
        memo[id(self)] = copied_environment
        if self.parent is not None:
            copied_environment.parent = deepcopy(self.parent, memo)
        return copied_environment

    def assign(self, name: str, value: Any) -> None:
        """Assigns a value to a symbol in the current environment."""
        self.symbols.update({name: value})  # type: ignore[union-attr]

    def replace(self, name: str, value: Any) -> None:
        """Updates the symbol if it exists."""
        if name in self.symbols:  # type: ignore[operator]
            self.symbols.update({name: value})  # type: ignore[union-attr]
            return None
        elif self.parent is not None:
            return self.parent.replace(name, value)
        print(f"{Colors.bright_red}   NameError{Colors.red}",f'Nothing was found with the name `{name}`!{Colors.reset}')

    def locate(self, name: str) -> Any:
        """Tries to find the requested symbol."""
        if (
            value := self.symbols.get(name, None)  # type: ignore[union-attr]
        ) is not None:
            return value
        elif self.parent is not None:
            return self.parent.locate(name)
        print(f"{Colors.bright_red}   NameError{Colors.red}",f'Nothing was found with the name `{name}`!{Colors.reset}')

    def exists(self, name: str, depth: Optional[int] = 0) -> bool:
        """Checks if the symbol exists at the specified depth or not."""
        environment = self
        while depth > 0 and environment.parent is not None:  # type: ignore[operator]
            environment = environment.parent
            depth -= 1  # type: ignore[operator]
        return depth == 0 and name in environment.symbols  # type: ignore[operator]

    def copy(self) -> 'Environment':
        """Helps to copy the environment more easily."""
        return deepcopy(self)

class Interpreter:
    """To walk on abstract syntax trees and execute their nodes.

    Attributes:
        builtin_symbols: A dictionary that includes the natives of the language.
        environment: An instance of `Environment`.
    """

    builtin_symbols: Dict[str, Any]

    def __init__(self, *, environment: Optional[Environment] = None) -> None:
        self.environment = (
            environment
            if environment is not None
            else Environment(symbols=self.builtin_symbols.copy())
        )

    def __deepcopy__(self, memo: Dict[int, Any]) -> 'Interpreter':
        """Returns a deep copy of the interpreter."""
        if id(self) in memo:
            return memo[id(self)]
        copied_interpreter = self.__class__(environment=self.environment)
        memo[id(self)] = copied_interpreter
        copied_interpreter.environment = deepcopy(self.environment, memo)
        return copied_interpreter

    def _interpret(self, node: ASTNode) -> Any:
        """Interprets the given AST node."""
        handler_name = '_interpret_{}'.format(
            '_'.join(
                map(
                    str.lower,
                    filter(
                        lambda x: x,
                        re.split(
                            r'([A-Z][a-z]*)',
                            node.__class__.__name__,
                        ),
                    ),
                )
            )
        )
        if (interpreter_method := getattr(self, handler_name, None)) is None:
            print(f"{Colors.bright_red}   AttributeError{Colors.red}",
                f'Implement the `{handler_name}` method in the '
                f'`{self.__class__.__name__}` class...{Colors.reset}'
            )
        try:
            return interpreter_method(node)
        except (BreakError, ContinueError, ReturnError):
            raise
        except InterpretError as e:
            raise InterpretError(
                error=e.error, origin=e.origin  # To avoid nesting errors
            )
        except BaseException as e:
            raise InterpretError(error=e, origin=str(node))

    def interpret(self, node: ModuleNode) -> None:
        """Tries to start the interpretation with caution."""
        try:
            self._interpret(node)
        except InterpretError as e:
            error_details = (
                str(e.error).rstrip('!.') or 'No additional error details'
            )
            (first_row, first_column), *_ = re.findall(
                r'row=(\d+), column=(\d+)', e.origin
            )
            print(
                f'{e.error.__class__.__name__}: {error_details}! '
                f'Around line {first_row}, column {first_column}. {Colors.reset}'
            )
            sys.exit(1)

    def copy(self) -> 'Interpreter':
        """Helps to copy the interpreter more easily."""
        return deepcopy(self)
