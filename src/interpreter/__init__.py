import re
import os
import pathlib
from functools import reduce
from typing import types, Optional, Union, Any, Sequence, List, Tuple  # type: ignore[attr-defined]

import socket
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

from constants import (
    RESOURCES_ROOT_PATH,
    FILE_EXTENSION,
    LIBRARY_INITIALIZER_FILE,
)
from helpers import partition_a_sequence
from exceptions import (
    BreakError,
    ContinueError,
    ReturnError,
    InterpretError,
)
from lexer import FarrRegexLexer
from parser import FarrParser
from parser.nodes import (
    ASTNode,
    ModuleNode,
    BlockNode,
    PassNode,
    NullNode,
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
    TryNode,
    FunctionDefinitionNode,
    VoidFunctionDefinitionNode,
    MemberFunctionDefinitionNode,
    StructDefinitionNode,
    ExtensionDefinitionNode,
    ReturnNode,
)
from interpreter.base import Environment, Interpreter
from interpreter.objects import (
    FarrObject,
    PassObject,
    NullObject,
    HeterogeneousLiteralObject,
    BooleanObject,
    IntegerObject,
    FloatObject,
    StringObject,
    RangeObject,
    ListObject,
    HashMapObject,
    PairObject,
    PythonNativeObject,
    PythonNativeClassMethodObject,
    PythonNativePrintObject,
    PythonNativePrintLineObject,
    PythonNativeReadLineObject,
    PythonNativePanicObject,
    PythonNativeAssertObject,
    PythonNativeExitObject,
    PythonNativeTypeOfObject,
    PythonNativeSimilarTypesObject,
    PythonNativeShellExecutionObject,
    PythonNativeBaseErrorObject,
    PythonNativeKeyboardInterruptErrorObject,
    PythonNativeSystemExitErrorObject,
    PythonNativeArithmeticErrorObject,
    PythonNativeAssertionErrorObject,
    PythonNativeAttributeErrorObject,
    PythonNativeImportErrorObject,
    PythonNativeLookupErrorObject,
    PythonNativeNameErrorObject,
    PythonNativeOSErrorObject,
    PythonNativeRuntimeErrorObject,
    PythonNativeNotImplementedErrorObject,
    PythonNativeTypeErrorObject,
    PythonNativeValueErrorObject,
    PythonNativeDeprecatedErrorObject,
    StructInstanceObject,
    VoidFunctionDefinitionObject,
    ExtensionInstanceObject,
    ModuleObject,
    LibraryObject,
    NonPythonNativeObject,
    FunctionDefinitionObject,
    StructDefinitionObject,
    ExtensionDefinitionObject,

    SystemConsole,
    SystemRaise,
    SystemMath,
    SystemChars,
    SystemBasicScience,
    JSONInterpreter,
    TimeObjLib,
    UseModLib,
    DateTimeObjLib,
    FSONInterpreter,
    SocketLIB,
    #Hashlib,
    #FernetLib,
    #Hashlib,
    cryptohh,
    cryptofernet,
    LenghtLIB,
    TypeLIB,
    
    PyTorchLIB,
    NumPyLIB,
    PandasLIB,
    MatplotlibLIB,
    
    #LearnForgeLIB,
    #TensorForgeLIB,
    #LinePredictorLIB,

    Shell,
    PowerShell,
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

class FarrInterpreter(Interpreter):
    builtin_symbols = {
       f'Null': NullObject(),
       f'True': BooleanObject(value=True),
       f'False': BooleanObject(value=False),
       f'True': BooleanObject(value=True),
       f'False': BooleanObject(value=False),
       f'Yes': BooleanObject(value=True),
       f'No': BooleanObject(value=False),
       f'print': PythonNativePrintObject(),
       f'println': PythonNativePrintLineObject(),

       f'Console': SystemConsole(), ### NEW ###
       #f'console': SystemConsole(), ### NEW ###
       
       f'Raise': SystemRaise(), ### NEW ###
       #f'raise': SystemRaise(), ### NEW ###
       
       f'SysChars': SystemChars(), ### NEW ###
       #f'chars': SystemChars(), ### NEW ###
       
       f'Math': SystemMath(), ### NEW ###
       #f'math': SystemMath(), ### NEW ###
       
       f'PhMath': SystemBasicScience(), ### NEW ###
       #f'bp': SystemBasicScience(), ### NEW ###

       f'Json': JSONInterpreter(), ### NEW ###
       #f'json': JSONInterpreter(), ### NEW ###

       f'Fson': FSONInterpreter(), ### NEW ###
       #f'fson': FSONInterpreter(), ### NEW ###

       f'SysTime': TimeObjLib(), ### NEW ###
       #f'time': TimeObjLib(), ### NEW ###

       f'Datetime': DateTimeObjLib(), ### NEW ###
       #f'datetime': DateTimeObjLib(), ### NEW ###

       f'Module': UseModLib(), ### NEW ###  ERROR ##########################
       #f'lib': UseModLib(), ### NEW ###    ERROR ##########################

       f'Socket': SocketLIB(), ### NEW ###
       #f'socket': SocketLIB(), ### NEW ###
       
       f'CryptoCipher': cryptofernet(), ### NEW ###
       #f'cipher': cryptofernet(), ### NEW ###
       
       f'CryptoHash': cryptohh(), ### NEW ###
       #f'hash': cryptohh(), ### NEW ###

       f'Len':LenghtLIB(),
       #f'len':LenghtLIB(),

       f'Type':TypeLIB(),
       #f'type':TypeLIB(),
       
       f'Lighter':PyTorchLIB(),
       #f'pytorch':PyTorchLIB(),
       
       f'Numpulse':NumPyLIB(),
       #f'numpy':NumPyLIB(),
       
       f'Pandamonium':PandasLIB(),
       #f'pandia':PandasLIB(),
       
       f'Graphia':MatplotlibLIB(),
       #f'graphia':MatplotlibLIB(),
       
       # f'ForgeLearn':LearnForgeLIB(),
       # f'learnf':LearnForgeLIB(),
       
       # f'ForgeTensor':TensorForgeLIB(),
       # f'tensorf':TensorForgeLIB(),

       # f'FutureData':LinePredictorLIB(),
       # f'ftdata':LinePredictorLIB(),

       f'CmdShell':Shell(),
       f'shell':Shell(),

       f'PowerShell':PowerShell(),
       f'pshell':PowerShell(),

       f'readln_e': PythonNativeReadLineObject(),
       f'Panic_eq': PythonNativePanicObject(),
       f'Assert_e': PythonNativeAssertObject(),
       f'exit_e': PythonNativeExitObject(),
       f'Typeof_q': PythonNativeTypeOfObject(),
       f'Similartypes_q': PythonNativeSimilarTypesObject(),
       f'Cmd_eq': PythonNativeShellExecutionObject(),
        
       f'BaseError': PythonNativeBaseErrorObject,
       f'KeyboardInterruptError': PythonNativeKeyboardInterruptErrorObject,
       f'SystemExitError': PythonNativeSystemExitErrorObject,
       f'ArithmeticError': PythonNativeArithmeticErrorObject,
       f'AssertionError': PythonNativeAssertionErrorObject,
       f'AttributeError': PythonNativeAttributeErrorObject,
       f'ImportError': PythonNativeImportErrorObject,
       f'LookupError': PythonNativeLookupErrorObject,
       f'NameError': PythonNativeNameErrorObject,
       f'OSError': PythonNativeOSErrorObject,
       f'RuntimeError': PythonNativeRuntimeErrorObject,
       f'NotImplementedError': PythonNativeNotImplementedErrorObject,
       f'TypeError': PythonNativeTypeErrorObject,
       f'ValueError': PythonNativeValueErrorObject,
       f'DeprecatedError': PythonNativeDeprecatedErrorObject,
    }

    def _interpret_module_node(self, node: ModuleNode) -> None:
        """Interprets a `ModuleNode`."""
        for child in node.body:
            self._interpret(child)
        return None

    def _interpret_block_node(self, node: BlockNode) -> None:
        """Interprets a `BlockNode`."""
        for child in node.body:
            self._interpret(child)
        return None

    def _interpret_pass_node(self, node: PassNode) -> PassObject:
        """Returns a `PassObject`."""
        return PassObject()

    def _interpret_null_node(self, node: NullNode) -> NullObject:
        """Returns a `NullObject`."""
        return NullObject()

    def _interpret_binary_node(self, node: BinaryNode) -> IntegerObject:
        """Converts a `BinaryNode` to a `IntegerObject`."""
        return IntegerObject(value=int(node.value, 2))

    def _interpret_octal_node(self, node: OctalNode) -> IntegerObject:
        """Converts an `OctalNode` to an `IntegerObject`."""
        return IntegerObject(value=int(node.value, 8))

    def _interpret_hexadecimal_node(
        self,
        node: HexadecimalNode,
    ) -> IntegerObject:
        """Converts a `HexadecimalNode` to a `IntegerObject`."""
        return IntegerObject(value=int(node.value, 16))

    def _interpret_integer_node(self, node: IntegerNode) -> IntegerObject:
        """Converts an `IntegerNode` to an `IntegerObject`."""
        return IntegerObject(value=int(node.value))

    def _interpret_float_node(self, node: FloatNode) -> FloatObject:
        """Converts a `FloatNode` to a `FloatObject`."""
        return FloatObject(value=float(node.value))

    def _interpolate(self, match_: re.Match) -> str:
        """Interpolates and executes a match."""
        return f''.join(
            map(
                lambda x: str(self._interpret(x)),
                FarrParser()
                .parse(FarrRegexLexer().tokenize(f'{match_.group(1)};'))
                .body,
            )
        )

    def _interpret_string_node(self, node: StringNode) -> StringObject:
        """Converts a `StringNode` to a `StringObject`."""
        return StringObject(
            value=re.sub(
                r'(?<!//)/$/{(.*?)/}',
                self._interpolate,
                (
                    cleaned_value.translate(
                        str.maketrans(
                            {  # type: ignore[arg-type]
                               f'/n': r'//n',
                               f'/t': r'//t',
                               f'/b': r'//b',
                               f'/r': r'//r',
                               f'/"': r'///"',
                               f'//': r'////',
                            }
                        )
                    )
                    if (
                        (cleaned_value := re.sub(r'^r?"|"$',f'', node.value))
                        and node.value.startswith('r')
                    )
                    else re.sub(
                        r'//([ntrb"//])',
                        lambda match_: {
                           f'n':f'/n',
                           f't':f'/t',
                           f'r':f'/r',
                           f'b':f'/b',
                           f'"':f'"',
                           f'//':f'//',
                        }.get(
                            match_.group(1), None  # type: ignore[arg-type]
                        ),
                        cleaned_value,
                    )
                ),
            )
        )

    def _interpret_identifier_node(self, node: IdentifierNode) -> Any:
        """Returns the stored value."""
        return self.environment.locate(node.value)

    def _interpret_range_node(self, node: RangeNode) -> RangeObject:
        """Converts a `RangeNode` to a `RangeObject`."""
        return RangeObject(
            from_=self._interpret(node.from_),
            to=self._interpret(node.to) if node.to is not None else None,
            by=self._interpret(node.by) if node.by is not None else None,
        )

    def _interpret_itemized_expression_node(
        self,
        node: ItemizedExpressionNode,
    ) -> List[Optional[FarrObject]]:
        """Interprets a list of nodes."""
        return [
            result
            for item in node.items
            if (result := self._interpret(item)) is not None
        ]

    def _process_chain_target(
        self,
        x: Union[ASTNode, FarrObject],
        y: ASTNode,
    ) -> FarrObject:
        """Handles the next part of the chain."""
        if (
            result := self._interpret(x) if isinstance(x, ASTNode) else x
        ) and isinstance(y, IdentifierNode):
            if isinstance(
                target := getattr(result, y.value), NonPythonNativeObject
            ):
                target.environment = result.environment
            return (
                PythonNativeClassMethodObject(method=target)
                if isinstance(target, types.MethodType)
                else target
            )
        elif isinstance(y, CallNode):
            if isinstance(
                target := getattr(result, y.invoke.value), NonPythonNativeObject
            ):
                target.environment = result.environment
            return (
                self._call_python_native_object(target, y.args)  # type: ignore[return-value]
                if isinstance(target, types.MethodType)
                else self._call_non_python_native_object(target, y.args)
            )
        return result[self._interpret(y)]

    def _interpret_chained_expressions_node(
        self,
        node: ChainedExpressionsNode,
    ) -> FarrObject:
        """Returns the result of a chain of expressions."""
        return reduce(self._process_chain_target, node.expressions.items)  # type: ignore[return-value, arg-type]

    def _interpret_list_node(self, node: ListNode) -> ListObject:
        """Converts a `ListNode` to a `ListObject`."""
        return ListObject(elements=self._interpret(node.elements))

    def _interpret_hash_map_node(self, node: HashMapNode) -> HashMapObject:
        """Converts a `HashMapNode` to a `HashMapObject`."""
        return HashMapObject(
            pairs=(
                self._interpret(node.pairs) if node.pairs is not None else []
            )
        )

    def _interpret_pair_node(self, node: PairNode) -> PairObject:
        """Converts a `PairNode` to a `PairObject`."""
        return PairObject(
            key=self._interpret(node.key),
            value=self._interpret(node.value),
        )

    def _populate_params(
        self,
        params: ItemizedExpressionNode,
        args: ItemizedExpressionNode,
    ) -> None:
        """Tries to assign arguments to parameters."""
        required, optional = partition_a_sequence(
            params.items, lambda x: x.expression is None
        )
        required, variadic = partition_a_sequence(
            required,
            lambda x: not isinstance(x, VariadicParameterDeclarationNode),
        )
        args_, kwargs = partition_a_sequence(
            args.items, lambda x: not isinstance(x, AssignmentNode)
        )
        args_, exp_args = partition_a_sequence(
            args_, lambda x: not isinstance(x, ExpandableArgumentNode)
        )
        if len(args.items) > len(params.items) and not variadic:
            print(f"{Colors.bright_red}    TypeError{Colors.red}",
               f'Too many arguments provided.f'
               f'Please check the function definition{Colors.reset}.'
            )
        elif len(args.items) < len(required) and not variadic and not exp_args:
            print(f"{Colors.bright_red}    TypeError{Colors.red}",
               f'Not enough arguments provided for the required parameters{Colors.reset}.'
            )
        elif len(args_) > len(required) and not variadic:
            print(f"{Colors.bright_red}    TypeError{Colors.red}",
               f'Provided more positional arguments than the function accepts{Colors.reset}.'
            )
        elif not args_ and not exp_args and required:
            print(f"{Colors.bright_red}    TypeError{Colors.red}",'Required parameters are missing arguments{Colors.reset}.')
        elif (args_ or exp_args) and not required and optional:
            print(f"{Colors.bright_red}    TypeError{Colors.red}",
               f'Positional arguments provided but the function expectsf'
               f'only keyword arguments{Colors.reset}.'
            )
        elif kwargs and not optional:
            print(f"{Colors.bright_red}    TypeError{Colors.red}",
               f'Keyword arguments provided but the function does not accept them{Colors.reset}.'
            )
        elif kwargs and set(
            map(lambda x: x.references.items[0].value, kwargs)
        ).isdisjoint(map(lambda x: x.identifier.value, optional)):
            print(f"{Colors.bright_red}    TypeError{Colors.red}",
               f'Provided keyword arguments do not correspond to any optionalf'
               f'parameters. Please check the function definition for validf'
               f'parameter names{Colors.reset}.'
            )
        elif len(variadic) > 1:
            print(f"{Colors.bright_red}    TypeError{Colors.red}",
               f'Multiple variadic parameters defined.f'
               f'A function can only have one variadic parameter{Colors.reset}.'
            )

        for param, arg in zip(required.copy(), args_.copy()):
            required.pop(0)
            args_.pop(0)
            self.environment.assign(param.identifier.value, arg)
        if (
            exp_args
            and (exp_args := exp_args.pop(0).expression)
            and variadic
            and not required
        ):
            self.environment.assign(variadic.pop(0).identifier.value, exp_args)
        elif (
            exp_args
            and len(exp_args.elements) == len(required)  # type: ignore[attr-defined]
            and not variadic
        ):
            for param, arg in zip(required, exp_args):
                self.environment.assign(param.identifier.value, arg)
        elif exp_args and required:
            for param, arg in zip(required.copy(), exp_args.elements.copy()):  # type: ignore[attr-defined]
                required.pop(0)
                exp_args.elements.pop(0)  # type: ignore[attr-defined]
                self.environment.assign(param.identifier.value, arg)
            if exp_args and not variadic:
                print(f"{Colors.bright_red}    TypeError{Colors.red}",
                   f'Extra arguments remain after unpacking, but no variadicf'
                   f'parameter is available to receive them{Colors.reset}.'
                )
            variadic_ = self.environment.locate(
                variadic.pop(0).identifier.value
            )
            variadic_.elements.extend(exp_args)
        elif args_ and variadic:
            variadic_ = self.environment.locate(
                variadic.pop(0).identifier.value
            )
            variadic_.elements.extend(args_)
        for kwarg in kwargs:
            if not self.environment.exists(
                name := kwarg.references.items.copy().pop().value, 0
            ):
                raise NameError(f'There is no parameter name `{name}`!')
            self.environment.assign(name, kwarg.expression)
        return None

    def _call_non_python_native_object(
        self,
        invoke: NonPythonNativeObject,
        args: ItemizedExpressionNode,
    ) -> FarrObject:
        """Calls native objects of our language."""
        args_, kwargs = partition_a_sequence(
            args.items, lambda x: not isinstance(x, AssignmentNode)
        )
        args_, exp_args = partition_a_sequence(
            args_, lambda x: not isinstance(x, ExpandableArgumentNode)
        )
        args_ = list(map(self._interpret, args_))
        exp_args = list(
            map(
                lambda x: ExpandableArgumentNode(
                    expression=self._interpret(x.expression)
                ),
                exp_args,
            )
        )
        kwargs = list(
            map(
                lambda x: AssignmentNode(
                    references=x.references,
                    expression=self._interpret(x.expression),
                ),
                kwargs,
            )
        )

        environment_backup = self.environment
        self.environment = Environment(
            parent=(
                invoke.environment
                if invoke.environment is not None
                else self.environment
            )
        )
        self._interpret(
            invoke.params
            if isinstance(invoke, FunctionDefinitionObject)
            else invoke.attributes  # type: ignore[attr-defined]
        )
        self._populate_params(
            (
                invoke.params
                if isinstance(
                    invoke,
                    FunctionDefinitionObject,
                )
                else invoke.attributes  # type: ignore[attr-defined]
            ),
            ItemizedExpressionNode(items=sum([args_, exp_args, kwargs], [])),
        )
        try:
            self._interpret(invoke.body)
        except ReturnError as e:
            result = e.expression
        else:
            result = (
                StructInstanceObject(environment=self.environment.copy())
                if isinstance(invoke, StructDefinitionObject)
                else NullObject()
            )
        self.environment = environment_backup
        return result  # type: ignore[return-value]

    def _call_python_native_object(
        self,
        invoke: PythonNativeObject,
        args: ItemizedExpressionNode,
    ) -> Optional[FarrObject]:
        """Calls Python native objects with respect to arguments."""
        args_, kwargs = partition_a_sequence(
            args.items, lambda x: not isinstance(x, AssignmentNode)
        )
        return invoke(  # type: ignore[operator]
            *map(self._interpret, args_),
            **dict(
                map(
                    lambda x: (
                        x.references.items.copy().pop(0).value,
                        self._interpret(x.expression),
                    ),
                    kwargs,
                )
            ),
        )

    def _interpret_call_node(self, node: CallNode) -> FarrObject:
        """Calls a callable object with the taken arguments."""
        return (
            self._call_non_python_native_object(invoke, node.args)  # type: ignore[return-value]
            if isinstance(
                invoke := self._interpret(node.invoke), NonPythonNativeObject
            )
            else self._call_python_native_object(invoke, node.args)
        )

    def _interpret_grouped_expression_node(
        self,
        node: GroupedExpressionNode,
    ) -> FarrObject:
        """Interprets grouped expressions."""
        return self._interpret(node.expression)

    def _interpret_negation_operation_node(
        self,
        node: NegationOperationNode,
    ) -> BooleanObject:
        """Interprets a negation operation."""
        return BooleanObject(value=not self._interpret(node.operand))

    def _interpret_pre_increment_node(
        self,
        node: PreIncrementNode,
    ) -> Union[IntegerObject, FloatObject]:
        """Adds one unit to the previous value and returns it."""
        *pointers, target = node.operand.items  # type: ignore[attr-defined]
        if not pointers:
            self.environment.replace(
                target.value,
                result := self.environment.locate(target.value)
                + IntegerObject(value=1),
            )
            return result
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[target] = (
                result := (
                    pointer[target := self._interpret(target)]
                    + IntegerObject(value=1)
                )
            )
            return result
        pointer.environment.replace(
            target.value,
            result := pointer.environment.locate(target.value)
            + IntegerObject(value=1),
        )
        return result

    def _interpret_pre_decrement_node(
        self,
        node: PreDecrementNode,
    ) -> Union[IntegerObject, FloatObject]:
        """Subtracts one unit from the previous value and returns it."""
        *pointers, target = node.operand.items  # type: ignore[attr-defined]
        if not pointers:
            self.environment.replace(
                target.value,
                result := self.environment.locate(target.value)
                - IntegerObject(value=1),
            )
            return result
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[target] = (
                result := (
                    pointer[target := self._interpret(target)]
                    - IntegerObject(value=1)
                )
            )
            return result
        pointer.environment.replace(
            target.value,
            result := pointer.environment.locate(target.value)
            - IntegerObject(value=1),
        )
        return result

    def _interpret_post_increment_node(
        self,
        node: PostIncrementNode,
    ) -> Union[IntegerObject, FloatObject]:
        """Returns the previous value and then adds one to it."""
        *pointers, target = node.operand.items  # type: ignore[attr-defined]
        if not pointers:
            self.environment.replace(
                target.value,
                (result := self.environment.locate(target.value))
                + IntegerObject(value=1),
            )
            return result
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[target] = (
                result := pointer[target := self._interpret(target)]
            ) + IntegerObject(value=1)
            return result
        pointer.environment.replace(
            target.value,
            (result := pointer.environment.locate(target.value))
            + IntegerObject(value=1),
        )
        return result

    def _interpret_post_decrement_node(
        self,
        node: PostDecrementNode,
    ) -> Union[IntegerObject, FloatObject]:
        """Returns the previous value and then subtracts one from it."""
        *pointers, target = node.operand.items  # type: ignore[attr-defined]
        if not pointers:
            self.environment.replace(
                target.value,
                (result := self.environment.locate(target.value))
                - IntegerObject(value=1),
            )
            return result
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[target] = (
                result := pointer[target := self._interpret(target)]
            ) - IntegerObject(value=1)
            return result
        pointer.environment.replace(
            target.value,
            (result := pointer.environment.locate(target.value))
            - IntegerObject(value=1),
        )
        return result

    def _interpret_arithmetic_operation_node(
        self,
        node: ArithmeticOperationNode,
    ) -> Optional[HeterogeneousLiteralObject]:
        """Interprets a mathematical operation."""
        left = self._interpret(node.left)
        right = self._interpret(node.right)

        match node.operator:
            case 'LeftShift':
                return left << right
            case 'RightShift':
                return left >> right
            case 'Add':
                return left + right
            case 'Subtract':
                return left - right
            case 'Multiply':
                return left * right
            case 'Divide':
                return left / right
            case 'Modulus':
                return left % right
            case 'Power':
                return left**right
        return None

    def _interpret_relational_operation_node(
        self,
        node: RelationalOperationNode,
    ) -> Optional[BooleanObject]:
        """Interprets a comparison operation."""
        left = self._interpret(node.left)
        right = self._interpret(node.right)

        match node.operator:
            case 'EqualEqual':
                return left == right
            case 'NotEqual':
                return left != right
            case 'LessThan':
                return left < right
            case 'GreaterThan':
                return left > right
            case 'LessThanOrEqual':
                return left <= right
            case 'GreaterThanOrEqual':
                return left >= right
        return None

    def _interpret_logical_operation_node(
        self,
        node: LogicalOperationNode,
    ) -> FarrObject:
        """Interprets logical operations."""
        left = self._interpret(node.left)
        right = self._interpret(node.right)

        match node.operator:
            case 'And':
                return left and right
            case 'Or':
                return left or right
        return None  # type: ignore[return-value]

    def _interpret_ternary_operation_node(
        self,
        node: TernaryOperationNode,
    ) -> FarrObject:
        """Interprets a condition as an expression."""
        return (
            self._interpret(node.then)
            if self._interpret(node.condition)
            else (
                self._interpret(node.orelse)
                if node.orelse is not None
                else None
            )
        )

    def _resolve_import_path(self, path: ItemizedExpressionNode) -> Union[pathlib.Path, List[pathlib.Path], None]:
        """Validates and returns the required path(s)."""
        resources_root_path = os.getenv(RESOURCES_ROOT_PATH, "E:/enchant/sbin/Infiniti-Lang/all/mip/infiniti3")
        
        if not resources_root_path:
            print(f"{Colors.red}OsError: {Colors.bright_red}The `{RESOURCES_ROOT_PATH}` environment variable is not set{Colors.reset}")
            return None
        
        target = pathlib.Path(resources_root_path) / 'libs'
        for part in map(lambda x: x.value, path.items):  # type: ignore[union-attr]
            target /= part

            if target.is_file() and target.suffix == f".{FILE_EXTENSION}":
                return target

            if not target.exists():
                print(f"{Colors.red}OsError: {Colors.bright_red}There is no file or folder named `{target}`{Colors.reset}")
                return None

            if target.is_dir() and not (target / LIBRARY_INITIALIZER_FILE).is_file():
                print(f"{Colors.red}ImportError: {Colors.bright_red}There is no `{LIBRARY_INITIALIZER_FILE}` in `{target}` directory{Colors.reset}")
                return None

        if target.is_dir():
            return list(target.glob(f"*.{FILE_EXTENSION}"))
        else:
            return target.with_suffix(f".{FILE_EXTENSION}")

    def _create_module_environment(self, file_path: pathlib.Path) -> Environment:
        """Returns the environment of the interpreted module."""
        interpreter = FarrInterpreter()
        interpreter._interpret(
            FarrParser().parse(FarrRegexLexer().tokenize(file_path.read_text()))
        )
        return interpreter.environment.copy()

    def _interpret_use_node(self, node: Any) -> None:
        """Handles the import of a library or module."""
        resolved_path = self._resolve_import_path(node.path)
        if resolved_path is None:
            return

        if isinstance(resolved_path, pathlib.Path):
            self.environment.assign(
                resolved_path.stem,
                ModuleObject(environment=self._create_module_environment(resolved_path))
            )
            return

        library_initializer, modules_path = partition_a_sequence(
            resolved_path, lambda x: x.name == LIBRARY_INITIALIZER_FILE
        )
        if not library_initializer:
            print(f"{Colors.red}ImportError: {Colors.bright_red}No initializer file `{LIBRARY_INITIALIZER_FILE}` found in library{Colors.reset}")
            return

        library_environment = self._create_module_environment(library_initializer[0])

        for module_path in modules_path:
            library_environment.assign(
                module_path.stem,
                ModuleObject(environment=self._create_module_environment(module_path))
            )

        self.environment.assign(
            library_initializer[0].parent.stem,
            LibraryObject(environment=library_environment)
        )

    def _interpret_variable_declaration_node(
        self,
        node: VariableDeclarationNode,
    ) -> None:
        """Defines a variable in the environment."""
        self.environment.assign(
            node.identifier.value,
            (
                self._interpret(node.expression)
                if node.expression is not None
                else NullObject()
            ),
        )

    def _interpret_variadic_parameter_declaration_node(
        self,
        node: VariadicParameterDeclarationNode,
    ) -> None:
        """Interprets a variadic parameter declaration node."""
        self.environment.assign(
            node.identifier.value,
            (
                self._interpret(node.expression)
                if node.expression is not None
                else ListObject(elements=[])
            ),
        )

    def _interpret_assignment_node(self, node: AssignmentNode) -> None:
        """Updates the content of a variable."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value, self._interpret(node.expression)  # type: ignore[union-attr]
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] = self._interpret(node.expression)
            return None
        pointer.environment.replace(
            target.value, self._interpret(node.expression)  # type: ignore[union-attr]
        )

    def _interpret_left_shift_assignment_node(
        self,
        node: LeftShiftAssignmentNode,
    ) -> None:
        """Performs a left shift assignment on the target variable."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                << self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] <<= self._interpret(
                node.expression
            )
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            << self._interpret(node.expression),
        )

    def _interpret_right_shift_assignment_node(
        self,
        node: RightShiftAssignmentNode,
    ) -> None:
        """Performs a right shift assignment on the target variable."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                >> self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] >>= self._interpret(
                node.expression
            )
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            >> self._interpret(node.expression),
        )

    def _interpret_add_assignment_node(self, node: AddAssignmentNode) -> None:
        """Adds something to the previous value."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                + self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] += self._interpret(node.expression)
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            + self._interpret(node.expression),
        )

    def _interpret_subtract_assignment_node(
        self,
        node: SubtractAssignmentNode,
    ) -> None:
        """Subtracts something from the previous value."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                - self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] -= self._interpret(node.expression)
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            - self._interpret(node.expression),
        )

    def _interpret_multiply_assignment_node(
        self,
        node: MultiplyAssignmentNode,
    ) -> None:
        """Multiplies something by the previous value."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                * self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] *= self._interpret(node.expression)
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            * self._interpret(node.expression),
        )

    def _interpret_divide_assignment_node(
        self,
        node: DivideAssignmentNode,
    ) -> None:
        """Divides something by the previous value."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                / self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] /= self._interpret(node.expression)
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            / self._interpret(node.expression),
        )

    def _interpret_modulus_assignment_node(
        self,
        node: ModulusAssignmentNode,
    ) -> None:
        """Calculates the remainder of dividing the previous value by something."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                % self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] %= self._interpret(node.expression)
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            % self._interpret(node.expression),
        )

    def _interpret_power_assignment_node(
        self,
        node: PowerAssignmentNode,
    ) -> None:
        """Raises the previous value to the power of something."""
        *pointers, target = node.references.items
        if not pointers:
            self.environment.replace(
                target.value,  # type: ignore[union-attr]
                self.environment.locate(target.value)  # type: ignore[union-attr]
                ** self._interpret(node.expression),
            )
            return None
        pointer = self._interpret(pointers.pop(0))
        while pointers:
            pointer = (
                getattr(pointer, link.value)  # type: ignore[union-attr]
                if not isinstance(link := pointers.pop(0), RangeNode)
                else pointer[self._interpret(link)]
            )
        if not hasattr(pointer,f'environment'):
            pointer[self._interpret(target)] **= self._interpret(
                node.expression
            )
            return None
        pointer.environment.replace(
            target.value,  # type: ignore[union-attr]
            pointer.environment.locate(target.value)  # type: ignore[union-attr]
            ** self._interpret(node.expression),
        )

    def _interpret_while_node(self, node: WhileNode) -> None:
        """Interprets a `WhileNode`."""
        while self._interpret(node.condition):
            try:
                self._interpret(node.body)
            except BreakError:
                break
            except ContinueError:
                continue
        else:
            if node.orelse is not None:
                self._interpret(node.orelse)
        return None

    def _interpret_for_node(self, node: ForNode) -> None:
        """Interprets a `ForNode`."""
        self._interpret(node.initial)
        for iteration in self._interpret(node.condition):
            for variable, value in zip(
                node.initial.items,
                iteration if isinstance(iteration, Sequence) else (iteration,),
            ):
                self.environment.assign(
                    (
                        variable.value
                        if isinstance(variable, IdentifierNode)
                        else variable.identifier.value  # type: ignore[union-attr]
                    ),
                    value,
                )
            try:
                self._interpret(node.body)
            except BreakError:
                break
            except ContinueError:
                continue
        else:
            if node.orelse is not None:
                self._interpret(node.orelse)
        return None

    def _interpret_foreach_node(self, node: ForeachNode) -> None:
        """Interprets a `ForNode`."""
        self._interpret(node.initial)
        for iteration in self._interpret(node.condition):
            for variable, value in zip(
                node.initial.items,
                iteration if isinstance(iteration, Sequence) else (iteration,),
            ):
                self.environment.assign(
                    (
                        variable.value
                        if isinstance(variable, IdentifierNode)
                        else variable.identifier.value  # type: ignore[union-attr]
                    ),
                    value,
                )
            try:
                self._interpret(node.body)
            except BreakError:
                break
            except ContinueError:
                continue
        else:
            if node.orelse is not None:
                self._interpret(node.orelse)
        return None


    def _interpret_break_node(self, node: BreakNode) -> None:
        """Throws a `BreakError` exception."""
        raise BreakError('If there was a loop, it was broken!')

    def _interpret_continue_node(self, node: ContinueNode) -> None:
        """Throws a `ContinueError` exception."""
        raise ContinueError('If you can go to the next round!')

    def _interpret_if_node(self, node: IfNode) -> None:
        """Interprets an `IfNode`."""
        if self._interpret(node.condition):
            self._interpret(node.body)
        elif node.orelse is not None:
            self._interpret(node.orelse)
        return None

    def _interpret_cond_node(self, node: CondNode) -> None:
        """Interprets an `CONDNode`."""
        if self._interpret(node.condition):
            self._interpret(node.body)
        elif node.orelse is not None:
            self._interpret(node.orelse)
        return None

    def _interpret_match_node(self, node: MatchNode) -> None:
        """Interprets a match-for statement."""
        result = self._interpret(node.expression)
        case = node.body.body.pop(0)
        while case is not None:
            if isinstance(case, BlockNode):
                self._interpret(case)
                return None
            elif (
                not isinstance(case.condition, ItemizedExpressionNode)  # type: ignore[union-attr]
                and result == self._interpret(case.condition)  # type: ignore[union-attr]
            ) or result in self._interpret(
                case.condition  # type: ignore[union-attr]
            ):
                self._interpret(case.body)  # type: ignore[union-attr]
                return None
            case = case.orelse  # type: ignore[union-attr]
        return None

    def _interpret_try_node(self, node: TryNode) -> None:
        """Manages trial and error."""
        try:
            self._interpret(node.body)
        except InterpretError as e:  # noqa: F841
            catch = node.catch
            while catch is not None:
                if matches := list(
                    filter(
                        lambda x: issubclass(  # type: ignore[arg-type]
                            e.error.__class__,  # noqa: F821
                            x.__bases__,  # type: ignore[attr-defined]
                        ),
                        map(
                            lambda x: self.environment.locate(x.value),  # type: ignore[union-attr]
                            catch.excepts.items,
                        ),
                    )
                ):
                    self.environment = Environment(parent=self.environment)
                    if catch.as_ is not None:
                        self.environment.assign(catch.as_.value, matches.pop(0))
                    self._interpret(catch.body)
                    self.environment = self.environment.parent  # type: ignore[assignment]
                    break
                catch = catch.orelse
            else:
                if node.catch is not None:
                    raise
        return None

    def _interpret_function_definition_node(
        self,
        node: FunctionDefinitionNode,
    ) -> None:
        """Defines a `FunctionDefinitionObject` in the environment."""
        self.environment.assign(
            node.identifier.value,
            FunctionDefinitionObject(
                body=node.body,  # type: ignore[arg-type]
                params=node.params,
            ),
        )

    def _interpret_member_function_definition_node(
        self,
        node: MemberFunctionDefinitionNode,
    ) -> None:
        """Adds a `FunctionDefinitionNode` to the body of the struct."""
        struct = self.environment.locate(node.struct.value)
        struct.body.body.append(
            FunctionDefinitionNode(
                identifier=node.identifier,
                body=node.body,
                params=node.params,
            )
        )
        
    def _interpret_member_function_extension_definition_node(
        self,
        node: MemberFunctionDefinitionNode,
    ) -> None:
        """Adds a `FunctionDefinitionNode` to the body of the struct."""
        extension = self.environment.locate(node.extension.value)
        extension.body.body.append(
            FunctionDefinitionNode(
                identifier=node.identifier,
                body=node.body,
                params=node.params,
            )
        )


    def _populate_on_parents(
        self,
        body: BlockNode,
        parents: Optional[ItemizedExpressionNode],
    ) -> Tuple[BlockNode, ItemizedExpressionNode]:
        """Collects all parent properties."""
        attributes = (
            body.body.pop() if body.body else ItemizedExpressionNode(items=[])
        )
        for parent in map(
            lambda x: self.environment.locate(x.value),  # type: ignore[union-attr]
            parents.items if parents is not None else [],
        ):
            attributes.items = parent.attributes.items + attributes.items  # type: ignore[union-attr]
            body.body = parent.body.body + body.body
        return body, attributes  # type: ignore[return-value]

    def _interpret_struct_definition_node(
        self,
        node: StructDefinitionNode,
    ) -> None:
        """Defines a `StructDefinitionObject` in the environment."""
        body, attributes = self._populate_on_parents(node.body, node.parents)  # type: ignore[arg-type]
        self.environment.assign(
            node.identifier.value,
            StructDefinitionObject(
                body=body,
                attributes=attributes,
            ),
        )

    def _interpret_extension_definition_node(
        self,
        node: ExtensionDefinitionNode,
    ) -> None:
        """Defines a `ExtensionDefinitionObject` in the environment."""
        body, attributes = self._populate_on_parents(node.body, node.parents)  # type: ignore[arg-type]
        self.environment.assign(
            node.identifier.value,
            ExtensionDefinitionObject(
                body=body,
                attributes=attributes,
            ),
        )

    def _interpret_return_node(self, node: ReturnNode) -> None:
        """Throws a `ReturnError` exception."""
        raise ReturnError(
            expression=(
                self._interpret(node.expression)
                if node.expression is not None
                else NullObject()
            )
        )


if __name__ ==f'__main__':
    import sys

    FarrInterpreter().interpret(eval(sys.stdin.read()))
