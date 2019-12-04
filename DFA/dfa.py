class FARule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state
    
    def applies_to(self, state, character):
        return self.state == state and self.character == character
    
    def follow(self):
        return self.next_state
    
    def __str__(self):
        return f'<FARule {str(self.state)} --{self.character}--> {str(self.next_state)}>'
    

class DFARulebook:
    def __init__(self, rules):
        self.rules = rules
    
    def next_state(self, state, character):
        return self.rule_for(state, character).follow()
    
    def rule_for(self, state, character):
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule


class DFA:
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook
    
    def accepting(self):
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = rulebook.next_state(self.current_state, character)
        return self.current_state
    
    def read_string(self, string):
        for char in string:
            self.read_character(char)
        return self.current_state


class DFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
    
    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)
    
    def accepts(self, string):
        dfa = self.to_dfa()
        dfa.read_string(string)
        return dfa.accepting()


if __name__ == "__main__":

    # DFA that only accepts character stream contains sequence 'ab'
    rulebook = DFARulebook([
        FARule(1, 'a', 2), FARule(1, 'b', 1),
        FARule(2, 'a', 2), FARule(2, 'b', 3),
        FARule(3, 'a', 3), FARule(3, 'b', 3)
    ])

    print('-' * 20)
    print(rulebook.next_state(1, 'a'))  # 2
    print(rulebook.next_state(1, 'b'))  # 1
    print(rulebook.next_state(2, 'b'))  # 3
    
    print('-' * 20)
    dfa = DFA(1, [3], rulebook)
    print(dfa.accepting())  # False
    dfa.read_character('b')
    print(dfa.accepting())  # False
    dfa.read_character('a')
    print(dfa.accepting())  # False
    dfa.read_character('b')
    print(dfa.accepting())  # True
    
    print('-' * 20)
    dfa = DFA(1, [3], rulebook)
    dfa.read_string('aaabbbaaa')
    print(dfa.accepting()) # True
    dfa = DFA(1, [3], rulebook)
    dfa.read_string('bbbbbbbbaa')
    print(dfa.accepting()) # False
    
    print('-' * 20)
    dfa_desgin = DFADesign(1, [3], rulebook)
    print(dfa_desgin.accepts('aaabbbbaaa')) # True
    print(dfa_desgin.accepts('bbbbbbbbaa')) # False
