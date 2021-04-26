# -*- coding: utf-8 -*-
"""
    Portugol Studio lexer
    ~~~~~~~~~~~

    Pygments lexer for Portugol Studio, a algorithmic language for beginners in Portuguese.

    :copyright: Copyright 2021 Héliton Martins
    :license: GPL v3.0, see LICENSE for details.
"""

import re
from pygments.token import Name, Keyword

from pygments.lexer import RegexLexer, include, bygroups, using, \
    this, inherit, default, words
from pygments.util import get_bool_opt
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Error


class PortugolStudioLexer(RegexLexer):
    """
    For Portugol Studio source code.
    """
    name = 'Portugol Studio'
    aliases = ['portugolstudio', 'portugol']
    filenames = ['*.por']  # just to have one if you whant to use

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    # The trailing ?, rather than *, avoids a geometric performance drop here.
    #: only one /* */ style comment
    _ws1 = r'\s*(?:/[*].*?[*]/\s*)?'

    tokens = {
        'whitespace': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'//(\n|[\w\W]*?[^\\]\n)', Comment.Single),
            (r'/(\\\n)?[*][\w\W]*?[*](\\\n)?/', Comment.Multiline),
            # Open until EOF, so no ending delimeter
            (r'/(\\\n)?[*][\w\W]*', Comment.Multiline),
        ],
        'statements': [
            (r'(")', bygroups(String), 'string'),
            (r"(')(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])(')",
             bygroups(String.Char, String.Char, String.Char)),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            (r'\*/', Error),
            (r'(?:!)', Error),
            (r'[~%&*+=|?<>/-]', Operator),
            (r'[()\[\],:.]', Punctuation),
            (words(('pare', 'caso', 'const', 'continue',
                    'faca', 'senao', 'para',
                    'se', 'retorne',
                    'escolha', 'enquanto'),
                   suffix=r'\b'), Keyword),
            (r'(logico|inteiro|real|caracter|vazio|cadeia)\b',
             Keyword.Type),
            (words(('inclua', 'biblioteca', 'funcao', 'programa'),
                   suffix=r'\b'), Keyword.Reserved),
            (r'(verdadeiro|falso|ou|e|nao)\b', Name.Builtin),
            (r'([a-zA-Z_]\w*)(\s*)(:)(?!:)',
             bygroups(Name.Label, Text, Punctuation)),  # switch-case statements
            (r'[a-zA-Z_]\w*', Name),
        ],
        'root': [
            include('whitespace'),
            # function declarations
            (r'(funcao)'                   # reserved keyword funcao
             r'((?:[\w*\s])+?(?:\s|[*]))'  # return arguments
             r'([a-zA-Z_]\w*)'             # method name
             r'(\s*\([^;]*?\))'            # signature
             , bygroups(Keyword.Reserved, using(this), Name.Function, using(this), using(this))),
            default('statement'),
        ],
        'statement': [
            include('whitespace'),
            include('statements'),
            ('[{}]', Punctuation),
            (';', Error),
        ],
        'funcao': [
            include('whitespace'),
            include('statements'),
            (';', Error),
            (r'\{', Punctuation, '#push'),
            (r'\}', Punctuation, '#pop'),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|'
             r'u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\', String),  # stray backslash
        ],
    }

    def __init__(self, **options):
        RegexLexer.__init__(self, **options)
