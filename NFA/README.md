# Nondeterministic Finite Automata

Any NFA can be translated to a DFA, because we can use a single DFA state to represent many possible NFA states, to simulate an NFA we only need to keep track of whate staes it could currently be in, then pick a different set of pissible states each time we read an input character.

* NFA
* NFA-Epsilon

## Terminology

* symbols: character
* transitions: rules for moving between states
* transition function: rulebook
* epsilon: None when passing character
* epsilon-transitions: free moves
