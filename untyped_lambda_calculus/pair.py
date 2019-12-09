PAIR = lambda x: lambda y: lambda f: f(x)(y)
LEFT = lambda p: p(lambda x: lambda y: x)
RIGHT = lambda p: p(lambda x: lambda y: y)

if __name__ == "__main__":
    from number import ONE, TWO, to_integer
    my_pair = PAIR(ONE)(TWO)
    assert to_integer(LEFT(my_pair)) == 1
    assert to_integer(RIGHT(my_pair)) == 2