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

if __name__ == "__main__":
    
    tape = Tape(['1', '0', '1'], '1', [], '_')
    assert str(tape) == '<Tape 101(1)>'
    assert str(tape.move_head_left()) == '<Tape 10(1)1>'
    assert str(tape.write('0')) == '<Tape 101(0)>'
    assert str(tape.move_head_right()) == '<Tape 1011(_)>'
    assert str(tape.move_head_right().write('0')) == '<Tape 1011(0)>'