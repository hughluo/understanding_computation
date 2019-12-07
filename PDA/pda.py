from stack import Stack

class PDAConfiguration:
    def __init__(self, state, stack):
        self.state = state
        self.stack = stack
    
    def __str__(self):
        return f'<PDAConfiguration state={self.state}, stack={str(self.stack)}>'


class PDARule:
    def __init__(self, state, character, next_state, pop_character, push_character):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.pop_character = pop_character
        self.push_character = push_character

    def applies_to(self, configuration, character):
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
            if rule.applies_to(configuration, character):
                return rule
    
    def applies_to(self, configuration, character):
        pass


class DPDA:
    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accepting(self):
        return self.current_configuration.state in self.accept_states

    def read_character(self, character):
        self.current_configuration = rulebook.next_configuration(self.current_configuration, character)
    
    def read_string(self, string):
        for char in string:
            self.read_character(char)
    

if __name__ == "__main__":
    print('-' * 20)
    rule = PDARule(1, '(', 2, '$', ['b', '$'])
    configuration = PDAConfiguration(1, Stack(['$']))
    print(rule.applies_to(configuration, '('))  # True
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
    print(dpda.accepting())
    assert dpda.accepting()
    dpda.read_string('(()')
    print(dpda.accepting())
    assert not dpda.accepting()
    print(dpda.current_configuration)
    assert str(dpda.current_configuration) == "<PDAConfiguration state=2, stack=<Stack (b)$>>"