# Created for aenea using libraries from the Dictation Toolbox
# https://github.com/dictation-toolbox/dragonfly-scripts
#
# Commands for writing in the Python and Go programming languages
#
# Author: Tony Grosinger
#
# Licensed under LGPL

import aenea
import aenea.configuration
from aenea.lax import Key, Function
from aenea import (
    IntegerRef,
    Text,
    Dictation,
    Choice
)
from _generic_edit import pressKeyMap
from format import format_snake_case, format_pascal_case, format_camel_case
import dragonfly

vim_context = aenea.ProxyPlatformContext('linux')
grammar = dragonfly.Grammar('python', context=vim_context)

mode = "gopher"
mode_map = {
    "gopher": "gopher",
    "python": "python"
}


def switch_mode(language):
    global mode
    mode = language


def create_class(text):
    if mode == "python":
        newText = 'class %s():\n    ' % format_pascal_case(text)
        Text("%(text)s").execute({"text": newText})


def create_private_function(text):
    if mode == "python":
        newText = 'def _%s(' % format_snake_case(text)
        Text("%(text)s").execute({"text": newText})
    elif mode == "gopher":
        newText = 'func %s(' % format_camel_case(text)
        Text("%(text)s").execute({"text": newText})


def create_class_function(text, text2):
    if mode == "gopher":
        newText = 'func (x *%s) %s(' % (format_pascal_case(text),
                                        format_pascal_case(text2))
        Text("%(text)s").execute({"text": newText})


def create_public_function(text):
    if mode == "python":
        newText = 'def %s(' % format_snake_case(text)
        Text("%(text)s").execute({"text": newText})
    elif mode == "gopher":
        newText = 'func %s(' % format_pascal_case(text)
        Text("%(text)s").execute({"text": newText})


def close_function():
    if mode == "python":
        Text("):\n").execute()
    elif mode == "gopher":
        Text(") {\n\n").execute()
        Key("up, tab").execute()


def print_line():
    if mode == "python":
        newText = "print()"
        Text("%(text)s").execute({"text": newText})
        Key("left").execute()
    if mode == "gopher":
        newText = "fmt.Println()"
        Text("%(text)s").execute({"text": newText})
        Key("left").execute()


def comment():
    Key("escape, i").execute()
    if mode == "python":
        Text("# ").execute()
    if mode == "gopher":
        Text("// ").execute()


def null():
    if mode == "python":
        Text("None").execute()
    if mode == "gopher":
        Text("nil").execute()


basics_mapping = aenea.configuration.make_grammar_commands('python', {
    'new class [named] <text>': Function(create_class),
    'new [public] (function|func) [named] <text>': Function(create_public_function),
    'new private (function|func) [named] <text>': Function(create_private_function),
    'new class function <text> [named] <text2>': Function(create_class_function),
    'close (function|func)': Function(close_function),
    'print line': Function(print_line),
    'null': Function(null),
    'comment': Function(comment),
    'mode <language>': Function(switch_mode),
    })


operators_mapping = {
    'defined':          Text(':= '),
    'assign':           Text('= '),
    'compare equal':    Text('== '),
    'compare not equal': Text('!= '),
    'compare greater':  Text('> '),
    'compare less':     Text('< '),
    'compare geck':     Text('>= '),
    'compare lack':     Text('<= '),
    'bit ore':          Text('| '),
    'bit and':          Text('& '),
    'bit ex or':        Text('^ '),
    'times':            Text('* '),
    'divided':          Text('/ '),
    'plus':             Text('+ '),
    'minus':            Text('- '),
    'plus equal':       Text('+= '),
    'minus equal':      Text('-= '),
    'times equal':      Text('*= '),
    'divided equal':    Text('/= '),
    'mod equal':        Text('%%= '),
    'pointer to':       Text('*'),
}

data_types_mapping = {
    'string': Text('string'),
    'int': Text('int'),
    'int 64': Text('int64'),
    'enum': Text('enum'),
    'int 32': Text('int32'),
    '(boolean|bool)': Text('bool'),
    'struct': Text('struct'),
}


class Basics(dragonfly.MappingRule):
    mapping = basics_mapping
    extras = [
        Dictation('text'),
        Dictation('text2'),
        IntegerRef('n', 1, 999),
        IntegerRef('n2', 1, 999),
        Choice("pressKey", pressKeyMap),
        Choice("language", mode_map)
    ]


class Operators(dragonfly.MappingRule):
    mapping = operators_mapping

class DataTypes(dragonfly.MappingRule):
    mapping = data_types_mapping

grammar.add_rule(Basics())
grammar.add_rule(Operators())
grammar.add_rule(DataTypes())
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None