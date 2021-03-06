from __future__ import division
import numpy as np
import numpy.matlib
import math
import random
import sys
from numpy import linalg as LA
from entropy import vonNeumann
from generate_random_quantum import generate_hermitian
from utils import *


def u_p_u(U, p):
    """
    Quantum operator e
    e = UpU*
    Function takes a unitary matrix U and a density matrix p and calculates
    UpU* where U* is the complex conjugate transpose
    """

    U_mat = np.matrix(U)
    # Q conjugate
    U_conj = U_mat.getH()

    # Multiply matrices
    Up = np.matmul(U, p)
    UpU_conj = np.matmul(Up, U_conj)

    return UpU_conj


def time_evol_U(t, H):
    """
    Unitary dynamic evolution U = exp{-iHt} where H = Hamitonian (hermitian matrix)
    and t = time
    """

    return np.exp(-1j*t*H)


def time_evol_is_unitary(t, H):
    """
    Returns true if time_evol_U gives unitary matrix
    """
    # Evolve
    ev = time_evol_U(t,H)

    # Conjugate of H
    h_c = np.matrix(H)
    h_c = h_c.getH()

    # complex conjugate of exp
    ev_u = time_evol_U(-t, h_c)

    I = ev*ev_u


def depolarising_channel(Q, prob):
    """
    Models state of quantum system after noise:
    E(p) = (prob * I)/d + (1-prob)*Q
    where Q is the quantum system and prob is the probability that
    the d-dimensional quantum system is depolarised
    """

    # We will focus on only qubit and qutrit
    dim = Q.shape[0]
    d = 2
    if(isPowerof3(dim)):
        d = 3
    elif(not isPowerof2(dim)):
        print("Error in Function 'depolarising_channel in evolution.py':")
        print("Density matrix given is not a qubit or qutrit system.")
        sys.exit()

    I = np.eye(dim)
    E = (prob/d) * I

    return E + (1-prob)*Q


def bit_flip_channel(Q, prob):
    """
    The bit flip channel flips the state of a qubit from 0 to 1 and vice versa
    with probability 1 - prob
    """
    dim = Q.shape[0]
    if(dim != 2):
        print("Error in Function 'bit_phase_flip_channel in evolution.py':")
        print("Density matrix given is not a 2 by 2 matrix.")
        sys.exit()

    I = np.eye(2)
    E_0 = math.sqrt(prob) * I
    II = np.zeros((2,2))
    II[1,0] = 1
    II[0,1] = 1
    E_1 = math.sqrt(1-prob) * II

    E = E_0.dot(Q).dot(E_0) + E_1.dot(Q).dot(E_1)

    return E


def phase_flip_channel(Q, prob):
    """
    The phase flip channel changes the phase of the state of the qubit
    """
    dim = Q.shape[0]
    if(dim != 2):
        print("Error in Function 'bit_phase_flip_channel in evolution.py':")
        print("Density matrix given is not a 2 by 2 matrix.")
        sys.exit()

    I = np.eye(2)
    E_0 = math.sqrt(prob) * I
    II = np.zeros((2,2))
    II[0,0] = 1
    II[1,1] = -1
    E_1 = math.sqrt(1-prob) * II

    E = E_0.dot(Q).dot(E_0) + E_1.dot(Q).dot(E_1)

    return E


def bit_phase_flip_channel(Q, prob):
    """
    This is a combination of a phase flip and a bit flip
    """

    dim = Q.shape[0]
    if(dim != 2):
        print("Error in Function 'bit_phase_flip_channel in evolution.py':")
        print("Density matrix given is not a 2 by 2 matrix.")
        sys.exit()


    I = np.eye(2)
    E_0 = math.sqrt(prob) * I
    temp = np.zeros((2,2))
    II = np.array(temp, dtype=np.complex128)
    II[0,1] = -1j
    II[1,0] = 1j
    E_1 = math.sqrt(1-prob) * II

    E = E_0.dot(Q).dot(E_0) + E_1.dot(Q).dot(E_1)

    return E


def is_entropy_constant(op, p, U):
    """
    Takes a function that evolves p (op) and checks if the entropy
    stays constant
    """

    # Evolve p
    evolved_p = op(U, p)
    H_p = vonNeumann(p)
    H_ev = vonNeumann(evolved_p);

    return isclose(H_p, H_ev)


def is_CPTP_entropy_more(op, p, prob):
    """
    Check that CPTP (Completely positve trace preserving)
    quantum operator obeys inequatlity H(E(p)) >= H(p)
    """
    H_p = vonNeumann(p)
    # Evolve p
    evolved_p = op(p, prob)
    H_e = vonNeumann(evolved_p)

    return (H_e > H_p) or isclose(H_e, H_p)

def CTPT_entropy(op, p, prob):
    H_p = vonNeumann(p)
    # Evolve p
    evolved_p = op(p, prob)
    H_e = vonNeumann(evolved_p)
    return H_p, H_e


def is_unital(op, n):
    """
    Checks that quantum channel op is unital i.e op(I) = I, I being the identity
    """

    I = np.matlib.identity(n)
    prob = 0
    for i in range(11):
        E = op(I, prob)
        if(not isMatrixSame(E, I)):
            return False
        prob = prob + 0.1
    return True


def is_PTP(op, p):
    """
    Checks if quantum operator op is positive and trace preserving
    """

    # Check if evolved matrix is positive self definite and has trace = 1
    prob = 0
    for i in range(11):
        E = op(p, prob)
        eigvalues, _ = np.linalg.eig(E)
        v = eigvalues.real
        tr = np.trace(E).real
        if(np.any(v < 0) or not isclose(tr,1.0)):
            return False
        prob = prob + 0.1
    return True
