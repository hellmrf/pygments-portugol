# -*- coding: utf-8 -*-
"""
    Portugol Studio lexer
    ~~~~~~~~~~~

    Pygments lexer for Portugol Studio, a algorithmic language for beginners in Portuguese.

    :copyright: Copyright 2021 Héliton Martins
    :license: GPL v2.0, see LICENSE for details.
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
            # preprocessor directives: without whitespace
            # (r'^#if\s+0', Comment.Preproc, 'if0'),
            # ('^#', Comment.Preproc, 'macro'),
            # # or with whitespace
            # ('^(' + _ws1 + r')(#if\s+0)',
            #  bygroups(using(this), Comment.Preproc), 'if0'),
            # ('^(' + _ws1 + ')(#)',
            #  bygroups(using(this), Comment.Preproc), 'macro'),
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'//(\n|[\w\W]*?[^\\]\n)', Comment.Single),
            (r'/(\\\n)?[*][\w\W]*?[*](\\\n)?/', Comment.Multiline),
            # Open until EOF, so no ending delimeter
            (r'/(\\\n)?[*][\w\W]*', Comment.Multiline),
        ],
        'statements': [
            (r'(L?)(")', bygroups(String.Affix, String), 'string'),
            (r"(L?)(')(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])(')",
             bygroups(String.Affix, String.Char, String.Char, String.Char)),
            (r'(\d+\.\d*|\.\d+|\d+)[eE][+-]?\d+[LlUu]*', Number.Float),
            (r'(\d+\.\d*|\.\d+|\d+[fF])[fF]?', Number.Float),
            (r'0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
            (r'0[0-7]+[LlUu]*', Number.Oct),
            (r'\d+[LlUu]*', Number.Integer),
            (r'\*/', Error),
            (r'[~!%^&*+=|?:<>/-]', Operator),
            (r'[()\[\],.]', Punctuation),
            (words(('pare', 'caso', 'const', 'continue',
                    'faca', 'senao', 'para',
                    'se', 'retorne',
                    'escolha', 'enquanto'),
                   suffix=r'\b'), Keyword),
            (r'(logico|inteiro|real|caracter|vazio|cadeia)\b',
             Keyword.Type),
            (words(('inclua', 'biblioteca', 'funcao', 'programa'),
                   suffix=r'\b'), Keyword.Reserved),
            # Vector intrinsics
            # (r'(__m(128i|128d|128|64))\b', Keyword.Reserved),
            # Microsoft-isms
            # (words((
            #     'asm', 'int8', 'based', 'except', 'int16', 'stdcall', 'cdecl',
            #     'fastcall', 'int32', 'declspec', 'finally', 'int64', 'try',
            #     'leave', 'wchar_t', 'w64', 'unaligned', 'raise', 'noop',
            #     'identifier', 'forceinline', 'assume'),
            #     prefix=r'__', suffix=r'\b'), Keyword.Reserved),
            (r'(verdadeiro|falso|ou|e|nao)\b', Name.Builtin),
            (r'([a-zA-Z_]\w*)(\s*)(:)(?!:)',
             bygroups(Name.Label, Text, Punctuation)),
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
            (';', Punctuation, '#pop'),
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
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'macro': [
            (r'(inclua|biblioteca)(' + _ws1 + r')([^\n]+)',
             bygroups(Comment.Preproc, Text, Comment.PreprocFile)),
            (r'[^/\n]+', Comment.Preproc),
            (r'/[*](.|\n)*?[*]/', Comment.Multiline),
            (r'//.*?\n', Comment.Single, '#pop'),
            (r'/', Comment.Preproc),
            (r'(?<=\\)\n', Comment.Preproc),
            (r'\n', Comment.Preproc, '#pop'),
        ],
    }

    stdlib_types = set((
        'size_t', 'ssize_t', 'off_t', 'wchar_t', 'ptrdiff_t', 'sig_atomic_t', 'fpos_t',
        'clock_t', 'time_t', 'va_list', 'jmp_buf', 'FILE', 'DIR', 'div_t', 'ldiv_t',
        'mbstate_t', 'wctrans_t', 'wint_t', 'wctype_t'))

    def __init__(self, **options):
        self.stdlibhighlighting = get_bool_opt(
            options, 'stdlibhighlighting', True)
        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        for index, token, value in \
                RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if self.stdlibhighlighting and value in self.stdlib_types:
                    token = Keyword.Type
            yield index, token, value
