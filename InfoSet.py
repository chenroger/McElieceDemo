#!/usr/bin/python3
import argparse
import sympy
import gzip
import pickle
import itertools
def crack(cFile, pubFile):
    with gzip.open(cFile, 'rb') as f:
        cipher = pickle.loads(f.read())
    with gzip.open(pubFile, 'rb') as f:
        G_pub, t_val = pickle.loads(f.read())
    if args.v:
        print('ciphers = ')
        sympy.pprint(cipher)
        print('\nG_pub = ')
        sympy.pprint(G_pub)
        print('t =', t_val)
    col = list(range(G_pub.shape[1]))
    k_val = G_pub.shape[0]
    cracked = []
    for c in cipher:
        cracked.append(itercol(c, G_pub, t_val))
    with gzip.open(args.o, 'wb') as f:
        f.write(pickle.dumps(cracked))
def itercol(c, G_pub, t_val):
    n_val = G_pub.shape[1]
    k_val = G_pub.shape[0]
    col = list(reversed(range(n_val)))
    dict = {}
    threshold = sympy.binomial(n_val, k_val) / 7
    for col_comb in itertools.combinations(col, n_val-k_val):
        G_copy = G_pub[:,:]
        c_copy = c[:,:]
        for col in col_comb:
            c_copy.col_del(col)
            G_copy.col_del(col)
        if G_copy.det() % 2:
            try:
                G_inv = (G_copy**-1).applyfunc(lambda x: mod(x,2))
                m = (c_copy * G_inv).applyfunc(lambda x: mod(x,2))
                dict[str(m)] = dict.setdefault(str(m), 0) + 1
                code = (m * G_pub).applyfunc(lambda x: mod(x,2))
                delta = (code - c).applyfunc(lambda x: mod(x,2))
                hd = (delta * sympy.Matrix([1] * delta.shape[1]))[0]
                if hd <= t_val:
                    if args.v: sympy.pprint(m)
                    return m
            except:
                pass
def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    if denom % modulus == 0:
        denom = int(denom/modulus)
    try:
        return numer*sympy.mod_inverse(denom,modulus) % modulus
    except:
        raise ValueError('Unable to apply modulus to matrix')
        exit()
parser = argparse.ArgumentParser()
parser.add_argument("-v", help="Enable verbose mode", action="store_true")
parser.add_argument("-c", type=str,
					help="File with data in matrices to crack")
parser.add_argument("-o", type=str, help="Output file")
parser.add_argument("-pub", type=str, help="Public Key")
args = parser.parse_args()
if args.c and args.pub:
    crack(args.c, args.pub)