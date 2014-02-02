from itertools import chain, starmap


__all__ = ['Empty', 'Single', 'Union', 'Con', 'KleeneStar',
           'union_char', 'char_range', 'string', 'plus']


class State:
    def __init__(self, is_final=False):
        self.is_final = is_final


class Empty:
    start_state = State(True)

    def next(self, state, char):
        return None


class Single:
    start_state = State()
    final_state = State(True)

    def __init__(self, char):
        self.char = char

    def next(self, state, char):
        if state == self.start_state and self.char == char:
            return self.final_state
        else:
            return None


class UnionState(State):
    def __init__(self, states):
        is_final = any(map(lambda s: s is not None and s.is_final, states))
        super().__init__(is_final)
        self.states = states

    def __eq__(self, other):
        return self.states == other.states

    def __ne__(self, other):
        return self.states != other.states

    def __hash__(self):
        return hash(self.states)


class Union:
    def __init__(self, *fas):
        if len(fas) < 2:
            raise ValueError('At least union 2 finite automata')

        self.fas = fas
        self.start_state = UnionState(tuple(fa.start_state for fa in fas))

    def next(self, state, char):
        if state is None:
            return None

        states = tuple(fa.next(sub_state, char)
                       for fa, sub_state in zip(self.fas, state.states))
        if all(map(lambda s: s is None, states)):
            return None

        return UnionState(states)


class ConState(State):
    def __init__(self, fa_states, is_final=False):
        super().__init__(is_final)
        self.fa_states = fa_states

    def __eq__(self, other):
        return self.fa_states == other.fa_states

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.fa_states)


class Con:
    def __init__(self, *fas):
        if len(fas) < 2:
            raise ValueError('At least concatenate 2 finite automata')

        self.fas = fas
        self.start_state = ConState(((0, fas[0].start_state),))

    def next(self, state, char):
        if state is None:
            return None

        fa_count = len(self.fas)
        last_fa = fa_count - 1

        def next_generator():
            for fa_index, sub_state in state.fa_states:
                if fa_index < fa_count:
                    fa = self.fas[fa_index]
                    next_state = fa.next(sub_state, char)
                    if next_state is not None:
                        yield (fa_index, next_state)

                        if next_state.is_final and fa_index < last_fa:
                            next_fa_index = fa_index + 1
                            next_fa = self.fas[next_fa_index]
                            yield (next_fa_index, next_fa.start_state)

        next_fa_states = frozenset(next_generator())
        if next_fa_states:
            is_finals = starmap(lambda fa, s: fa == last_fa and s.is_final,
                                next_fa_states)
            is_final = any(is_finals)
            return ConState(next_fa_states, is_final)
        else:
            return None


class KleeneStarState(State):
    def __init__(self, states, is_final=True):
        super().__init__(is_final)
        self.states = states

    def __eq__(self, other):
        return self.states == other.states

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.states)


class KleeneStar:
    def __init__(self, fa):
        self.fa = fa
        self.start_state = KleeneStarState(frozenset([self.fa.start_state]),
                                           is_final=True)

    def next(self, state, char):
        next_states = map(lambda s: self.fa.next(s, char), state.states)
        filtered = list(filter(None, next_states))
        if filtered:
            is_final = any(map(lambda s: s.is_final, filtered))
            states = (chain(filtered, [self.fa.start_state]) if is_final
                      else filtered)
            next_state = KleeneStarState(frozenset(states),
                                         is_final=is_final)
            return next_state
        else:
            return None


def union_char(chars):
    return Union(*map(Single, chars))


def char_range(start, end):
    return union_char(map(chr, range(ord(start), ord(end) + 1)))


def string(strings):
    return Con(*map(Single, strings))


def plus(fa):
    return Con(fa, KleeneStar(fa))
