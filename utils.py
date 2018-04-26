import numpy as np
from numpy import linalg as LA
import math
import random
import sys


def isMatrixSame(A, B):
    """
    Returns true if matrices A and B are equal
    """
    dimA = A.shape
    dimB = B.shape

    if(dimA != dimB):
        return False

    for i in range(dimA[0]):
        for j in range(dimA[0]):
            if(not isclose(A[i,j],B[i,j])):
                return False
    return True


def matrixInList(A, L):
    """
    Returns true if matrix A is the list L
    """
    # if list empty
    if(not L):
        return False

    for l in L:
        if(isMatrixSame(A, l)):
            return True
    return False


def isclose(a, b, rel_tol=1e-14, abs_tol=0.0):
    """
    Compares floating point numbers
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def allocSub(p):
    """
    Allocates space needed to store each separated density matrix of p
    """
    dim = p.shape[0]
    sub_dim = 0

    if(isPowerof2(dim)): # qubit
        sub_dim = dim / 2
    elif(isPowerof3(dim)): # qutrit
        sub_dim = dim / 3

    # Error if sub_dim is still = 0
    if sub_dim == 0:
        print "Error in Function 'allocSub in utils.py':"
        print "Density matrix dimension not power of 2 (qubit) or 3 (qutrit)"

    temp = np.zeros((sub_dim, sub_dim))
    sub_p = np.matrix(temp, dtype=np.complex128)

    return sub_p

def isPowerof2(n):
    """
    Returns true if n is a power of 2 i.e can be written as 2^q = n
    """
    return (n and not (n & (n-1)))


def isPowerof3(n):
    """
    Returns true if n is a power of 3 i.e can be written as 3^q = n
    """
    # 3^19 = 1162261467
    return 1162261467 % n == 0;


def check_n_qubit(p,n):
    """
    Ensures quantum system p is a n qubit quantum state
    """
    dim = p.shape[0]
    if(dim != 2**n):
        print "Error in Function 'check_n_qubit in utils.py':"
        print "Quantum system is not a " + str(n) + " qubit system"
        sys.exit()

def check_power_of_dim(n,dim,func_str):
    """
    Checks that density matrix dimentsion n = dim^q
    If so, return number of qubits/qutrits...
    If not, exit with error
    """
    m = math.log(n)
    n = math.log(dim)
    q = m / n

    # Checks that q is an integer
    if((m%n) == 0):
        return q
    else:
        print "Error in Function '" + func_str +"':"
        print "Density matrix given is neither a qubit or qutrit system."
        print "i.e. Width and Length of matrix is not in form 2^q (qubit) or 3^q (qutrit)"
        sys.exit()



def testTrue(func, args, lim):
    """
    Function that runs functions many times
    """
    for i in range(lim):
        if not func(args) :
            return False
    return True


def getCombinations(A, n):
    """
    Function that returns all the 'n' digit combinations of values in array A
    """


# def __getCombinations_helper()
