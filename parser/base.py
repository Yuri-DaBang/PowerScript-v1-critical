
from typing import Optional, List

from lexer.base import TokenState
from parser.nodes import ModuleNode


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


    

class Parser:
    """A brain that analyzes the grammar of a language.

    Attributes:
        _tokens_state: A list of TokenState objects.
        _current_token: It is clear from the name.
        _next_token: Read the previous attribute description.
    """

    def __init__(self) -> None:
        self._tokens_state = []  # type: ignore[var-annotated]
        self._current_token = None
        self._next_token = None

    def at_end(self) -> bool:
        """Looks at the remaining tokens to check the end."""
        return (
            not self._tokens_state
            and self._current_token is None
            and self._next_token is None
        )

    def advance(self) -> Optional[TokenState]:
        """Advances to the next token in the tokens state."""
        return self._tokens_state.pop(0) if self._tokens_state else None

    def expect(self, *args: str) -> None:
        """Raises if the expectation is not met."""
        if (args_ := '/'.join(args)) and self._current_token is None:
            print(f"{Colors.bright_red}   Error{Colors.red}",f'Expected `{args_}`, but nothing here!{Colors.reset}')
        elif self._current_token.name not in args:  # type: ignore[attr-defined]
            print(f"{Colors.bright_red}   Error{Colors.red}",
                f'Expected `{args_}`, got `{self._current_token.name}`! '  # type: ignore[attr-defined]
                f'{Colors.red}Line {self._current_token.row}, column {self._current_token.column}{Colors.reset}'
            )
        return None

    def check(self, *args: str) -> Optional[bool]:
        """Checks whether the current token matches the target or not."""
        return (
            self._current_token.name in args  # type: ignore[attr-defined]
            if self._current_token is not None
            else None
        )

    def peek(self, *args: str) -> Optional[bool]:
        """Looks at the next token to match."""
        return (
            self._next_token.name in args  # type: ignore[attr-defined]
            if self._next_token is not None
            else None
        )

    def step(self) -> None:
        """Moves the next and current token values forward."""
        if (
            self._tokens_state
            and self._current_token is None
            and self._next_token is None
        ):
            self._next_token = self.advance()  # type: ignore[assignment]
        self._current_token = self._next_token
        self._next_token = self.advance()  # type: ignore[assignment]

    def parse(self, tokens_state: List[TokenState]) -> ModuleNode:
        """Returns a AST that shows the structure of the code."""
        raise NotImplementedError
