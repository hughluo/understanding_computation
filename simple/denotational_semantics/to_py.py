class Environment(dict):
    def __str__(self):
        str__ = '{' + ', '.join([f'{k}: {v}'for k, v in self.items()]) + '}'
        return f'{str__}'
    
    def merge(self, other):
        self.update(other)
        return self
  

# Expressions

class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'
    
    def to_py(self):
        return f'lambda e: e[\'{self.name}\']'


class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'<{self.value}>'

    def to_py(self):
        return f'lambda e: {self.value}'


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} + {self.right}'

    def to_py(self):
        return f'lambda e: ({self.left.to_py()}).__call__(e) + ({self.right.to_py()}).__call__(e)'


class Boolean:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'<{self.value}>'
    
    def __eq__(self, other):
        return self.value == other.value
    
    def to_py(self):
        return f'lambda e: {self.value}'


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'{self.left} < {self.right}'
    
    def to_py(self):
        return f'lambda e: ({self.left.to_py()}).__call__(e) < ({self.right.to_py()}).__call__(e)'


# Statements

class DoNothing:
    def __init__(self):
        pass

    def __str__(self):
        return f'<do nothing>'
    
    def __eq__(self, other):
        return isinstance(other, DoNothing)

    def to_py(self):
        return f'lambda e: e'


class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        print(f'init assign, {self.expression}')

    def __str__(self):
        return f'{self.name} = {self.expression}'


    def to_py(self):
        return f'lambda e: e.merge(dict({self.name}=({self.expression.to_py()}).__call__(e)))'

# TODO: Sequnce, If, While
class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    
    def __str__(self):
        return f'{self.first}; {self.second}'
    
    def evaluate(self, environment):
        return self.second.evaluate(self.first.evaluate(environment))    


class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return f'if {self.condition}: {self.consequence} else {self.alternative}'
    
    def evaluate(self, environment):
        b = self.condition.evaluate(environment)
        if b == Boolean(True):
            return self.consequence.evaluate(environment)
        else:
            return self.alternative.evaluate(environment)


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __str__(self):
        return f'while ({self.condition}) {self.body}'
    
    def evaluate(self, environment):
        b = self.condition.evaluate(environment)
        if b == Boolean(True):
            return self.evaluate(self.body.evaluate(environment))
        else:
            return environment


if __name__ == "__main__":
    env = Environment({'x': 3})
    proc = eval(
        Add(
            Variable('x'),
            Number(1)
        ).to_py()
    )
    print(proc.__call__(env))

    proc = eval(
        LessThan(
            Add(
                Variable('x'),
                Number(1)
            ),
            Number(3)
        ).to_py()
    )
    print(proc.__call__(env))

    proc = eval(
        Assign(
            'y',
            Add(
                Variable('x'),
                Number(1)
            )
        ).to_py()
    )
    print(proc.__call__(env))