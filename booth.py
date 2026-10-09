"""Booth's algorithm (signed multiplication) - used in the scorer to compute
weight x violation_count, carried over from Review 1."""


def booth_multiply(m, r, bits=32):
    mask = (1 << bits) - 1
    width = 2 * bits + 1
    wmask = (1 << width) - 1
    A = ((m & mask) << (bits + 1)) & wmask
    S = ((-m & mask) << (bits + 1)) & wmask
    P = ((r & mask) << 1) & wmask
    for _ in range(bits):
        last2 = P & 3
        if last2 == 1:        # 01 -> add multiplicand
            P = (P + A) & wmask
        elif last2 == 2:      # 10 -> subtract multiplicand
            P = (P + S) & wmask
        sign = (P >> (width - 1)) & 1
        P = (P >> 1) | (sign << (width - 1))   # arithmetic shift right
    P >>= 1
    P &= (1 << (2 * bits)) - 1
    if P >> (2 * bits - 1):
        P -= 1 << (2 * bits)
    return P
