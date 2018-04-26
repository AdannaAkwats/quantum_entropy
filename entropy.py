import numpy as np
from numpy import linalg as LA
import math
import random
from shannon import randomProbabilityDist
from partial_trace import separate
from utils import check_n_qubit
from utils import check_power_of_dim

def vonNeumann(A):
    """
    Calculate the Von Neumann Entropy of a quantum state
    """

    # Get eigenvalues of A
    values, _ = LA.eig(A)
    values = values.real
    # Take the natural logarithm of the eigenvalues and sum them
    v = values*np.log2(values)
    return -np.sum(v)


def is_non_neg_VN(A):
    """
    Returns true if vonNeumann entropy >= 0
    """
    return vonNeumann(A) >= 0


def is_non_neg_relative_entropy(p,r):
    """
    Validates Klein's inequality: The quantum relative entropy is non-negative,
    with equality if and only if p = r
    """
    return relative_entropy(p,r) >= 0


def conditional_entropy(pAB):
    """
    calculates the conditional entropy: H(A|B) = H(A,B) - H(B)
    """

    # Ensure that system is a 2 qubit quantum system
    check_n_qubit(2)

    systems, _ = separate(pAB)
    pB = systems[1]
    H_B = vonNeumann(B)
    H_AB = vonNeumann(pAB)

    return H_AB - H_B


def relative_entropy(p,r):
    """
    Calculates the relative entropy of quantum state p to quantum state r
    H(p||r) = tr(p log p) - tr(p log r)
    """

    #  tr(p log p)
    A = -vonNeumann(p)
    print A
    # tr(p log r)
    eign_p,_ = LA.eig(p)
    eign_p = eign_p.real
    eign_r,_ = LA.eig(r)
    eign_r = eign_r.real
    l = np.log2(eign_r)
    B = eign_p*l
    B = np.sum(B)

    # H(p||r)
    return A - B


def monotocity_relative_entropy(pAB, rAB):
    """
    Returns true if relative entropy is monotonic i.e. H(pA || rA) <= H(pAB || rAB)
    """

    H_AB = relative_entropy(pAB,rAB)
    s_p,_ = separate(pAB)
    pA = s_p[0]
    s_r,_ = separate(rAB)
    rA = s_p[0]
    H_A = relative_entropy(pA, rA)
    return H_A <= H_B

def mutual_information():
    """
    calculates the mutual information defined by: H(A:B) = H(A) + H(B) - H(A,B)
    """
    # Ensure that system is a 2 qubit quantum system
    check_n_qubit(2)

    systems, _ = separate(pAB)
    pA = systems[0]
    pB = systems[1]
    H_A = vonNeumann(A)
    H_B = vonNeumann(B)
    H_AB = vonNeumann(pAB)

    return H_A + H_B - H_AB


def weakSubadditivity(pAB):
    """
    Checks that weak subadditivity holds: H(A,B) <= H(A) + H(B)
    (2 qubit system)
    """

    # Ensure that system is a 2 qubit quantum system
    check_n_qubit(pAB, 2)

    systems, _ = separate(pAB)
    pA = systems[0]
    pB = systems[1]
    H_A = vonNeumann(pA)
    H_B = vonNeumann(pB)
    H_AB = vonNeumann(pAB)

    return H_AB <= H_A + H_B


def strongSubadditivity_q(pABC):
    """
    Checks that strong subadditivity holds: H(A,B,C) + H(B) <= H(A, B)
    + H(B,C) (3 qubit system)
    """

    # Ensure that system is a 3 qubit quantum system
    check_n_qubit(pABC, 3)

    systems, joint_systems = separate(pABC)
    pAB = joint_systems[0]
    pBC = joint_systems[1]
    pB = systems[1]

    H_ABC = vonNeumann(pABC)
    H_AB = vonNeumann(pAB)
    H_BC = vonNeumann(pBC)
    H_B = vonNeumann(pB)

    return H_ABC + H_B <= H_AB + H_BC


def Unitary(n):
    """
    Generate random nxn unitary matrix
    """

    # generate a random complex matrix
    temp = np.zeros((n,n))
    u_rand = np.random.randn(2 * n * n).view(np.complex128)
    X = np.array(temp, dtype=np.complex128)
    k = 0
    for i in range(n):
        for j in range(n):
            X[i,j] = u_rand[k]
            k += 1

    X /= math.sqrt(2)

    # factorize the matrix
    Q, R = LA.qr(X)
    test = np.allclose(X, np.dot(Q,R))

    # For a complex square matrix U, Q should be unitary, so
    # verify that Q is unitary
    Q_mat = np.matrix(Q)
    # Q conjugate
    Q_conj = Q_mat.getH()
    I = np.matmul(Q, Q_conj)

    # unitary matrix Q
    return Q, Q_conj, I


# generates multipartite states
def generate(n):
    """
    Generate random nxn matrix A s.t A = UDU*, where D is diagonal,
    U is unitary matrix and U* is conplex conjugate transpose of U
    """

    # Unitary matrix and its complex conjugate transpose
    U, U_conj, I = Unitary(n)

    # D: diagonal matrix filled with prob distribution so all entries add to 1
    D = np.zeros((n,n))
    diag = randomProbabilityDist(n)
    for i in range(n):
        D[i,i] = diag[i]

    # A = UDU*
    D_mat = np.matrix(D)
    UD = np.matmul(U, D)
    # A = UDU*
    A = np.matmul(UD, U_conj)

    A = A / np.trace(A)

    return A

# TODO : COMPLETE
def generate_unitary(n):
    """
    Generates nxn unitary matrix disributed with Haar Measure
    according to article: https://arxiv.org/pdf/math-ph/0609050.pdf
    """
    # Z ares i.i.d. standard complex normal random variables
    # belongs to Ginibre ensemble
    N = (np.matlib.randn(n,n) + 1j*np.matlib.randn(n,n))/np.sqrt(2.0)
    Q,R = LA.qr(N)
    D = np.diagonal(R)
    R = np.diag(D/np.absolute(D))
    U = Q*R
    # D = np.diagonal(R)
    # P = D/np.absolute(D)
    # U = np.multiply(Q,P,Q)

    # Complex conjuate of U
    U_conj = np.matrix(U)
    U_conj = U_conj.getH()

    print np.multiply(U,U_conj)

    return U


def generate_pure_state(n,dim):
    """
    Generate random pure quantum state of dim
    qubit: dim = 2, qutrit: dim = 3, ...
    """

    func_str = "generate_pure_state in entropy.py"
    check_power_of_dim(n,dim,func_str)

    # p_AB = |u><u|_AB
    # |u>_AB = U_AB |0>_AB
    O = np.zeros(n)
    O[0] = 1

    U = generate_unitary(n)

    # |u>AB = U |0>AB
    u = U.dot(O)

    # <u|AB
    u_mat = np.matrix(u)
    u_conj = u_mat.getH()

    # pAB = |u> <u|
    p = np.matmul(u_conj, u_mat)

    # TODO: Change seps to return higher dimensions
    seps,_ = separate(p)
    pA = seps[0]
    return pA
