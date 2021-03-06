from entropy import *
from generate_random_quantum import *
from evolution import *
import time

# TEST UNITARY <ATRIX IS UNITARY
def test_unitary(u):
    """
    Returns true if u is unitary
    """
    assert is_unitary(u) == True

# TEST HERMITIAN MATRIX IS HERMITIAN
def test_hermitian(h):
    """
    Returns true if h is hermitian
    """
    assert is_hermitian(h) == True

# TEST CONDITIONS FOR DENSITY MATRIX
def test_density_matrix(d):
    """
    Returns true if d is a density matrix
    """
    # Hermitian and positive semi definite
    assert is_hermitian(d) == True
    assert is_positive_semi_def(d) == True
    # Trace = 1
    assert np.isclose(np.trace(d).real, 1) == True
    assert is_close_to_zero(np.trace(d).imag) == True

# USED FOR TESTING INEQUALITIES THAT CAN TAKE MULTIPARTITE STATES
def test_defs(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2**2) # 2-qubit state
        test_func(p2)
        p3 = gen_func(2**3) # 3-qubit state
        test_func(p3)
        p4 = gen_func(2**4) # 4-qubit state
        test_func(p4)
        p5 = gen_func(2**5) # 5-qubit state
        test_func(p5)

        q2 = gen_func(3**2) # 2-qutrit state
        test_func(q2)
        q3 = gen_func(3**3) # 3-qutrit state
        test_func(q3)
        q4 = gen_func(3**4) # 4-qutrit state
        test_func(q4)
        q5 = gen_func(3**5) # 5-qutrit state
        test_func(q5)

    print("%d of each of 2 - 5 qubit and qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))


# # USED FOR TESTING INEQUALITIES THAT CAN TAKE MULTIPARTITE STATES
def test_defs_true(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2**2) # 2-qubit state
        assert test_func(p2) == True
        p3 = gen_func(2**3) # 3-qubit state
        assert test_func(p3) == True
        p4 = gen_func(2**4) # 4-qubit state
        assert test_func(p4) == True
        p5 = gen_func(2**5) # 5-qubit state
        assert test_func(p5) == True

        q2 = gen_func(3**2) # 2-qutrit state
        assert test_func(q2) == True
        q3 = gen_func(3**3) # 3-qutrit state
        assert test_func(q3) == True
        q4 = gen_func(3**4) # 4-qutrit state
        assert test_func(q4) == True
        q5 = gen_func(3**5) # 5-qutrit state
        assert test_func(q5) == True


    print("%d of each of 2 - 5 qubit and qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))


# TEST ENTROPY IN PURE STATE IS ZERO
def test_pure_state_entropy_is_zero(p):
    """
    Returns true if vonNeumann entropy of pure state is zero
    """
    vn = vonNeumann(p)
    assert is_close_to_zero(vn) == True

# TEST RELATIVE ENTROPY NON-NEGATIVE
def test_relative_entropy_non_negative(p,r):
    """
    Return true if relative entropy is non-negative, with equality
    if and only if p = r
    """
    assert is_non_neg_relative_entropy(p,r) == True
    re = relative_entropy(p, p)
    # Relative entropy h(p || p) = 0
    assert is_close_to_zero(re) == True


# TEST RELATIVE ENTROPY INEQUALITIES
def test_re(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2**2) # 2-qubit state
        r2 = gen_func(2**2) # 2-qubit state
        test_func(p2,r2)
        p3 = gen_func(2**3) # 3-qubit state
        r3 = gen_func(2**3) # 3-qubit state
        test_func(p3,r3)
        p4 = gen_func(2**4) # 4-qubit state
        r4 = gen_func(2**4) # 4-qubit state
        test_func(p4,r4)

        q2 = gen_func(3**2) # 2-qutrit state
        w2 = gen_func(3**2) # 2-qutrit state
        test_func(q2,w2)
        q3 = gen_func(3**3) # 3-qutrit state
        w3 = gen_func(3**3) # 3-qutrit state
        test_func(q3,w3)

    print("%d of each of 2,3,4 qubit states and 2,3 qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))


# TEST MONOTONICITY RELATIVE ENTROPY
def test_monotonic_re(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2**2) # 2-qubit state
        r2 = gen_func(2**2) # 2-qubit state
        assert test_func(p2,r2,2) == True

        q2 = gen_func(3**2) # 2-qutrit state
        w2 = gen_func(3**2) # 2-qutrit state
        assert test_func(q2,w2,3) == True

    print("%d of each of 2,3,4 qubit and qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))

# USED TO TEST INEQUALITIES USING 2-PARTITE STATES
def test_bi_partite(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2**2) # 2-qubit state
        assert test_func(p2,2) == True

        q2 = gen_func(3**2) # 2-qutrit state
        assert test_func(q2,3) == True


    print("%d of each of 2 qubit and qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))

# USED TO TEST INEQUALITIES USING 3-PARTITE STATES
def test_tri_partite(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p3 = gen_func(2**3) # 3-qubit state
        assert test_func(p3,2) == True

        q3 = gen_func(3**3) # 3-qutrit state
        assert test_func(q3,3) == True

    print("%d of each of 3 qubit and qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))

# USED TO TEST INEQUALITIES USING 4-PARTITE STATES
def test_4_partite(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p4 = gen_func(2**4) # 4-qubit state
        q4 = gen_func(3**4) # 4-qutrit state

        assert test_func(p4, 2) == True
        assert test_func(q4, 3) == True

    print("%d of each of 4 qubit and qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))


# TEST CHANNEL PARTIAL TRACE PRESERVING
def test_PTP(gen_func, channel_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2) # 1-qubit state
        assert is_PTP(channel_func, p2) == True

    print("%d of 1-qubit states tested" % (lim))
    print("is_PTP %s: --- PASSED in %s seconds ---" % (channel_func, time.clock() - start_time))

# TEST QUANTUM CHANNEL UNITAL
def test_unital(gen_func, channel_func, lim):
    start_time = time.clock()
    for i in range(lim):
        assert is_unital(channel_func,2) == True

    print("%d times tested" % (lim))
    print("is_unital %s: --- PASSED in %s seconds ---" % (channel_func, time.clock() - start_time))


# TEST QUANTUM CHANNEL NOT UNITAL
def test_not_unital(gen_func, channel_func, lim):
    start_time = time.clock()
    for i in range(lim):
        assert is_unital(channel_func,2) == False

    print("%d times tested" % (lim))
    print("is_unital %s: --- PASSED in %s seconds ---" % (channel_func, time.clock() - start_time))


# TEST CTPT UNITAL CHANNELS GIVE GREATER OR CONSTANT ENTROPY
def test_entropy_more(gen_func, channel_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2) # 1-qubit state
        prob = 0
        for i in range(11):
            assert is_CPTP_entropy_more(channel_func,p2, prob) == True
            prob = prob + 0.1

    print("%d of 1-qubit states tested" % (lim))
    print("is_CPTP_entropy_more %s: --- PASSED in %s seconds ---" % (channel_func, time.clock() - start_time))



# TEST UNITARY EVOLUTON GIVES CONSTANT ENTROPY
def test_constant_entropy(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p2 = gen_func(2**2) # 2-qubit state
        u2 = generate_unitary(2**2) # 2-qubit state
        assert is_entropy_constant(test_func, p2, u2) == True
        p3 = gen_func(2**3) # 3-qubit state
        u3 = generate_unitary(2**3) # 3-qubit state
        assert is_entropy_constant(test_func, p3, u3) == True
        p4 = gen_func(2**4) # 4-qubit state
        u4 = generate_unitary(2**4) # 4-qubit state
        assert is_entropy_constant(test_func, p4, u4) == True
        p5 = gen_func(2**5) # 5-qubit state
        u5 = generate_unitary(2**5) # 5-qubit state
        assert is_entropy_constant(test_func, p5, u5) == True

        q2 = gen_func(3**2) # 2-qutrit state
        w2 = generate_unitary(3**2) # 2-qutrit state
        assert is_entropy_constant(test_func, q2, w2) == True
        q3 = gen_func(3**3) # 3-qutrit state
        w3 = generate_unitary(3**3)# 3-qutrit state
        assert is_entropy_constant(test_func, q3, w3) == True
        q4 = gen_func(3**4) # 4-qutrit state
        w4 = generate_unitary(3**4) # 4-qutrit state
        assert is_entropy_constant(test_func, q4, w4) == True
        q5 = gen_func(3**5) # 5-qutrit state
        w5 = generate_unitary(3**5) # 5-qutrit state
        assert is_entropy_constant(test_func, q5, w5) == True


    print("%d of each of 2 - 5 qubit and qutrit states tested" % (lim))
    print("is_entropy_constant %s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))


# USED TO TEST NON SHANNON INEQUALITIES
def test_non_shannon(gen_func, test_func, lim):
    start_time = time.clock()
    for i in range(lim):
        p4 = gen_func(2**4) # 4-qubit state
        q4 = gen_func(3**4) # 4-qutrit state

        res, _ = test_func(p4, 2)
        res, _ = test_func(q4, 3)
        assert res == True

    print("%d of each of 4 qubit and qutrit states tested" % (lim))
    print("%s: --- PASSED in %s seconds ---" % (test_func, time.clock() - start_time))
