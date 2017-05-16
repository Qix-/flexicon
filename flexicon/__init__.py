import regex

import sys
if sys.version_info[0] < 3:
    _unicode = unicode

    def _repr(x):
        if type(x) is unicode:
            return repr(x)[1:]
else:
    _unicode = str
    _repr = repr


class FlexiconError(Exception):
    pass


def _find_line_ranges(source):
    ranges = []

    last = 0
    count = 0
    for c in source:
        if c == '\n':
            ranges.append((last, count))
            last = count
        count += 1

    ranges.append((last, count))

    return ranges


def _get_line_for_index(i, ranges):
    count = 1
    for r in ranges:
        left, right = r
        if i >= left and i <= right:
            return (count, (i - left) + 1)
        count += 1
    raise FlexiconError('character is not within range: ' + str(i))


def _compile(r):
    return regex.compile(r, flags=regex.VERSION1)


class Lexer(object):
    def __init__(self, postprocessor=None):
        self.postprocessor = postprocessor
        self.rules = []

        self.__reset()

    def __reset(self):
        self.col = 0
        self.row = 0
        self.name = None
        self.text = None

    def lex(self, source, name=None):
        self.__reset()

        assert type(source) is _unicode

        ranges = _find_line_ranges(source)

        try:
            self.name = name

            tokens = []

            length = len(source)
            position = 0

            while position < length:
                for rule in self.rules:
                    match = rule[0].match(source[position:])

                    if match:
                        self.text = match[0]
                        _, end = match.span()

                        result = rule[1](*match[1:])
                        if self.postprocessor:
                            result = self.postprocessor(result, self)

                        self.row, self.col = _get_line_for_index(end, ranges)

                        if result is not None:
                            tokens.append(result)

                        position = position + end

                        break

                else:
                    # no tokens matched
                    if self.name:
                        name = self.name + ':'
                    else:
                        name = ''
                    raise FlexiconError('unexpected character {}\n\tat {}{}:{}'.format(_repr(source[position]), name, self.row, self.col))

            return tokens

        finally:
            self.__reset()

    @property
    def position(self):
        return (self.name, self.row, self.col)

    @property
    def rule(self):
        def decorator(pattern):
            regexp = _compile(pattern)

            def rule_inner(fn):
                self.rules.append([regexp, fn])
                return fn

            return rule_inner
        return decorator

    def simple(self, *ruleset):
        for r in ruleset:
            assert type(r) is tuple and len(r) == 2

            k, v = r

            if type(k) is not str:
                raise FlexiconError('rule pattern is not a string: {}'.format(repr(k)))
            if not callable(v):
                raise FlexiconError('rule handler is not callable: {}'.format(repr(v)))

            self.rules.append([_compile(k), v])

        return self
