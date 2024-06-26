

from lexer.base import GroupedTokens, Token, RegexLexer


class FarrRegexLexer(RegexLexer):
    tokens = [
        GroupedTokens(
            r'/{2}.*|\/\*[\s\S]*?\*\/',
            [
                Token('SingleLineComment', r'/{2}.*', ignore=True),
                Token('SingleLineHeading', r'//{2}.*', ignore=True),
                Token('MultiLineComment', r'\/\*[\s\S]*?\*\/', ignore=True),
                Token('MultiLineComment', r'\/\/\/[\s\S]*?\/\/\/', ignore=True),
            ],
        ),
        GroupedTokens(
            r'0[box]\d+|[\-\+]?(?:\d+\.(?!\.)\d*|\d*\.(?!\.)\d+|\d+)|'
            r'r?"(?:[^"\\]|\\.)*"',
            [
                Token('Binary', r'0b\d+'),
                Token('Octal', r'0o\d+'),
                Token('Hexadecimal', r'0x\d+'),
                Token('Integer', r'[\-\+]?\d+'),
                Token('Float', r'[\-\+]?(?:\d+\.(?!\.)\d*|\d*\.(?!\.)\d+)'),
                Token('String', r'r?"(?:[^"\\]|\\.)*"'),
            ],
        ),
        GroupedTokens(
            r'[\<\>]{2}\=|[&\|\=\:\+\-\<\>]{2}|[\<\>\!\+\-\*/%\^]\=|\.{2,3}|[\s\W]',
            [
                Token('LineBreaker', r'[\n\r]', ignore=True),
                Token('Indent', r'[\040\t]', ignore=True),
                Token('LeftParenthesis', r'\('),
                Token('RightParenthesis', r'\)'),
                Token('LeftBrace', r'\{'),
                Token('RightBrace', r'\}'),
                Token('LeftBracket', r'\['),
                Token('RightBracket', r'\]'),
                Token('LeftSpike', r'\<'),
                Token('RightSpike', r'\>'),
                Token('Comma', r','),
                Token('Dot', r'\.'),
                Token('Colon', r'\:'),
                Token('DoubleColon', r'\:{2}'),
                Token('DoubleAA', r'\@{2}'),
                Token('Increment', r'\+{2}'),
                Token('Decrement', r'\-{2}'),
                Token('Semicolon', r';'),
                Token('Add', r'\+'),
                Token('Subtract', r'\-'),
                Token('Multiply', r'\*'),            

                Token('Power', r'\*{2}'),    ### NEW ###
                
                Token('SameType', r'\~\~'),    ### NEW ###
                Token('NotSametype', r'\!\~'),    ### NEW ###
                Token('SametypeandValue', r'\~\~\~'),    ### NEW ###
                Token('NotSametypeandValue', r'\!\~\~'),    ### NEW ###

                Token('StringColonEqual', r':string:='), ### NEW ###
                Token('IntColonEqual', r':int:='), ### NEW ###
                Token('FloatColonEqual', r':float:='), ### NEW ###
                Token('FloatColonEqual', r':double:='), ### NEW ###
                Token('BoolColonEqual', r':bool:='), ### NEW ###
                
                Token('Then', r'\-\>'),
                Token('Then', r'then'),
                
                Token('Divide', r'/'),
                Token('Modulus', r'%'),
                Token('Power', r'\^'),
                Token('Not', r'\!'),
                Token('And', r'&{2}'),
                Token('Or', r'\|{2}'),
                Token('Equal', r'\='),
                Token('ColonEqual', r'\:\='),
                Token('EqualEqual', r'\={2}'),
                Token('NotEqual', r'\!\='),
                Token('LeftShift', r'\<{2}'),
                Token('RightShift', r'\>{2}'),
                Token('LessThan', r'\<'),
                Token('GreaterThan', r'\>'),
                Token('LessThanOrEqual', r'\<\='),
                Token('GreaterThanOrEqual', r'\>\='),
                Token('LeftShiftEqual', r'\<{2}\='),
                Token('RightShiftEqual', r'\>{2}\='),
                Token('AddEqual', r'\+\='),
                Token('SubtractEqual', r'\-\='),
                Token('MultiplyEqual', r'\*\='),
                Token('DivideEqual', r'/\='),
                Token('ModulusEqual', r'%\='),
                Token('PowerEqual', r'\^\='),
                Token('Between', r'\.{2}'),
                Token('Pass', r'\.{3}'),
                Token('Between', r'\\between'),
                Token('Pass', r'\\pass'),
            ],
        ),
        GroupedTokens(
            r'_?[A-Za-z][A-Za-z_]*\d{,3}(?:\?\!|\!\?|\!|\?)?|\w*',
            [
                Token('Then', r'then'),
                Token('And', r'&&'),
                Token('Or', r'\|\|'),
                Token('SameType', r'~~'),    ### NEW ###
                Token('NotSametype', r'!~'),    ### NEW ###
                Token('SametypeandValue', r'~~~'),    ### NEW ###
                Token('NotSametypeandValue', r'!~~'),    ### NEW ###

                Token('Null', r'null'),
                
                Token('Use', r'use'),
                Token('Use', r'using'),  ### NEW ###
                
                Token('Variable', r'let'),
                Token('Variable', r'var'),  ### NEW ###
                Token('Variable', r'val'),  ### NEW ###

                #Token('String', r'string'),  ### NEW ### STRING 
                #Token('Int', r'int'),  ### NEW ### INT
                #Token('Float', r'float'),  ### NEW ### FLOAT
                #Token('Bool', r'bool'),  ### NEW ### BOOL
                #Token('More', r'more'),  ### NEW ### MORE
                
                Token('If', r'if'),
                Token('Else', r'else'),

                Token('Cond', r'case'),
                Token('Default', r'default'),

                Token('Match', r'match'),
                Token('While', r'while'),
                Token('Break', r'break!'),
                Token('Continue', r'continue!'),
                
                Token('For', r'for'),
                Token('For', r'foreach'),   ### NEW ###
                
                Token('In', r'in'),
                Token('Try', r'try'),
                Token('Catch', r'catch'),
                Token('Function', r'function'),
                Token('Void', r'void'),
                Token('Return', r'return!'),
                Token('Struct', r'struct'),
                Token('Struct', r'class'),
                Token('Extension', r'ecc'),  ### NEW ###
                Token('Identifier', r'.*'),
            ],
        ),
    ]


if __name__ == '__main__':
    import sys
    from pprint import pprint

    pprint(FarrRegexLexer().tokenize(sys.stdin.read()))
