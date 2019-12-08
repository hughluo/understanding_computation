class Stack:
    """Purely functional non-destructive stack"""
    def __init__(self, list_):
        self.stk = [e for e in list_]

    def __eq__(self, other):
        return self.stk == other.stk
    
    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        rest = ''.join((char for char in self.stk[1:]))
        return f'<Stack ({self.top()}){rest}>'
    
    def pop(self):
        return Stack(self.stk[1:])

    def push(self, character):
        return Stack([character] + self.stk[:])

    def top(self):
        return self.stk[0]

if __name__ == "__main__":
    print('-' * 20)
    stack = Stack(['a', 'b', 'c', 'd', 'e'])
    print(stack)                                    #  <Stack (a)bcde>
    print(stack.top())                              # a
    print(stack.pop().pop().top())                  # c
    print(stack.push('x').push('y').top())          # y
    print(stack.push('x').push('y').pop().top())    # x