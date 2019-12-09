TRUE = lambda x : lambda y: x
FALSE = lambda x : lambda y: y

def to_boolean(proc):
    return proc(True)(False)

if __name__ == "__main__":
    assert to_boolean(TRUE)
    assert not to_boolean(FALSE)