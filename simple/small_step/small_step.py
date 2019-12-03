class Machine:
    def __init__(self, statement, environment):
        self.statement = statement
        self.environment = environment
    
    def step(self):
        self.statement, self.environment = self.statement.reduce(self.environment)
    
    def run(self):
        print(f'machine start running ...')
        while self.statement.is_reducible():
            print('-'*20)
            print(f'In environment: {self.environment}')
            print(f'reduce {self.statement}')
            self.step()
            print('-'*20)
        print(f'machine end running...')
        print(f'statement: {self.statement}, environment: {self.environment}')


class Environment(dict):
    def __str__(self):
        str__ = '{' + ', '.join([f'{k}: {v}'for k, v in self.items()]) + '}'
        return f'{str__}'


class DoNothing:
    def __init__(self):
        pass

    def __str__(self):
        return f'<do nothing>'
    
    def __eq__(self, other):
        return isinstance(other, DoNothing)
    
    def is_reducible(self):
        return False


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'
    
    def is_reducible(self):
        return True
    
    def reduce(self, environment):
        return environment[self.name]


class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        print(f'init assign, {self.expression}')

    def __str__(self):
        return f'{self.name} = {self.expression}'

    def is_reducible(self):
        return True
    
    def reduce(self, environment):
        if self.expression.is_reducible():
            print(f'assigin: {self.expression} is reducible')
            return Assign(self.name, self.expression.reduce(environment)), environment
        else:
            print(f'update env')
            environment.update({self.name: self.expression})
            return DoNothing(), environment 


class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    
    def __str__(self):
        return f'{self.first}; {self.second}'
    
    def is_reducible(self):
        return True
    
    def reduce(self, environment):
        if self.first == DoNothing():
            return self.second, environment
        else:
            reduced_first, reduced_environment = self.first.reduce(environment)
            return Sequence(reduced_first, self.second), reduced_environment


class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return f'if {self.condition}: {self.consequence} else {self.alternative}'
    
    def is_reducible(self):
        return True
    
    def reduce(self, environment):
        if self.condition.is_reducible():
            return If(self.condition.reduce(environment), self.consequence, self.alternative), environment
        else:
            if self.condition == Boolean(True):
                return self.consequence, environment
            else:
                return self.alternative, environment


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __str__(self):
        return f'while ({self.condition}) {self.body}'
    
    def is_reducible(self):
        return True
    
    def reduce(self, environment):
        return If(self.condition, Sequence(self.body, self), DoNothing()), environment


class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'<{self.value}>'

    def is_reducible(self):
        return False


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} + {self.right}'

    def is_reducible(self):
        return True    

    def reduce(self, environment):
        if self.left.is_reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)


class Boolean:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'<{self.value}>'
    
    def __eq__(self, other):
        return self.value == other.value
    
    def is_reducible(self):
        return False


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'{self.left} < {self.right}'
    
    def is_reducible(self):
        return True
    
    def reduce(self,environment):
        if self.left.is_reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)


if __name__ == "__main__":
    # Machine(Assign('a', Add(Number(5), Number(3))), Environment()).run()
    # Machine(Assign('b', LessThan(Number(5), Number(3))), Environment()).run()
    # Machine(If(LessThan(Number(5), Number(3)), Assign('a', Number(55)), Assign('a', Number(33))), Environment()).run()
    # Machine(Sequence(Assign('a', Number(3)), Assign('b', Add(Number(1), Number(4)))), Environment()).run()
    # Machine(Sequence(Assign('a', Number(0)), Assign('a', Add(Variable('a'), Number(1)))), Environment()).run()


    """
    sum10 = 0
    i = 0    
    while i < 11:
        sum10 += i
        i += 1
    """

    Machine(
        Sequence(
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
        ),
        Environment()
    ).run()
