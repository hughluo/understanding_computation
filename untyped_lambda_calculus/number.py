ZERO  = lambda p : lambda x: x
ONE   = lambda p : lambda x: p(x)
TWO   = lambda p : lambda x: p(p(x))

def to_integer(proc):
    return proc(lambda n: n + 1)(0)

if __name__ == "__main__":
    assert to_integer(ZERO) == 0
    assert to_integer(ONE) == 1
    assert to_integer(TWO) == 2
