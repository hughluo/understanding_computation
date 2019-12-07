class FARule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state
    
    def is_applies_to(self, state, character):
        return self.state == state and self.character == character
    
    def follow(self):
        return self.next_state
    
    def __str__(self):
        return f'<FARule {str(self.state)} --{self.character}--> {str(self.next_state)}>'
    

class NFARulebook:
    def __init__(self, rules):
        self.rules = rules
    
    def next_states(self, states, character):
        res = set()
        for state in states:
            for state in self.follow_rules_for(state, character):
                res.add(state)
        return res

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        
        if all(s in states for s in more_states):
            return states
        else:
            return self.follow_free_moves(states | more_states)
        
    def follow_rules_for(self, state, character):
        res = []
        for rule in self.rules_for(state, character):
            res.append(rule.follow())
        return res
    
    def rules_for(self, state, character):
        res = []
        for rule in self.rules:
            if rule.is_applies_to(state, character):
                res.append(rule)
        return res


class NFA:
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def current_states_(self):
        self.current_states = self.rulebook.follow_free_moves(self.current_states)
        return self.current_states

    def is_accepting(self):
        intersect = self.current_states.intersection(self.accept_states)
        return len(intersect) > 0

    def read_character(self, character):
        self.current_states = rulebook.next_states(self.current_states_(), character)
        return self.current_states
    
    def read_string(self, string):
        for char in string:
            self.read_character(char)
        return self.current_states


class NFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
    
    def to_nfa(self):
        return NFA({self.start_state}, self.accept_states, self.rulebook)
    
    def is_accepts(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.is_accepting()


if __name__ == "__main__":
    print('-' * 20)
    rulebook = NFARulebook([
        FARule(1, None, 2), FARule(1, None, 4),
        FARule(2, 'a', 3), 
        FARule(3, 'a', 2),
        FARule(4, 'a', 5), 
        FARule(5, 'a', 6),
        FARule(6, 'a', 4) 
    ])
    print(rulebook.next_states({1}, None))  # {2, 4}

    print('-' * 20)
    print(rulebook.follow_free_moves({1}))  # {1, 2, 4}

    print('-' * 20)
    nfa_design = NFADesign(1, [2, 4], rulebook)
    print(nfa_design.is_accepts('aa'))     # True
    print(nfa_design.is_accepts('aaa'))    # True
    print(nfa_design.is_accepts('aaaaa'))  # False
    print(nfa_design.is_accepts('aaaaaa')) # True