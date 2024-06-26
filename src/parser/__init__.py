
from functools import partial
from typing import Optional, Union, Callable, List, Tuple

from helpers import partition_a_sequence, normalize_identifier
from lexer.base import TokenState
from parser.base import Parser
from parser.nodes import (
    VoidFunctionDefinitionNode,
    VoidMemberFunctionDefinitionNode,
    ModuleNode,
    BlockNode,
    ExpressionNode,
    PassNode,
    NullNode,
    HeterogeneousLiteralNode,
    BinaryNode,
    OctalNode,
    HexadecimalNode,
    IntegerNode,
    FloatNode,
    StringNode,
    IdentifierNode,
    RangeNode,
    ItemizedExpressionNode,
    ChainedExpressionsNode,
    ListNode,
    HashMapNode,
    PairNode,
    ExpandableArgumentNode,
    CallNode,
    GroupedExpressionNode,
    NegationOperationNode,
    PreIncrementNode,
    PreDecrementNode,
    PostIncrementNode,
    PostDecrementNode,
    ArithmeticOperationNode,
    RelationalOperationNode,
    LogicalOperationNode,
    TernaryOperationNode,
    StatementNode,
    UseNode,
    VariableDeclarationNode,
    VariadicParameterDeclarationNode,
    AssignmentNode,
    LeftShiftAssignmentNode,
    RightShiftAssignmentNode,
    AddAssignmentNode,
    SubtractAssignmentNode,
    MultiplyAssignmentNode,
    DivideAssignmentNode,
    ModulusAssignmentNode,
    PowerAssignmentNode,
    WhileNode,
    ForNode,
    ForeachNode,
    BreakNode,
    ContinueNode,
    IfNode,
    CondNode,
    MatchNode,
    CaseNode,
    TryNode,
    CatchNode,
    FunctionDefinitionNode,
    MemberFunctionDefinitionNode,
    StructDefinitionNode,
    ExtensionDefinitionNode,
    ReturnNode,
)

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

########################
### __INIT__ LIBRARY ###
########################


class FarrParser(Parser):
    def _except_current_and_next_at(
        self,
        index: int,
        tokens: Tuple[str, ...],
    ) -> Optional[bool]:
        """Checks the token at the given index without advancing the position."""
        return (
            self._tokens_state[index].name in tokens
            if len(self._tokens_state) >= index
            else None
        )

    def _validate(
        self,
        fn: Callable[[], Optional[ExpressionNode]],
        expects: Tuple[str, ...],
    ) -> Optional[ExpressionNode]:
        """Validates function output and checks for expected tokens."""
        if (node := fn()) is None:
            self.expect(*expects)
        return node

    def _followed_by(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
        expects: Tuple[str, ...],
    ) -> Optional[Union[ExpressionNode, StatementNode]]:
        """Calls function and expects following tokens."""
        node = fn()
        self.expect(*expects)
        self.step()
        return node

    def _followed_by_semicolon(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> Optional[Union[ExpressionNode, StatementNode]]:
        """Calls function and expects following semicolon."""
        return self._followed_by(fn, ('Semicolon',))

    def _grouped(
        self,
        opened: str,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
        closed: str,
    ) -> Optional[Union[ExpressionNode, StatementNode]]:
        """Groups expression between opening and closing tokens."""
        self.expect(opened)
        self.step()
        result = fn()
        self.expect(closed)
        self.step()
        return result

    def _bracketed(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> Optional[Union[ExpressionNode, StatementNode]]:
        """Groups expression in brackets."""
        return self._grouped('LeftBracket', fn, 'RightBracket')

    def _braced(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> Optional[Union[ExpressionNode, StatementNode]]:
        """Groups expressions in braces."""
        return self._grouped('LeftBrace', fn, 'RightBrace')

    def _parenthesized(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> Optional[Union[ExpressionNode, StatementNode]]:
        """Groups expression in parentheses."""
        return self._grouped('LeftParenthesis', fn, 'RightParenthesis')

    def _separated_items(
        self,
        fn: Callable[
            [],
            Optional[
                Union[ExpressionNode, VariableDeclarationNode, AssignmentNode]
            ],
        ],
        separators: Tuple[str, ...],
    ) -> ItemizedExpressionNode:
        """Collects separated items."""
        items = []
        while (node := fn()) is not None:
            if isinstance(node, ItemizedExpressionNode):
                items.extend(node.items)
            else:
                items.append(node)
            if not self.check(*separators):
                break
            self.step()
        return ItemizedExpressionNode(items=items)

    def _comma_separated_items(
        self,
        fn: Callable[
            [],
            Optional[
                Union[ExpressionNode, VariableDeclarationNode, AssignmentNode]
            ],
        ],
    ) -> ItemizedExpressionNode:
        """Collects items separated by comma."""
        return self._separated_items(fn, ('Comma',))

    def _dot_separated_items(
        self,
        fn: Callable[
            [],
            Optional[
                Union[ExpressionNode, VariableDeclarationNode, AssignmentNode]
            ],
        ],
    ) -> ItemizedExpressionNode:
        """Collects items separated by dot."""
        return self._separated_items(fn, ('Dot',))

    def _accumulate_until(
        self,
        retreat: Callable[[], Optional[bool]],
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> List[Union[ExpressionNode, StatementNode]]:
        """Accumulates nodes until condition is met."""
        body = []
        while not retreat() and (node := fn()) is not None:
            body.append(node)
        return body

    def _parse_pass(self) -> PassNode:
        """Parses a pass token."""
        self.expect('Pass')
        pass_ = PassNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
        )
        self.step()
        return pass_

    def _parse_null(self) -> NullNode:
        """Parses a null."""
        self.expect('Null')
        null = NullNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
        )
        self.step()
        return null

    def _parse_binary(self) -> BinaryNode:
        """Parses a binary value."""
        self.expect('Binary')
        binary = BinaryNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
            value=self._current_token.value,  # type: ignore[attr-defined]
        )
        self.step()
        return binary

    def _parse_octal(self) -> OctalNode:
        """Parses an octal value."""
        self.expect('Octal')
        octal = OctalNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
            value=self._current_token.value,  # type: ignore[attr-defined]
        )
        self.step()
        return octal

    def _parse_hexadecimal(self) -> HexadecimalNode:
        """Parses a hexadecimal value."""
        self.expect('Hexadecimal')
        hexadecimal = HexadecimalNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
            value=self._current_token.value,  # type: ignore[attr-defined]
        )
        self.step()
        return hexadecimal

    def _parse_integer(self) -> IntegerNode:
        """Parses an integer token."""
        self.expect('Integer')
        integer = IntegerNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
            value=self._current_token.value,  # type: ignore[attr-defined]
        )
        self.step()
        return integer

    def _parse_float(self) -> FloatNode:
        """Parses a float token."""
        self.expect('Float')
        float_ = FloatNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
            value=self._current_token.value,  # type: ignore[attr-defined]
        )
        self.step()
        return float_

    def _parse_string(self) -> StringNode:
        """Parses a string token."""
        self.expect('String')
        string = StringNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
            value=self._current_token.value,  # type: ignore[attr-defined]
        )
        self.step()
        return string

    def _parse_identifier(self) -> IdentifierNode:
        """Parses an identifier token."""
        self.expect('Identifier', 'Symbol')
        identifier = IdentifierNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
            value=normalize_identifier(
                self._current_token.value  # type: ignore[attr-defined]
            ),
        )
        self.step()
        return identifier

    def _process_factor(self) -> Optional[ExpressionNode]:
        """Processes a factor expression."""
        if self.check('Pass'):
            return self._parse_pass()
        elif self.check('Null'):
            return self._parse_null()
        elif self.check('Binary'):
            return self._parse_binary()
        elif self.check('Octal'):
            return self._parse_octal()
        elif self.check('Hexadecimal'):
            return self._parse_hexadecimal()
        elif self.check('Integer'):
            return self._parse_integer()
        elif self.check('Float'):
            return self._parse_float()
        elif self.check('String'):
            return self._parse_string()
        elif self.check('Identifier', 'Symbol'):
            return self._parse_identifier()
        return None

    def _parse_negation_operation(self) -> NegationOperationNode:
        """Parses a negation operation."""
        self.expect('Not')
        operator = self._current_token
        self.step()
        return NegationOperationNode(
            row=operator.row,  # type: ignore[attr-defined]
            column=operator.column,  # type: ignore[attr-defined]
            operator=None,
            operand=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_pre_increment(self) -> PreIncrementNode:
        """Parses a pre-increment operation."""
        self.expect('Increment')
        operator = self._current_token
        self.step()
        return PreIncrementNode(
            row=operator.row,  # type: ignore[attr-defined]
            column=operator.column,  # type: ignore[attr-defined]
            operator=None,
            operand=(
                expression.expressions
                if isinstance(
                    expression := self._process_expression(),
                    ChainedExpressionsNode,
                )
                else ItemizedExpressionNode(items=[expression])
            ),
        )

    def _parse_pre_decrement(self) -> PreDecrementNode:
        """Parses a pre-decrement operation."""
        self.expect('Decrement')
        operator = self._current_token
        self.step()
        return PreDecrementNode(
            row=operator.row,  # type: ignore[attr-defined]
            column=operator.column,  # type: ignore[attr-defined]
            operator=None,
            operand=(
                expression.expressions
                if isinstance(
                    expression := self._process_expression(),
                    ChainedExpressionsNode,
                )
                else ItemizedExpressionNode(items=[expression])
            ),
        )

    def _parse_list(self) -> ListNode:
        """Parses a list node."""
        return ListNode(
            elements=self._braced(  # type: ignore[arg-type]
                partial(
                    self._comma_separated_items,
                    fn=self._process_expression,
                )
            )
        )

    def _parse_pair(self) -> PairNode:
        """Parses a pair expression."""
        self.expect('Colon')
        self.step()
        return PairNode(
            key=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
            value=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _resolve_empty_hash_map(self) -> None:
        """Resolves an empty hash map."""
        self.expect('LeftBrace')
        self.step()
        self.expect('Colon')
        self.step()
        self.expect('RightBrace')
        self.step()
        return None

    def _parse_hash_map(self) -> HashMapNode:
        """Parses a hash map node."""
        return HashMapNode(
            pairs=(
                self._braced(  # type: ignore[arg-type]
                    partial(
                        self._comma_separated_items,
                        fn=self._parse_pair,
                    )
                )
                if not self._except_current_and_next_at(0, ('RightBrace',))
                else self._resolve_empty_hash_map()  # type: ignore[func-returns-value]
            )
        )

    def _parse_range(self) -> RangeNode:
        """Parses a range expression."""
        from_ = self._validate(self._process_expression, ('Expression',))
        if (by := None) or self.check('Comma'):
            self.step()
            by = self._validate(self._process_expression, ('Expression',))
        if (to := None) or self.check('Between'):
            self.step()
            to = self._validate(self._process_expression, ('Expression',))
        return RangeNode(from_=from_, to=to, by=by)  # type: ignore[arg-type]

    def _parse_arithmetic_operation(self) -> ArithmeticOperationNode:
        """Parses an arithmetic operation."""
        self.expect(
            'LeftShift',
            'RightShift',
            'Add',
            'Subtract',
            'Multiply',
            'Divide',
            'Modulus',
            'Power',
        )
        operator = self._current_token
        self.step()
        return ArithmeticOperationNode(
            row=operator.row,  # type: ignore[attr-defined]
            column=operator.column,  # type: ignore[attr-defined]
            operator=operator.name,  # type: ignore[attr-defined]
            left=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
            right=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_keyword_assignment(self) -> AssignmentNode:
        """Assigns to an optional parameter when calling."""
        references = self._dot_separated_items(self._parse_identifier)
        self.expect('Equal')
        self.step()
        return AssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_expandable_argument(self) -> ExpandableArgumentNode:
        """Parses an expandable argument for calls."""
        self.expect('Pass')
        self.step()
        return ExpandableArgumentNode(
            expression=self._validate(self._process_expression, ('Expression',))  # type: ignore[arg-type]
        )

    def _resolve_call_argument(
        self,
    ) -> Optional[Union[ExpressionNode, AssignmentNode]]:
        """Resolves a call argument expression."""
        return (
            self._parse_keyword_assignment()
            if self.check('Identifier', 'Symbol') and self.peek('Equal')
            else (
                self._parse_expandable_argument()
                if self.check('Pass')
                and not self.peek('Comma', 'RightParenthesis')
                else self._process_expression()
            )
        )

    def _parse_call(self, invoke: IdentifierNode) -> CallNode:
        """Parses a function call expression."""
        return CallNode(
            invoke=invoke,
            args=self._parenthesized(  # type: ignore[arg-type]
                partial(
                    self._comma_separated_items,
                    fn=self._resolve_call_argument,
                )
            ),
        )

    def _resolve_chain_target(self) -> Optional[ExpressionNode]:
        """Resolves chain target expression."""
        return (
            (
                term.expressions
                if isinstance(term, ChainedExpressionsNode)
                else term
            )
            if isinstance(
                term := self._process_term(),
                (
                    IdentifierNode,
                    RangeNode,
                    ChainedExpressionsNode,
                    CallNode,
                ),
            )
            else None
        )

    def _parse_chained_expressions(
        self,
        base: ExpressionNode,
    ) -> ChainedExpressionsNode:
        """Parses chained expressions."""
        return ChainedExpressionsNode(
            expressions=ItemizedExpressionNode(
                items=[
                    base,
                    *self._dot_separated_items(
                        partial(
                            self._validate,
                            fn=self._resolve_chain_target,
                            expects=('Term',),
                        )
                    ).items,
                ]
            )
        )

    def _process_chaining(
        self,
        base: ExpressionNode,
    ) -> Union[ExpressionNode, ChainedExpressionsNode]:
        """Processes chained expressions if dot is detected."""
        if self.check('Dot'):
            self.step()
            return self._parse_chained_expressions(base)
        return base

    def _process_term(self) -> Optional[ExpressionNode]:
        """Processes a term expression."""
        if self.check('Increment'):
            return self._parse_pre_increment()
        elif self.check('Decrement'):
            return self._parse_pre_decrement()
        elif (factor := self._process_factor()) is None:
            if self.check('Not'):
                return self._parse_negation_operation()
            elif self.check('LeftBrace') and (
                self.peek('RightBrace')
                or self._except_current_and_next_at(0, ('Comma',))
            ):
                return self._process_chaining(self._parse_list())
            elif self.check('LeftBrace') and self.peek('Colon'):
                return self._process_chaining(self._parse_hash_map())
            elif self.check('LeftParenthesis'):
                return self._process_chaining(
                    GroupedExpressionNode(
                        expression=self._parenthesized(  # type: ignore[arg-type]
                            self._process_expression
                        )
                    )
                )
            elif self.check('LeftBracket'):
                return self._bracketed(self._parse_range)  # type: ignore[return-value]
            elif self.check(
                'LeftShift',
                'RightShift',
                'Add',
                'Subtract',
                'Multiply',
                'Divide',
                'Modulus',
                'Power',
            ):
                return self._parse_arithmetic_operation()
        elif isinstance(factor, HeterogeneousLiteralNode):
            if isinstance(factor, IdentifierNode) and self.check(
                'LeftParenthesis'
            ):
                return self._process_chaining(self._parse_call(factor))
            return self._process_chaining(factor)
        return factor

    def _process_expression(self) -> Optional[ExpressionNode]:
        """Processes an expression."""
        if (left := self._process_term()) is None:
            return None

        if self.check(
            'EqualEqual',
            'NotEqual',
            'GreaterThan',
            'LessThan',
            'GreaterThanOrEqual',
            'LessThanOrEqual',
            ):
            operator = self._current_token
            self.step()
            left = RelationalOperationNode(
                row=operator.row,  # type: ignore[attr-defined]
                column=operator.column,  # type: ignore[attr-defined]
                operator=operator.name,  # type: ignore[attr-defined]
                left=left,
                right=self._validate(  # type: ignore[arg-type]
                    self._process_expression,
                    ('Expression',),
                ),
            )
        if self.check(
            'Sametype',      ### NEW ###
            'NotSametype',   ### NEW ###
            'SametypeandValue', ### NEW ###
            'NotSametypeandValue', ### NEW ###
            'LessThanOrEqual', ### NEW ###
            ):
            operator = self._current_token
            self.step()
            left = RelationalOperationNode(
                row=operator.row,  # type: ignore[attr-defined]
                column=operator.column,  # type: ignore[attr-defined]
                operator=operator.name,  # type: ignore[attr-defined]
                left=left,
                right=self._validate(  # type: ignore[arg-type]
                    self._process_expression,
                    ('Expression',),
                ),
            )
        if self.check(
            'StringColonEqual', ### NEW ###
            'IntColonEqual', ### NEW ###
            'FloatColonEqual',### NEW ###
            'BoolColonEqual', ### NEW ###
            ):
            operator = self._current_token
            self.step()
            left = RelationalOperationNode(
                row=operator.row,  # type: ignore[attr-defined]
                column=operator.column,  # type: ignore[attr-defined]
                operator=operator.name,  # type: ignore[attr-defined]
                left=left,
                right=self._validate(  # type: ignore[arg-type]
                    self._process_expression,
                    ('Expression',),g
                ),
            )
        if self.check('And', 'Or'):
            operator = self._current_token
            self.step()
            left = LogicalOperationNode(
                row=operator.row,  # type: ignore[attr-defined]
                column=operator.column,  # type: ignore[attr-defined]
                operator=operator.name,  # type: ignore[attr-defined]
                left=left,
                right=self._validate(  # type: ignore[arg-type]
                    self._process_expression,
                    ('Expression',),
                ),
            )

        if self.check('Increment'):
            operator = self._current_token
            self.step()
            left = PostIncrementNode(
                row=operator.row,  # type: ignore[attr-defined]
                column=operator.column,  # type: ignore[attr-defined]
                operator=None,
                operand=(
                    left.expressions
                    if isinstance(left, ChainedExpressionsNode)
                    else ItemizedExpressionNode(items=[left])
                ),
            )
        elif self.check('Decrement'):
            operator = self._current_token
            self.step()
            left = PostDecrementNode(
                row=operator.row,  # type: ignore[attr-defined]
                column=operator.column,  # type: ignore[attr-defined]
                operator=None,
                operand=(
                    left.expressions
                    if isinstance(left, ChainedExpressionsNode)
                    else ItemizedExpressionNode(items=[left])
                ),
            )

        if self.check('If'):
            if_ = self._current_token
            self.step()
            condition = self._validate(
                self._process_expression,
                ('Expression',),
            )
            self.expect('Else')
            self.step()
            left = TernaryOperationNode(
                row=if_.row,  # type: ignore[attr-defined]
                column=if_.column,  # type: ignore[attr-defined]
                then=left,
                condition=condition,  # type: ignore[arg-type]
                orelse=self._validate(  # type: ignore[arg-type]
                    self._process_expression,
                    ('Expression',),
                ),
            )

        if self.check('Cond'):
            if_ = self._current_token
            self.step()
            condition = self._validate(
                self._process_expression,
                ('Expression',),
            )
            self.expect('Default')
            self.step()
            left = TernaryOperationNode(
                row=if_.row,  # type: ignore[attr-defined]
                column=if_.column,  # type: ignore[attr-defined]
                then=left,
                condition=condition,  # type: ignore[arg-type]
                orelse=self._validate(  # type: ignore[arg-type]
                    self._process_expression,
                    ('Expression',),
                ),
            )
        return left

    def _parse_use(self) -> UseNode:
        """Parses an use statement."""
        self.expect('Use')
        self.step()
        return UseNode(
            path=self._separated_items(
                self._parse_identifier,
                ('Divide',),
            )
        )

    def _parse_variable_declaration(self) -> VariableDeclarationNode:
        """Parses a variable declaration statement."""
        self.expect('Variable')
        self.step()
        identifier = self._parse_identifier()
        expression = None
        
        # Check for string type
        if self.check('ColonEqual'):
            self.step()
            expression = self._validate(
                self._process_expression, ('Expression',)
            )
            return VariableDeclarationNode(identifier=identifier, expression=expression)
        elif self.check('Equal'):
            self.step()
            expression = self._validate(
                self._process_expression, ('Expression',)
            )
            return VariableDeclarationNode(identifier=identifier, expression=str(expression))
        

        return VariableDeclarationNode(identifier=identifier, expression=expression)

    def _parse_variadic_parameter_declaration(
        self,
    ) -> VariadicParameterDeclarationNode:
        """Parses a declaration of a variadic parameter."""
        self.expect('Variable')
        self.step()
        identifier = self._parse_identifier()
        self.expect('Pass')
        self.step()
        if (expression := None) or self.check('Equal'):
            self.step()
            expression = self._validate(
                self._process_expression, ('Expression',)
            )
        return VariadicParameterDeclarationNode(
            identifier=identifier, expression=expression
        )  # type: ignore[arg-type]

    def _parse_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> AssignmentNode:
        """Parses an assignment statement."""
        self.expect('Equal')
        self.step()
        return AssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_left_shift_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> LeftShiftAssignmentNode:
        """Parses a left shift assignment."""
        self.expect('LeftShiftEqual')
        self.step()
        return LeftShiftAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_right_shift_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> RightShiftAssignmentNode:
        """Parses a right shift assignment."""
        self.expect('RightShiftEqual')
        self.step()
        return RightShiftAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_add_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> AddAssignmentNode:
        """Parses an addition assignment."""
        self.expect('AddEqual')
        self.step()
        return AddAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_subtract_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> SubtractAssignmentNode:
        """Parses a subtraction assignment."""
        self.expect('SubtractEqual')
        self.step()
        return SubtractAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_multiply_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> MultiplyAssignmentNode:
        """Parses a multiplication assignment."""
        self.expect('MultiplyEqual')
        self.step()
        return MultiplyAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_divide_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> DivideAssignmentNode:
        """Parses a division assignment."""
        self.expect('DivideEqual')
        self.step()
        return DivideAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_modulus_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> ModulusAssignmentNode:
        """Parses a modulus assignment."""
        self.expect('ModulusEqual')
        self.step()
        return ModulusAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_power_assignment(
        self,
        references: ItemizedExpressionNode,
    ) -> PowerAssignmentNode:
        """Parses a power assignment."""
        self.expect('PowerEqual')
        self.step()
        return PowerAssignmentNode(
            references=references,
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
        )

    def _parse_block(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> BlockNode:
        """Parses a block."""
        #self.expect('Equal')
        #self.step()
        self.expect('LeftBrace')
        self.step()
        body = self._accumulate_until(
            lambda: self.at_end() or self.check('RightBrace'), fn
        )
        self.expect('RightBrace')
        self.step()
        return BlockNode(body=body)  # type: ignore[arg-type]

    def _parse_classes_block(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> BlockNode:
        """Parses a block."""
        self.expect('ColonEqual')
        self.step()
        self.expect('LeftBrace')
        self.step()
        body = self._accumulate_until(
            lambda: self.at_end() or self.check('RightBrace'), fn
        )
        self.expect('RightBrace')
        self.step()
        return BlockNode(body=body)  # type: ignore[arg-type]

    def _parse_then_block(
        self,
        fn: Callable[[], Optional[Union[ExpressionNode, StatementNode]]],
    ) -> BlockNode:
        """Parses a block."""
        self.expect('Then')
        self.step()
        self.expect('LeftBrace')
        self.step()
        body = self._accumulate_until(
            lambda: self.at_end() or self.check('RightBrace'), fn
        )
        self.expect('RightBrace')
        self.step()
        return BlockNode(body=body)  # type: ignore[arg-type]

    def _parse_while(self) -> WhileNode:
        """Parses a while statement."""
        self.expect('While')
        self.step()
        condition = self._validate(
            (
                partial(  # type: ignore[arg-type]
                    self._parenthesized,
                    fn=self._process_expression,
                )
                if self.check('LeftParenthesis')
                else self._process_expression
            ),
            ('Expression',),
        )
        body = self._parse_block(self._process_expression_or_statement)
        if (orelse := None) or self.check('Else'):
            self.step()
            orelse = self._parse_block(self._process_expression_or_statement)
        return WhileNode(condition=condition, body=body, orelse=orelse)  # type: ignore[arg-type]

    def _resolve_initial(
        self,
    ) -> Union[IdentifierNode, VariableDeclarationNode]:
        """Resolves an initial declaration in a for loop."""
        return (
            self._parse_variable_declaration()
            if self.check('Variable')
            else self._parse_identifier()
        )

    def _parse_for(self) -> ForNode:
        """Parses a for statement."""
        self.expect('For')
        self.step()
        initial = (
            self._parenthesized(
                partial(
                    self._comma_separated_items,
                    fn=self._resolve_initial,
                )
            )
            if self.check('LeftParenthesis')
            else self._comma_separated_items(self._resolve_initial)
        )
        self.expect('In')
        self.step()
        condition = self._validate(self._process_expression, ('Expression',))
        body = self._parse_block(self._process_expression_or_statement)
        if (orelse := None) or self.check('Else'):
            self.step()
            orelse = self._parse_block(self._process_expression_or_statement)
        return ForNode(
            condition=condition,  # type: ignore[arg-type]
            body=body,
            orelse=orelse,
            initial=initial,  # type: ignore[arg-type]
        )

    def _parse_foreach(self) -> ForeachNode:
        """Parses a for statement."""
        self.expect('Foreach')
        self.step()
        initial = (
            self._parenthesized(
                partial(
                    self._comma_separated_items,
                    fn=self._resolve_initial,
                )
            )
            if self.check('LeftParenthesis')
            else self._comma_separated_items(self._resolve_initial)
        )
        self.expect('In')
        self.step()
        condition = self._validate(self._process_expression, ('Expression',))
        body = self._parse_block(self._process_expression_or_statement)
        if (orelse := None) or self.check('Else'):
            self.step()
            orelse = self._parse_block(self._process_expression_or_statement)
        return ForNode(
            condition=condition,  # type: ignore[arg-type]
            body=body,
            orelse=orelse,
            initial=initial,  # type: ignore[arg-type]
        )


    def _parse_break(self) -> BreakNode:
        """Parses a break statement."""
        self.expect('Break')
        break_ = BreakNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
        )
        self.step()
        return break_

    def _parse_continue(self) -> ContinueNode:
        """Parses a continue statement."""
        self.expect('Continue')
        continue_ = ContinueNode(
            row=self._current_token.row,  # type: ignore[attr-defined]
            column=self._current_token.column,  # type: ignore[attr-defined]
        )
        self.step()
        return continue_

    def _parse_if(self) -> IfNode:
        """Parses an if statement."""
        self.expect('If')
        self.step()
        condition = self._validate(
            (
                partial(  # type: ignore[arg-type]
                    self._parenthesized,
                    fn=self._process_expression,
                )
                if self.check('LeftParenthesis')
                else self._process_expression
            ),
            ('Expression',),
        )
        body = self._parse_block(self._process_expression_or_statement)
        if (orelse := None) or self.check('Else') and self.peek('If'):
            self.step()
            orelse = self._parse_if()
        elif self.check('Else'):
            self.step()
            orelse = self._parse_block(  # type: ignore[assignment]
                self._process_expression_or_statement
            )
        return IfNode(condition=condition, body=body, orelse=orelse)  # type: ignore[arg-type]
    
    def _parse_cond(self) -> CondNode:
        """Parses an if statement."""
        self.expect('Cond')
        self.step()
        condition = self._validate(
            (
                partial(  # type: ignore[arg-type]
                    self._parenthesized,
                    fn=self._process_expression,
                )
                if self.check('LeftParenthesis')
                else self._process_expression
            ),
            ('Expression',),
        )
        body = self._parse_then_block(self._process_expression_or_statement)
        if (orelse := None) or self.check('Default') and self.peek('Cond'):
            self.step()
            orelse = self._parse_cond()
        elif self.check('Default'):
            self.step()
            orelse = self._parse_block(  # type: ignore[assignment]
                self._process_expression_or_statement
            )
        return CondNode(condition=condition, body=body, orelse=orelse)  # type: ignore[arg-type]

    def _parse_case(self) -> CaseNode:
        """Parses a case of the match statement."""
        self.expect('For')
        self.step()
        condition = (
            self._parenthesized(  # type: ignore[arg-type]
                partial(
                    self._comma_separated_items,
                    fn=self._process_expression,
                )
            )
            if self.check('LeftParenthesis')
            else self._validate(
                self._process_expression,
                ('Expression',),
            )
        )
        body = self._parse_then_block(self._process_expression_or_statement)
        if (orelse := None) or self.check('Else') and self.peek('For'):
            self.step()
            orelse = self._parse_case()
        elif self.check('Else'):
            self.step()
            orelse = self._parse_block(self._process_expression_or_statement)  # type: ignore[assignment]
        return CaseNode(condition=condition, body=body, orelse=orelse)  # type: ignore[arg-type]

    def _parse_match(self) -> MatchNode:
        """Parses a match-for statement."""
        self.expect('Match')
        self.step()
        return MatchNode(
            expression=self._validate(  # type: ignore[arg-type]
                self._process_expression,
                ('Expression',),
            ),
            body=self._parse_then_block(self._parse_case),
        )

    def _parse_catch(self) -> CatchNode:
        """Parses a catch clause."""
        self.expect('Catch')
        self.step()
        return CatchNode(
            excepts=(
                self._parenthesized(  # type: ignore[arg-type]
                    partial(
                        self._comma_separated_items,
                        fn=self._parse_identifier,
                    )
                )
                if self.check('LeftParenthesis')
                else self._comma_separated_items(self._parse_identifier)
            ),
            as_=self._parse_identifier() if self.check('Identifier') else None,
            body=self._parse_block(self._process_expression_or_statement),
            orelse=self._parse_catch() if self.check('Catch') else None,
        )

    def _parse_try(self) -> TryNode:
        """Parses a try-catch statement."""
        self.expect('Try')
        self.step()
        body = self._parse_block(self._process_expression_or_statement)
        if (catch := None) or self.check('Catch'):
            catch = self._parse_catch()
        return TryNode(body=body, catch=catch)

    def _resolve_parameter(
        self,
    ) -> Optional[
        Union[VariableDeclarationNode, VariadicParameterDeclarationNode]
    ]:
        """Resolves a parameter declaration."""
        return (
            self._parse_variadic_parameter_declaration()
            if self.check('Variable')
            and self._except_current_and_next_at(0, ('Pass',))
            else (
                self._parse_variable_declaration()
                if self.check('Variable')
                else None
            )
        )

    def _parse_function(self) -> FunctionDefinitionNode:
        """Parses a function definition."""
        self.expect('Function')
        self.step()
        return FunctionDefinitionNode(
            identifier=self._parse_identifier(),
            params=self._parenthesized(  # type: ignore[arg-type]
                partial(
                    self._comma_separated_items,
                    fn=self._resolve_parameter,
                )
            ),
            body=self._parse_block(self._process_expression_or_statement),
        )
    
    def _parse_void_function(self) -> VoidFunctionDefinitionNode:
        """Parses a function definition."""
        self.expect('Void')
        self.step()
        return VoidFunctionDefinitionNode(
            identifier=self._parse_identifier(),
            params=self._parenthesized(  # type: ignore[arg-type]
                partial(
                    self._comma_separated_items,
                    fn=self._resolve_parameter,
                )
            ),
            body=self._parse_block(self._process_expression_or_statement),
        )

    def _parse_member_function(self) -> MemberFunctionDefinitionNode:
        """Parses a member function definition."""
        self.expect('Function')
        self.step()
        struct = self._parse_identifier()
        self.expect('DoubleColon')
        self.step()
        return MemberFunctionDefinitionNode(
            identifier=self._parse_identifier(),
            params=self._parenthesized(  # type: ignore[arg-type]
                partial(
                    self._comma_separated_items,
                    fn=self._resolve_parameter,
                )
            ),
            body=self._parse_block(self._process_expression_or_statement),
            struct=struct,
        )
    
    def _parse_member_void_function(self) -> VoidMemberFunctionDefinitionNode:
        """Parses a member function definition."""
        self.expect('Void')
        self.step()
        struct = self._parse_identifier()
        self.expect('DoubleAA')
        self.step()
        return VoidMemberFunctionDefinitionNode(
            identifier=self._parse_identifier(),
            params=self._parenthesized(  # type: ignore[arg-type]
                partial(
                    self._comma_separated_items,
                    fn=self._resolve_parameter,
                )
            ),
            body=self._parse_block(self._process_expression_or_statement),
            struct=struct,
        )

    def _parse_struct(self) -> StructDefinitionNode:
        """Parses a struct definition."""
        self.expect('Struct')
        self.step()
        identifier = self._parse_identifier()
        if (parents := None) or self.check('LessThan'):
            self.step()
            parents = (
                self._parenthesized(
                    partial(
                        self._comma_separated_items,
                        fn=self._parse_identifier,
                    )
                )
                if self.check('LeftParenthesis')
                else self._comma_separated_items(self._parse_identifier)
            )
        return StructDefinitionNode(
            identifier=identifier,
            body=self._parse_classes_block(
                partial(
                    self._comma_separated_items,
                    fn=self._parse_variable_declaration,
                )
            ),
            parents=parents,  # type: ignore[arg-type]
        )

    def _parse_extension(self) -> ExtensionDefinitionNode:
        """Parses a Extension definition."""
        self.expect('Extension')
        self.step()
        identifier = self._parse_identifier()
        if (parents := None) or self.check('LessThan'):
            self.step()
            parents = (
                self._parenthesized(
                    partial(
                        self._comma_separated_items,
                        fn=self._parse_identifier,
                    )
                )
                if self.check('LeftParenthesis')
                else self._comma_separated_items(self._parse_identifier)
            )
        return ExtensionDefinitionNode(
            identifier=identifier,
            body=self._parse_classes_block(
                partial(
                    self._comma_separated_items,
                    fn=self._parse_variable_declaration,
                )
            ),
            parents=parents,  # type: ignore[arg-type]
        )

    def _parse_return(self) -> ReturnNode:
        """Parses a return statement."""
        self.expect('Return')
        return_ = self._current_token
        self.step()
        return ReturnNode(
            row=return_.row,  # type: ignore[attr-defined]
            column=return_.column,  # type: ignore[attr-defined]
            expression=self._process_expression(),
        )

    def _process_expression_or_statement(
        self,
    ) -> Optional[Union[ExpressionNode, StatementNode]]:
        """Processes either an expression or a statement."""
        if self.check('Use'):
            return self._followed_by_semicolon(self._parse_use)  # type: ignore[return-value]
        elif self.check('Variable'):
            return self._followed_by_semicolon(  # type: ignore[return-value]
                self._parse_variable_declaration
            )
        # elif self.check('String'):
        #     return self._followed_by_semicolon(  # type: ignore[return-value]
        #         self._parse_variable_string_declaration
        #     )
        # elif self.check('Int'):
        #     return self._followed_by_semicolon(  # type: ignore[return-value]
        #         self._parse_variable_declaration
        #     )
        # elif self.check('Float'):
        #     return self._followed_by_semicolon(  # type: ignore[return-value]
        #         self._parse_variable_declaration
        #     )
        # elif self.check('Bool'):
        #     return self._followed_by_semicolon(  # type: ignore[return-value]
        #         self._parse_variable_declaration
        #     )
        # elif self.check('More'):
        #     return self._followed_by_semicolon(  # type: ignore[return-value]
        #         self._parse_variable_declaration
        #     )
        elif self.check('While'):
            return self._parse_while()
        elif self.check('For'):
            return self._parse_for()
        elif self.check('Foreach'):
            return self._parse_foreach()
        elif self.check('Break'):
            return self._followed_by_semicolon(self._parse_break)  # type: ignore[return-value]
        elif self.check('Continue'):
            return self._followed_by_semicolon(self._parse_continue)  # type: ignore[return-value]
        elif self.check('If'):
            return self._parse_if()
        elif self.check('Cond'):
            return self._parse_cond()
        elif self.check('Match'):
            return self._parse_match()
        elif self.check('Try'):
            return self._parse_try()
        elif self.check('Function') and not self._except_current_and_next_at(
            0, ('DoubleColon',)
        ):
            return self._parse_function()
        elif self.check('Function'):
            return self._parse_member_function()
        elif self.check('Void') and not self._except_current_and_next_at(
            0, ('DoubleAA',)
        ):
            return self._parse_void_function()
        elif self.check('Void'):
            return self._parse_member_void_function()
        elif self.check('Struct'):
            return self._parse_struct()
        elif self.check('Extension'):
            return self._parse_extension
        elif self.check('Return'):
            return self._followed_by_semicolon(self._parse_return)  # type: ignore[return-value]
        elif (
            expression := self._process_expression()
        ) is not None and self.check('Equal'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('LeftShiftEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_left_shift_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('RightShiftEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_right_shift_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('AddEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_add_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('SubtractEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_subtract_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('MultiplyEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_multiply_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('DivideEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_divide_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('ModulusEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_modulus_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        elif expression is not None and self.check('PowerEqual'):
            return self._followed_by_semicolon(
                partial(
                    self._parse_power_assignment,
                    references=(
                        expression.expressions
                        if isinstance(expression, ChainedExpressionsNode)
                        else ItemizedExpressionNode(items=[expression])
                    ),
                )
            )
        return self._followed_by_semicolon(lambda: expression)

    def parse(self, tokens_state: List[TokenState]) -> ModuleNode:
        """Parses the whole module and returns the root AST node."""
        self._tokens_state = tokens_state
        self.step()

        return ModuleNode(
            body=sum(
                partition_a_sequence(
                    self._accumulate_until(
                        self.at_end,
                        self._process_expression_or_statement,
                    ),
                    lambda x: isinstance(
                        x,
                        (
                            FunctionDefinitionNode,
                            VoidFunctionDefinitionNode,
                            StructDefinitionNode,
                            ExtensionDefinitionNode,
                            MemberFunctionDefinitionNode,
                            VoidMemberFunctionDefinitionNode
                        ),
                    ),
                ),
                [],
            )
        )


if __name__ == '__main__':
    import sys
    from pprint import pprint

    pprint(FarrParser().parse(eval(sys.stdin.read())))
