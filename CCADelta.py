#!/usr/bin/python3
import argparse
import sympy
import gzip
import pickle
def encode(text, k_val):
    output = []
    current = sympy.Matrix()
    for c in text:
        ascii_val = ord(c)
        for i in range(6, -1, -1):
            if current.shape[1] == k_val:
                output.append(current)
                current = sympy.Matrix()
            bit = pow(2, i)
            if ascii_val >= bit:
                ascii_val -= bit
                if current.shape[1] == 0:
                    current = sympy.Matrix([1])
                else:
                    current = current.col_insert(current.shape[1],
                    							 sympy.Matrix([1]))
            else:
                if current.shape[1] == 0:
                    current = sympy.Matrix([0])
                else:
                    current = current.col_insert(current.shape[1],
                    							 sympy.Matrix([0]))
    nonempty = current.shape[1]
    final = sympy.Matrix([0] * k_val).T
    if not nonempty == k_val:
        current = current.row_join(sympy.Matrix([0] * (k_val - nonempty)).T)
    output.append(current)
    output.append(final)
    if args.v: print(text); sympy.pprint(output)
    return output
# From https://stackoverflow.com/questions/31190182/sympy-solving-matrices
# -in-a-finite-field
def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    try:
        return numer*sympy.mod_inverse(denom,modulus) % modulus
    except:
        print('Error: Unable to apply modulus to matrix')
        exit()
def findDelta():
    a_str, b_str = args.strings
    a_matrices = encode(a_str, args.k)
    b_matrices = encode(b_str, args.k)
    delta_matrices = []
    if args.v: print('\nDelta:')
    for i in range(len(a_matrices)):
        current = (a_matrices[i] + b_matrices[i]).applyfunc(
        										  lambda x: mod(x,2))
        delta_matrices.append(current)
        if args.v: sympy.pprint(current)
    if args.o:
        with gzip.open(args.o, 'wb') as f:
            f.write(pickle.dumps(delta_matrices))
parser = argparse.ArgumentParser()
parser.add_argument('strings', metavar='Input', type=str, nargs='+',
					help='strings to find the difference between')
parser.add_argument("-k", type=int, help="Length of each matrix")
parser.add_argument("-v", help="Enable verbose mode", action="store_true")
parser.add_argument("-o", type=str, help="File to store output")
args = parser.parse_args()
if not len(args.strings) == 2:
    print('Include two strings to process.')
    print(parser.format_help())
    exit()
elif not len(args.strings[0]) == len(args.strings[1]):
    print('Strings not equal length')
    print(parser.format_help())
    exit()
elif args.k:
    findDelta()
else:
    print(parser.format_help())