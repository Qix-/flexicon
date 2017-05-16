# Flexicon

Flexicon is a simple [regex](https://pypi.python.org/pypi/regex/)-based lexer and tokenizer.

## Installation

```console
$ pip install flexicon
```

## Usage

```python
from flexicon import Lexer

# Simple Expression Lexer
EXPRESSION_LEXER = Lexer().simple(
    (r'[ \t]+', lambda: None),
    (r'\+', lambda: ('ADD',)),
    (r'\/', lambda: ('DIVIDE',)),
    (r'\-', lambda: ('SUBTRACT',)),
    (r'\*', lambda: ('MULTIPLY',)),
    (r'\(', lambda: ('OPAREN',)),
    (r'\)', lambda: ('CPAREN',)),
    (r'([0-9]+)', lambda n: ('NUMBER', int(n))),
    (r'([a-zA-Z])', lambda c: ('VARIABLE', c))
)

print(EXPRESSION_LEXER.lex(u'1 + 2a(4 / b)'))

# Outputs:
# [
#      ('NUMBER', 1),
#      ('ADD',),
#      ('NUMBER', 2),
#      ('VARIABLE', 'a'),
#      ('OPAREN',),
#      ('NUMBER', 4),
#      ('DIVIDE',),
#      ('VARIABLE', 'b'),
#      ('CPAREN',)
# ]
```

# License
Copyright &copy; 2017, Josh Junon. Released under the [MIT License](LICENSE).
