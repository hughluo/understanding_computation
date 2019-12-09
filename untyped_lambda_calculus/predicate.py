from number import ZERO, ONE, TWO
from boolean import TRUE, FALSE, to_boolean

IS_ZERO = lambda n: n(lambda x: FALSE)(TRUE)

if __name__ == "__main__":
    assert to_boolean(IS_ZERO(ZERO))
    assert not to_boolean(IS_ZERO(ONE))
    assert not to_boolean(IS_ZERO(TWO))