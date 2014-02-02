from itertools import product, starmap

from lispy.reglang import (Empty, Single, Union, Con, KleeneStar,
                           union_char, char_range, string, plus)


class TestEmpty:
    def setup(self):
        self.fa = Empty()

    def test_accept(self):
        assert self.fa.start_state.is_final

    def test_reject(self):
        next_state = self.fa.next(self.fa.start_state, 'x')
        assert next_state is None


class TestSingle:
    def setup(self):
        self.char = 'x'
        self.fa = Single(self.char)

    def test_accept(self):
        next_state = self.fa.next(self.fa.start_state, self.char)
        assert next_state.is_final

    def test_reject(self):
        next_state = self.fa.next(self.fa.start_state, 'y')
        assert next_state is None

    def test_two_char(self):
        s1 = self.fa.next(self.fa.start_state, self.char)
        assert s1 is not None
        s2 = self.fa.next(s1, self.char)
        assert s2 is None


class TestUnion:
    def setup(self):
        self.char1 = 'x'
        self.char2 = 'y'
        fa1 = Single(self.char1)
        fa2 = Single(self.char2)
        self.fa = Union(fa1, fa2)

    def test_accept_char1(self):
        next_state = self.fa.next(self.fa.start_state, self.char1)
        assert next_state.is_final

    def test_accept_char2(self):
        next_state = self.fa.next(self.fa.start_state, self.char2)
        assert next_state.is_final

    def test_reject(self):
        next_state = self.fa.next(self.fa.start_state, 'z')
        assert next_state is None


class TestConSingle:
    def setup(self):
        self.char1 = 'x'
        self.char2 = 'y'
        fa1 = Single(self.char1)
        fa2 = Single(self.char2)
        self.fa = Con(fa1, fa2)

    def test_accept(self):
        s1 = self.fa.next(self.fa.start_state, self.char1)
        assert not s1.is_final

        s2 = self.fa.next(s1, self.char2)
        assert s2.is_final

    def test_reject_char1(self):
        next_state = self.fa.next(self.fa.start_state, self.char1)
        assert not next_state.is_final

    def test_reject_char2(self):
        next_state = self.fa.next(self.fa.start_state, self.char2)
        assert next_state is None


class TestConUnionSingle:
    def setup(self):
        self.union_char_1 = 'xy'
        self.union_char_2 = 'ab'

        union_chars = [self.union_char_1, self.union_char_2]
        singles = (map(Single, chars) for chars in union_chars)
        unions = starmap(Union, singles)
        self.fa = Con(*unions)

    def test_accept(self):
        start_state = self.fa.start_state
        for char1, char2 in product(self.union_char_1, self.union_char_2):
            s1 = self.fa.next(start_state, char1)
            assert not s1.is_final

            s2 = self.fa.next(s1, char2)
            assert s2.is_final

    def test_reject_1(self):
        start_state = self.fa.start_state
        for char1, char2 in [self.union_char_1, self.union_char_1]:
            s1 = self.fa.next(start_state, char1)
            assert not s1.is_final

            s2 = self.fa.next(s1, char2)
            assert s2 is None

    def test_reject_2(self):
        start_state = self.fa.start_state
        for char in self.union_char_2:
            s = self.fa.next(start_state, char)
            assert s is None


class TestKleeneStar:
    def setup(self):
        self.string = 'abc'
        self.fa = KleeneStar(Con(*map(Single, self.string)))

    def test_accept_empty(self):
        self.verify('')

    def test_accept_repeat_1(self):
        self.verify(self.string)

    def test_accept_repeat_2(self):
        self.verify(self.string * 2)

    def test_accept_repeat_3(self):
        self.verify(self.string * 3)

    def verify(self, string):
        state = self.fa.start_state
        for char in string:
            assert state is not None
            state = self.fa.next(state, char)
        else:
            assert state.is_final

    def test_reject_half(self):
        index = len(self.string) // 2
        half_string = self.string[:index]
        state = self.fa.start_state
        for char in half_string:
            state = self.fa.next(state, char)
            assert not state.is_final


class TestUnionChar:
    def setup(self):
        self.union_char = 'abcde'
        self.fa = union_char(self.union_char)

    def test_accept(self):
        for char in self.union_char:
            next_state = self.fa.next(self.fa.start_state, char)
            assert next_state.is_final

            next_state = self.fa.next(next_state, char)
            assert next_state is None

    def test_reject(self):
        for char in 'xyz':
            next_state = self.fa.next(self.fa.start_state, char)
            assert next_state is None


class TestCharRange:
    def setup(self):
        self.char_range = 'abcdefghijklmnopqrstuvwxyz'
        self.fa = char_range('a', 'z')

    def test_accept(self):
        for char in self.char_range:
            next_state = self.fa.next(self.fa.start_state, char)
            assert next_state.is_final

            next_state = self.fa.next(next_state, char)
            assert next_state is None

    def test_reject(self):
        for char in 'ABC':
            next_state = self.fa.next(self.fa.start_state, char)
            assert next_state is None


class TestString:
    def setup(self):
        self.string = 'abcde'
        self.fa = string(self.string)

    def test_accept(self):
        state = self.fa.start_state
        for char in self.string:
            assert not state.is_final
            state = self.fa.next(state, char)
        else:
            assert state.is_final

    def test_reject(self):
        state = self.fa.start_state
        for char in self.string:
            assert not state.is_final
            state = self.fa.next(state, char)
        else:
            assert state.is_final

        state = self.fa.next(state, 'x')
        assert state is None


class TestPlus:
    def setup(self):
        self.string = 'abc'
        self.fa = plus(Con(*map(Single, self.string)))

    def test_accept_repeat_1(self):
        self.verify(self.string)

    def test_accept_repeat_2(self):
        self.verify(self.string * 2)

    def test_accept_repeat_3(self):
        self.verify(self.string * 3)

    def verify(self, string):
        state = self.fa.start_state
        for char in string:
            assert state is not None
            state = self.fa.next(state, char)
        else:
            assert state.is_final

    def test_reject_empty(self):
        assert not self.fa.start_state.is_final

    def test_reject_half(self):
        index = len(self.string) // 2
        half_string = self.string[:index]
        state = self.fa.start_state
        for char in half_string:
            state = self.fa.next(state, char)
            assert not state.is_final
