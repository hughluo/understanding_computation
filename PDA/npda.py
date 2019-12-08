from stack import Stack
from pda import PDARule, PDAConfiguration 
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