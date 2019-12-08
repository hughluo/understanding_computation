class Tape:
    """Purely functional non-destructive tape"""
    def __init__(self, left, middle, right, blank):
        self.left = left
        self.middle = middle
        self.right = right
        self.blank = blank
    
    def __str__(self):
        left = ''.join(self.left)
        right = ''.join(self.right)
        return f'<Tape {left}({self.middle}){right}>'
    
    def write(self, character):
        return Tape(self.left, character, self.right, self.blank)
    
    def move_head_left(self):
        left = self.left[:-1] if len(self.left) > 1 else []
        middle = self.left[-1] if len(self.left) > 0 else self.blank
        right = [self.middle] + self.right
        return Tape(left, middle, right, self.blank)
    
    def move_head_right(self):
        left = self.left + [self.middle]
        middle = self.right[0] if len(self.right) > 0 else self.blank
        right = self.right[1:] if len(self.right) > 1 else []
        return Tape(left, middle, right, self.blank)
    

class TMConfiguration:
    def __init__(self, state, tape):
        self.state = state
        self.tape = tape
    
    def __str__(self):
        return f'<TMConfiguration state={self.state}, tape={str(self.tape)}>'


class TMRule:
    def __init__(self, state, character, next_state, write_character, direction):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.write_character = write_character
        self.direction = direction
    
    def is_applies_to(self, configuration):
        return self.state == configuration.state and self.character == configuration.tape.middle
    
    def follow(self, configuration):
        return TMConfiguration(self.next_state, self.next_tape(configuration))
    
    def next_tape(self, configuration):
        written_tape = configuration.tape.write(self.write_character)
        if self.direction == 'left':
            return written_tape.move_head_left()
        elif self.direction == 'right':
            return written_tape.move_head_right()
        else:
            raise AttributeError(f'expected string \'left\' or \'right\' as direction, {self.direction} countered')


class DTMRulebook:
    def __init__(self, rules):
        self.rules = rules
    
    def next_configuration(self, configuration):
        return self.rule_for(configuration).follow(configuration)
    
    def rule_for(self, configuration):
        for rule in self.rules:
            if rule.is_applies_to(configuration):
                return rule
    
    def is_applies_to(self, configuration):
        return self.rule_for(configuration) is not None


class DTM:
    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook
    
    def is_accepting(self):
        return self.current_configuration.state in self.accept_states
    
    def step(self):
        self.current_configuration = self.rulebook.next_configuration(self.current_configuration)
    
    def run(self):
        while not self.is_accepting() and not self.is_stuck():
            self.step()
        
    def is_stuck(self):
        return not self.is_accepting() and not self.rulebook.is_applies_to(self.current_configuration)

if __name__ == "__main__":

    tape = Tape(['1', '0', '1'], '1', [], '_')
    assert str(tape) == '<Tape 101(1)>'
    assert str(tape.move_head_left()) == '<Tape 10(1)1>'
    assert str(tape.write('0')) == '<Tape 101(0)>'
    assert str(tape.move_head_right()) == '<Tape 1011(_)>'
    assert str(tape.move_head_right().write('0')) == '<Tape 1011(0)>'

    rule = TMRule(1, '0', 2, '1', 'right')
    assert rule.is_applies_to(TMConfiguration(1, Tape([], '0', [], '_')))
    assert not rule.is_applies_to(TMConfiguration(1, Tape([], '1', [], '_')))
    assert not rule.is_applies_to(TMConfiguration(2, Tape([], '0', [], '_')))

    assert str(rule.follow(TMConfiguration(1, Tape([], '0', [], '_')))) == '<TMConfiguration state=2, tape=<Tape 1(_)>>'

    rulebook = DTMRulebook([
        TMRule(1, '0', 2, '1', 'right'),
        TMRule(1, '1', 1, '0', 'left'),
        TMRule(1, '_', 2, '1', 'right'),
        TMRule(2, '0', 2, '0', 'right'),
        TMRule(2, '1', 2, '1', 'right'),
        TMRule(2, '_', 3, '_', 'left'),
    ])
    configuration = TMConfiguration(1, tape)
    assert str(configuration) == '<TMConfiguration state=1, tape=<Tape 101(1)>>'
    configuration = rulebook.next_configuration(configuration)
    assert str(configuration) == '<TMConfiguration state=1, tape=<Tape 10(1)0>>'
    configuration = rulebook.next_configuration(configuration)
    assert str(configuration) == '<TMConfiguration state=1, tape=<Tape 1(0)00>>'
    configuration = rulebook.next_configuration(configuration)
    assert str(configuration) == '<TMConfiguration state=2, tape=<Tape 11(0)0>>'

    dtm = DTM(TMConfiguration(1, tape), [3], rulebook)
    assert str(dtm.current_configuration) == '<TMConfiguration state=1, tape=<Tape 101(1)>>'
    assert not dtm.is_accepting()
    dtm.step()
    assert str(dtm.current_configuration) == '<TMConfiguration state=1, tape=<Tape 10(1)0>>'
    assert not dtm.is_accepting()
    dtm.run()
    assert str(dtm.current_configuration) == '<TMConfiguration state=3, tape=<Tape 110(0)_>>'
    assert dtm.is_accepting()

    tape = Tape(['1', '2', '1'], '1', [], '_')
    dtm = DTM(TMConfiguration(1, tape), [3], rulebook)
    dtm.run()
    assert not dtm.is_accepting()
    assert dtm.is_stuck()
    assert str(dtm.current_configuration) == '<TMConfiguration state=1, tape=<Tape 1(2)00>>'

    # A Turing machine for recognizing strings like 'aaabbbccc', 'aabbcc'
    test_rulebook = DTMRulebook([
        # state 1: scan right looking for a
        TMRule(1, 'X', 1, 'X', 'right'), # skip X
        TMRule(1, 'a', 2, 'X', 'right'), # cross out a, go to state 2
        TMRule(1, '_', 6, '_', 'left'),  # find blank, go to state 6 (accept)

        # state 2: scan right looking for b
        TMRule(2, 'a', 2, 'a', 'right'), # skip a
        TMRule(2, 'X', 2, 'X', 'right'), # skip X
        TMRule(2, 'b', 3, 'X', 'right'), # cross out b, go to state 3

        # state 3: scan right looking for c
        TMRule(3, 'b', 3, 'b', 'right'), # skip b
        TMRule(3, 'X', 3, 'X', 'right'), # skip X
        TMRule(3, 'c', 4, 'X', 'right'),  # cross out c, go to state 4
        
        # state 4: scan right looking for end of string
        TMRule(4, 'c', 4, 'c', 'right'), # skip c
        TMRule(4, '_', 5, '_', 'left'),  # find blank, go to state 5

        # state 5: scan left looking for beginning of string
        TMRule(5, 'a', 5, 'a', 'left'),  # skip a
        TMRule(5, 'b', 5, 'b', 'left'),  # skip b
        TMRule(5, 'c', 5, 'c', 'left'),  # skip c
        TMRule(5, 'X', 5, 'X', 'left'),  # skip X
        TMRule(5, '_', 1, '_', 'right'), # find blank, go to state 1
    ])

    test_tape = Tape([], 'a', ['a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'], '_')
    assert str(test_tape) == '<Tape (a)aabbbccc>'
    dtm = DTM(TMConfiguration(1, test_tape), [6], test_rulebook)
    for i in range(10):
        dtm.step()
    assert str(dtm.current_configuration) == '<TMConfiguration state=5, tape=<Tape XaaXbbXc(c)_>>'
    
    for i in range(25):
        dtm.step()
    assert str(dtm.current_configuration) == '<TMConfiguration state=5, tape=<Tape _XXa(X)XbXXc_>>'
    
    dtm.run()
    assert dtm.is_accepting()
    assert str(dtm.current_configuration) == '<TMConfiguration state=6, tape=<Tape _XXXXXXXX(X)_>>'


    test_tape = Tape([], 'a', ['a', 'b', 'b', 'c', 'c'], '_')
    dtm = DTM(TMConfiguration(1, test_tape), [6], test_rulebook)
    dtm.run()
    assert dtm.is_accepting()