from stack import Stack

class PDAConfiguration:
    STUCK_STATE = float('-inf')
    def __init__(self, state, stack):
        self.state = state
        self.stack = stack
    
    def __eq__(self, other):
        return self.state == other.state and self.stack == other.stack
    
    def __hash__(self):
        return hash(hash(self.state) + hash(self.stack))
    
    def __str__(self):
        return f'<PDAConfiguration state={self.state}, stack={str(self.stack)}>'
    
    def stuck(self):
        return PDAConfiguration(PDAConfiguration.STUCK_STATE, self.stack)
    
    def is_stuck(self):
        return self.state == PDAConfiguration.STUCK_STATE


class PDARule:
    def __init__(self, state, character, next_state, pop_character, push_character):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.pop_character = pop_character
        self.push_character = push_character

    def is_applies_to(self, configuration, character):
        return self.state == configuration.state and self.pop_character == configuration.stack.top() and \
            self.character == character
    
    def follow(self, configuration):
        return PDAConfiguration(self.next_state, self.next_stack(configuration))
    
    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop()
        return Stack(self.push_character + popped_stack.stk)


class DPDARulebook:
    def __init__(self, rules):
        self.rules = rules
    
    def next_configuration(self, configuration, character):
        return self.rule_for(configuration, character).follow(configuration)
    
    def rule_for(self, configuration, character):
        for rule in self.rules:
            if rule.is_applies_to(configuration, character):
                return rule
    
    def is_applies_to(self, configuration, character):
        return self.rule_for(configuration, character) is not None
    
    def follow_free_moves(self, configuration):
        if self.is_applies_to(configuration, None):
            return self.follow_free_moves(self.next_configuration(configuration, None))
        else:
            return configuration


class DPDA:
    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook

    def current_configuration_(self):
        self.current_configuration = rulebook.follow_free_moves(self.current_configuration)
        return self.current_configuration

    def is_accepting(self):
        self.current_configuration_()
        return self.current_configuration.state in self.accept_states

    def read_character(self, character):
        self.current_configuration = self.next_configuration(character)
    
    def read_string(self, string):
        for char in string:
            if not self.is_stuck():
                self.read_character(char) 
        
    def next_configuration(self, character):
        if self.rulebook.is_applies_to(self.current_configuration_(), character):
            return self.rulebook.next_configuration(self.current_configuration_(), character)
        else:
            return self.current_configuration.stuck()
    
    def is_stuck(self):
        return self.current_configuration.is_stuck()


class DPDADesign:
    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self.start_state = start_state
        self.bottom_character = bottom_character
        self.accept_states = accept_states
        self.rulebook = rulebook
    
    def is_accepts(self, string):
        dpda = self.to_dpda()
        dpda.read_string(string)
        return dpda.is_accepting()
    
    def to_dpda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return DPDA(start_configuration, self.accept_states, self.rulebook)


if __name__ == "__main__":
    print('-' * 20)
    rule = PDARule(1, '(', 2, '$', ['b', '$'])
    configuration = PDAConfiguration(1, Stack(['$']))
    print(rule.is_applies_to(configuration, '('))  # True
    print(rule.follow(configuration))
    
    print('-' * 20)
    rulebook = DPDARulebook([
        PDARule(1, '(', 2, '$', ['b', '$']),
        PDARule(2, '(', 2, 'b', ['b', 'b']),
        PDARule(2, ')', 2, 'b', []),
        PDARule(2, None, 1, '$', ['$']),
    ])
    configuration = rulebook.next_configuration(configuration, '(')
    print(configuration)
    assert str(configuration) == "<PDAConfiguration state=2, stack=<Stack (b)$>>"
    configuration = rulebook.next_configuration(configuration, '(')
    print(configuration)
    assert str(configuration) == "<PDAConfiguration state=2, stack=<Stack (b)b$>>"
    configuration = rulebook.next_configuration(configuration, ')')
    print(configuration)
    assert str(configuration) == "<PDAConfiguration state=2, stack=<Stack (b)$>>"

    print('-' * 20)
    dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
    print(dpda.is_accepting())
    assert dpda.is_accepting()
    dpda.read_string('(()')
    print(dpda.is_accepting())
    assert not dpda.is_accepting()
    print(dpda.current_configuration)
    assert str(dpda.current_configuration) == "<PDAConfiguration state=2, stack=<Stack (b)$>>"

    print('-' * 20)
    configuration = PDAConfiguration(2, Stack(['$']))
    print(rulebook.follow_free_moves(configuration))
    assert str(rulebook.follow_free_moves(configuration)) == "<PDAConfiguration state=1, stack=<Stack ($)>>"

    print('-' * 20)
    dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
    dpda.read_string('(()(')
    print(dpda.is_accepting())
    assert not dpda.is_accepting()
    print(dpda.current_configuration)
    assert str(dpda.current_configuration) == "<PDAConfiguration state=2, stack=<Stack (b)b$>>"

    print('-' * 20)
    dpda_design = DPDADesign(1, '$', [1], rulebook)
    assert dpda_design.is_accepts('(((((((())))))))')
    assert dpda_design.is_accepts('()(())(())((()))')
    assert not dpda_design.is_accepts('(()(()(()()(()()))()')

    print('-' * 20)
    dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
    dpda.read_string('())')
    assert not dpda.is_accepting()
    assert dpda.is_stuck()
    assert not dpda_design.is_accepts('())')

    print('-' * 20)
    c1 = PDAConfiguration(1, Stack(['$']))
    c2 = PDAConfiguration(1, Stack(['$']))
    assert c1 == c2