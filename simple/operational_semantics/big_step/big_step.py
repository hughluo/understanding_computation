class Environment(dict):
    def __str__(self):
        str__ = '{' + ', '.join([f'{k}: {v}'for k, v in self.items()]) + '}'
        return f'{str__}'
  

# Expressions

class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'
    
    def evaluate(self, environment):
        return environment[self.name]


class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'<{self.value}>'

    def evaluate(self, environment):
        return self


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} + {self.right}'

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value + self.right.evaluate(environment).value)


class Boolean:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'<{self.value}>'
    
    def __eq__(self, other):
        return self.value == other.value
    
    def evaluate(self, environment):
        return self


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'{self.left} < {self.right}'
    
    def evaluate(self, environment):
        return Boolean(self.left.evaluate(environment).value < self.right.evaluate(environment).value)


# Statements

class DoNothing:
    def __init__(self):
        pass

    def __str__(self):
        return f'<do nothing>'
    
    def __eq__(self, other):
        return isinstance(other, DoNothing)

    def evaluate(self, environment):
        return environment  


class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        print(f'init assign, {self.expression}')

    def __str__(self):
        return f'{self.name} = {self.expression}'

    def evaluate(self, environment):
        environment.update({self.name: self.expression.evaluate(environment)})
        return environment


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
    # env = Environment()
    # env['x'] = Number(1)
    # end_env = While(
    #     LessThan(Variable('x'), Number(5)),
    #     Assign('x', Add(Variable('x'), Number(1)))
    # ).evaluate(env)
    # print(end_env)

    env = Environment()
    end_env = Sequence(
        Assign('sum10', Number(0)),
        Sequence(
            Assign('i', Number(0)),
            While(
                LessThan(Variable('i'), Number(11)),
                Sequence(
                    Assign('sum10', Add(Variable('sum10'), Variable('i'))),
                    Assign('i', Add(Variable('i'), Number(1)))
                )
            )
        )
    ).evaluate(env)
    print(end_env)