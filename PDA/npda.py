from stack import Stack
from dpda import PDARule, PDAConfiguration 
from time import sleep

class NPDARulebook:
    def __init__(self, rules):
        self.rules = rules
    
    def next_configurations(self, configurations, character):
        res = set()
        for config in configurations:
            for config in self.follow_rules_for(config, character):
                res.add(config)
        return res

    def follow_free_moves(self, configurations):
        more_configurations = self.next_configurations(configurations, None)
        if more_configurations.issubset(configurations):
            return configurations
        else:
            return self.follow_free_moves(configurations | more_configurations)
        
    def follow_rules_for(self, configuration, character):
        res = []
        for rule in self.rules_for(configuration, character):
            res.append(rule.follow(configuration))
        return res
    
    def rules_for(self, configuration, character):
        res = []
        for rule in self.rules:
            if rule.is_applies_to(configuration, character):
                res.append(rule)
        return res


class NPDA:
    def __init__(self, current_configurations, accept_states, rulebook):
        self.current_configurations = current_configurations
        self.accept_states = accept_states
        self.rulebook = rulebook

    def current_configurations_(self):
        self.current_configurations = self.rulebook.follow_free_moves(self.current_configurations)
        return self.current_configurations

    def is_accepting(self):
        self.current_configurations_()
        curret_states = set((config.state for config in self.current_configurations))
        intersect = curret_states.intersection(self.accept_states)
        return len(intersect) > 0

    def read_character(self, character):
        self.current_configurations = rulebook.next_configurations(self.current_configurations_(), character)
    
    def read_string(self, string):
        for char in string:
            self.read_character(char)

class NPDADesign:
    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self.start_state = start_state
        self.bottom_character = bottom_character
        self.accept_states = accept_states
        self.rulebook = rulebook
    
    def is_accepts(self, string):
        npda = self.to_dpda()
        npda.read_string(string)
        return npda.is_accepting()
    
    def to_dpda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return NPDA(set([start_configuration]), self.accept_states, self.rulebook)

if __name__ == "__main__":
    rulebook = NPDARulebook([
        PDARule(1, 'a', 1, '$', ['a', '$']),
        PDARule(1, 'a', 1, 'a', ['a', 'a']),
        PDARule(1, 'a', 1, 'b', ['a', 'b']),
        PDARule(1, 'b', 1, '$', ['b', '$']),
        PDARule(1, 'b', 1, 'a', ['b', 'a']),
        PDARule(1, 'b', 1, 'b', ['b', 'b']),
        PDARule(1, None, 2, '$', ['$']),
        PDARule(1, None, 2, 'a', ['a']),
        PDARule(1, None, 2, 'b', ['b']),
        PDARule(2, 'a', 2, 'a', []),
        PDARule(2, 'b', 2, 'b', []),
        PDARule(2, None, 3, '$', ['$']),
    ])

    configuration = PDAConfiguration(1, Stack(['$']))
    npda = NPDA(set([configuration]), [3], rulebook)
    assert npda.is_accepting()
    npda.read_string('abb')
    assert not npda.is_accepting()
    npda.read_string('a')
    assert npda.is_accepting()

    npda_design = NPDADesign(1, '$', [3], rulebook)
    assert npda_design.is_accepts('abba')
    assert npda_design.is_accepts('babbaabbab')
    assert not npda_design.is_accepts('abb')
    assert not npda_design.is_accepts('baabaa')