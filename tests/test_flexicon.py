import unittest

from flexicon import Lexer, FlexiconError


# Simple Expression Lexer
rules = (
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


class TestFlexicon(unittest.TestCase):
    def test_simple_token(self):
        lexer = Lexer().simple(*rules)

        self.assertEqual(lexer.lex(u'1'), [('NUMBER', 1)])
        self.assertEqual(lexer.lex(u'12345'), [('NUMBER', 12345)])
        self.assertEqual(lexer.lex(u'a'), [('VARIABLE', 'a')])
        self.assertEqual(lexer.lex(u'+'), [('ADD',)])
        self.assertEqual(lexer.lex(u'-'), [('SUBTRACT',)])

    def test_mutiple_tokens(self):
        lexer = Lexer().simple(*rules)

        self.assertEqual(lexer.lex(u'1 + 2a(4 / b)'), [
            ('NUMBER', 1),
            ('ADD',),
            ('NUMBER', 2),
            ('VARIABLE', 'a'),
            ('OPAREN',),
            ('NUMBER', 4),
            ('DIVIDE',),
            ('VARIABLE', 'b'),
            ('CPAREN',)])

    def test_errors(self):
        lexer = Lexer().simple(*rules)

        try:
            lexer.lex(u'1234&1234')
            self.fail('didn\'t catch erroneous \'&\'')
        except FlexiconError as e:
            self.assertEqual(str(e), 'unexpected character \'&\'\n\tat 1:5')

        try:
            lexer.lex(u'1234&1234', 'testinput')
            self.fail('didn\'t catch erroneous \'&\'')
        except FlexiconError as e:
            self.assertEqual(str(e), 'unexpected character \'&\'\n\tat testinput:1:5')

        try:
            lexer.simple((1, lambda: None))
            self.fail('didn\'t catch non-string pattern')
        except FlexiconError as e:
            self.assertEqual(str(e), 'rule pattern is not a string: 1')

        try:
            lexer.simple((r'foo', False))
            self.fail('didn\'t catch non-callable handler')
        except FlexiconError as e:
            self.assertEqual(str(e), 'rule handler is not callable: False')
