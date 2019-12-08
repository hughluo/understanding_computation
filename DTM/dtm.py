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