#from pygments.lexers.asm import CppLexer
import re

from pygments.lexer import RegexLexer, include, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation

from pygments.lexers.supercollider import SuperColliderLexer
from pygments.token import Name, Keyword


class SCLexer(SuperColliderLexer):
    name = 'SCLexer'
    aliases = ['isc']

    EXTRA_KEYWORDS = ['SinOsc']

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'<!--', Comment),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline)
        ],
        'slashstartsregex': [
            include('commentsandwhitespace'),
            (r'/(\\.|[^[/\\\n]|\[(\\.|[^\]\\\n])*])+/'
             r'([gim]+\b|\B)', String.Regex, '#pop'),
            (r'(?=/)', Text, ('#pop', 'badregex')),
            default('#pop'),
        ],
        'badregex': [
            (r'\n', Text, '#pop')
        ],
        'root': [
            (r'^(?=\s|/|<!--)', Text, 'slashstartsregex'),
            include('commentsandwhitespace'),
            (r'\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|'
             r'(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?', Operator, 'slashstartsregex'),
            (r'[{(\[;,]', Punctuation, 'slashstartsregex'),
            (r'[})\].]', Punctuation),
            (words((
                'for', 'in', 'while', 'do', 'break', 'return', 'continue',
                'switch', 'case', 'default', 'if', 'else', 'throw', 'try',
                'catch', 'finally', 'new', 'delete', 'typeof', 'instanceof',
                'void'), suffix=r'\b'),
             Keyword, 'slashstartsregex'),
            (words(('var', 'let', 'with', 'function', 'arg'), suffix=r'\b'),
             Keyword.Declaration, 'slashstartsregex'),
            (words((
                '(abstract', 'boolean', 'byte', 'char', 'class', 'const',
                'debugger', 'double', 'enum', 'export', 'extends', 'final',
                'float', 'goto', 'implements', 'import', 'int', 'interface',
                'long', 'native', 'package', 'private', 'protected', 'public',
                'short', 'static', 'super', 'synchronized', 'throws',
                'transient', 'volatile'), suffix=r'\b'),
             Keyword.Reserved),
            (words(('true', 'false', 'nil', 'inf'), suffix=r'\b'), Keyword.Constant),
            (words((
                'Array', 'Boolean', 'Date', 'Error', 'Function', 'Number',
                'Object', 'Packages', 'RegExp', 'String',
                'isFinite', 'isNaN', 'parseFloat', 'parseInt', 'super',
                'thisFunctionDef', 'thisFunction', 'thisMethod', 'thisProcess',
                'thisThread', 'this',
                'SinOsc'), suffix=r'\b'),
             Name.Builtin),
            (r'[$A-Z]\w*', Name.Builtin),
            (words(('ar', 'kr', 'ir'), suffix=r'\b'),
             Keyword.Declaration),
            (r'[$a-z]\w*:', Keyword.Constant),
            (r'[$a-zA-Z_]\w*', Name.Other),
            (r'\\?[$a-zA-Z_]\w*', String.Symbol),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
        ]
    }

    def get_tokens_unprocessed(self, text):
        for index, token, value in SuperColliderLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
