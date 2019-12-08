# Pushdown Automata

A pushdown auotmaton is a finite state machine with a buil-in stack.

DFA cannot solve the problem such as "balancing brackets" cause a finite automaton must always have a finite number of states, so for any given machine, there is always a finite limit to how many levels of nesting it can support (it cannot keep track of an arbitray amount of information).

## DPDA

There should be no configurations where the machine's next move is ambiguous of conflicting rules.
But it is okay to write a free move rule that does not read any input, as long as there are not any other rules for the same state and top-of-stack character.
DPDA can only have one rule that applies when the machine in a very state.

## NPDA

Palindrome problem is an example of a job where an NPDA can do something that a DPDA cannot.

Unlike the NFA-to-DFA trick, we cannot represent multiple NPDA configurations as a single DPDA configuration. Because there is no way to combine all the possible stacks into a single stack so that a DPDA can still see all the topmost characters and access every possible stack individually.
