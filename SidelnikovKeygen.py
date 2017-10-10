#!/usr/bin/python3
import random
import sympy
import numpy
import itertools
from SidelnikovUtil import *

x = sympy.Symbol('x')
alpha = sympy.Symbol('a')
# Generate key pairs
def keygen(r_val, m_val, files):
    global x
    # Produce k*n generator matrix G for the code
    G_matrix = get_RM(r_val, m_val)
    if args.v: print('\nG ='); sympy.pprint(G_matrix); print(G_matrix.shape)
    k_val = G_matrix.shape[0]
    H_matrix = get_H(G_matrix[:,:])
    if args.v: print('\nH ='); sympy.pprint(H_matrix); print(H_matrix.shape)
    # Select a random k*k binary non-singular matrix S
    S_matrix = get_nonsingular(k_val)
    if args.vv: print('\nS ='); sympy.pprint(S_matrix)
    # Select a random n*n permutation matrix P
    n_val = G_matrix.shape[1]
    permutation = random.sample(range(n_val), n_val)
    P_matrix = sympy.Matrix(n_val, n_val,
    						lambda i, j: int((permutation[i]-j)==0))
    if args.vv: print('\nP ='); sympy.pprint(P_matrix)
    # Compute k*n matrix G_pub = SGP
    G_pub = (S_matrix * G_matrix * P_matrix).applyfunc(lambda x: mod(x,2))
    if args.v: print('\nG_pub ='); sympy.pprint(G_pub); print(G_pub.shape)
    # Public key is (G_pub, t)
    # Private key is (S, G, P)
    # length of the Code
    if args.v: print("\nn = ", n_val)
    if args.v: print("k =", k_val)
    t_val = pow(2, m_val-r_val-1) - 1
    if args.v: print("t =", t_val)
    writeKeys(G_pub, t_val, S_matrix, H_matrix, P_matrix, files)
def get_H(bin_G):
    for i in range(bin_G.shape[0]):
        bin_G.col_del(0)
    bin_H = bin_G.T
    ident = sympy.eye(bin_H.shape[0])
    for i in range(bin_H.shape[0]):
        bin_H = bin_H.col_insert(bin_H.shape[1], ident.col(i))
    return(bin_H)
# create the Generator matrix
def get_RM(r_val, m_val):
    n_val = pow(2, m_val)
    variables = []
    row_var = []
    for i in range(m_val):
        variables.append(i)
        row_var.append(i)
    for i in range(r_val-1):
        for comb in itertools.combinations(variables, i+2):
            row_var.append(comb)
    k_val = len(row_var) + 1
    var_matrix = []
    period = n_val
    cycles = 1
    for v in variables:
        row = sympy.Matrix(1, 0, [])
        for c in range(cycles):
            row = row.row_join(sympy.zeros(1, period/2))
            row = row.row_join(sympy.ones(1, period/2))
        var_matrix.append(row)
        cycles *= 2
        period /= 2
    var_matrix = list(reversed(var_matrix))
    RM_matrix = sympy.ones(1, n_val)
    for i in range(k_val-1):
        new_row = sympy.ones(1, n_val)
        try:
            for j in row_var[i]:
                new_row = new_row.multiply_elementwise(var_matrix[j])
        except TypeError:
            new_row = var_matrix[i]
        RM_matrix = RM_matrix.col_join(new_row)
    RM_matrix, pivot = RM_matrix.rref(iszerofunc=lambda x: x % 2==0)
    RM_matrix = RM_matrix.applyfunc(lambda x: mod(x,2))
    RM_matrix = fixup_G(RM_matrix, pivot)
    return(RM_matrix)
def fixup_G(bin_H, pivot):
    num_removed = 0
    for j in range(bin_H.shape[0]):
        if bin_H.row(j-num_removed) == sympy.zeros(1, bin_H.shape[1]):
            bin_H.row_del(j-num_removed)
            num_removed += 1
    for i in range(bin_H.shape[0]):
        if not i == pivot[i]:
            col_a = bin_H.col(i)
            col_b = bin_H.col(pivot[i])
            bin_H.col_del(i)
            bin_H = bin_H.col_insert(i, col_b)
            bin_H.col_del(pivot[i])
            bin_H = bin_H.col_insert(pivot[i], col_a)
    return(bin_H)
# From https://stackoverflow.com/questions/31190182/sympy-solving-matrices
# -in-a-finite-field
def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    if denom % modulus == 0:
        denom = int(denom/modulus)
    try:
        return numer*sympy.mod_inverse(denom,modulus) % modulus
    except:
        raise ValueError('Unable to apply modulus to matrix')
        exit()
def get_nonsingular(k_val):
    # Randomly generate a k*k Matrix
    # If it is singular generate another
    while True:
        matrix = sympy.Matrix(numpy.random.choice([sympy.Integer(0),
        		 sympy.Integer(1)], size=(k_val, k_val), p=[1./3, 2./3]))
        if matrix.det() % 2:
            return matrix