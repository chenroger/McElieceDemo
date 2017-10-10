#!/usr/bin/python3
import itertools
from McElieceKeygen import *
def get_dist(a_matrix, b_matrix):
    diff_matrix = (a_matrix + b_matrix).applyfunc(lambda x: mod(x,2))
    dist = (diff_matrix * sympy.Matrix([1] * diff_matrix.shape[1]))[0]
    return dist
def encrypt(mfile, pubkey, outfile):
    G_pub, t_val = readFromFile(pubkey)
    message = readFromFile(mfile)
    cipher = []
    for m in message:
        if args.v: print(sympy.pretty(m), end=' -> ')
        c = (m * G_pub).applyfunc(lambda x: mod(x,2))
        if not args.f:
            errors = []
            for i in range(t_val):
                inlist = True
                while inlist:
                    pos = random.randrange(G_pub.shape[1])
                    if not pos in errors:
                        inlist = False
                        errors.append(pos)
            for e in errors:
                if c[e] == 0:
                    c[e] = 1
                else:
                    c[e] = 0
        if(args.v): sympy.pprint(c)
        cipher.append(c)
    writeCipher(cipher, outfile)
def decrypt(cfile, privkey, outfile):
    S_matrix, H_matrix, P_matrix, t_val = readFromFile(privkey)
    k_val = H_matrix.shape[0]
    n_val = H_matrix.shape[1]
    S_inverse = (S_matrix**-1).applyfunc(lambda x: mod(x,2))
    P_inverse = (P_matrix**-1).applyfunc(lambda x: mod(x,2))
    cipher = readFromFile(cfile)
    errors_tbit = []
    numbers = []
    for i in range(H_matrix.shape[1]):
        numbers.append(i)
    # Generate t-bit errors and syndromes
    for bits in itertools.combinations(numbers, t_val):
        et = sympy.zeros(1, H_matrix.shape[1])
        for bit in bits:
            et[bit] = 1
        st = (et * H_matrix.T).applyfunc(lambda x: mod(x,2))
        errors_tbit.append([et, st])
    message = []
    s_zeros = sympy.zeros(1,H_matrix[0])
    for c in cipher:
        print(sympy.pretty(c), end=' -> ')
        mSG = (c * P_inverse).applyfunc(lambda x: mod(x,2))
        s_mSG = (mSG * H_matrix.T).applyfunc(lambda x: mod(x,2))
        if not args.f:
            for errors in errors_tbit:
                if errors[1] == s_mSG:
                    recover = (mSG + errors[0]).applyfunc(lambda x: mod(x,2))
                    s_recover = (recover * H_matrix.T).applyfunc(
                    								   lambda x: mod(x,2))
                    mSG = recover
        mS = mSG.extract([0], list(range(k_val, n_val)))
        m = (mS *S_inverse).applyfunc(lambda x: mod(x,2))
        if(args.v): sympy.pprint(m)
        message.append(m)
    writePlain(message, outfile)
if args.vv:
    args.v = True
if args.g and args.m and args.t and args.o:
    keygen(args.m, args.t, args.o)
elif args.e and args.pub and args.o:
    encrypt(args.e, args.pub, args.o)
elif args.d and args.priv and args.o:
    decrypt(args.d, args.priv, args.o)
else:
    print(parser.format_help())