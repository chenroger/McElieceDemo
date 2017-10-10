#!/usr/bin/python3
import argparse
import sympy
import gzip
import pickle
# From https://stackoverflow.com/questions/31190182/sympy-solving-matrices
# -in-a-finite-field
def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    try:
        return numer*sympy.mod_inverse(denom,modulus) % modulus
    except:
        print('Error: Unable to apply modulus to matrix')
        exit()
def applyDelta(a_matrices, b_matrices):
    c_matrices = []
    if args.v: print('\nResult:')
    for i in range(len(a_matrices)):
        current = (a_matrices[i] + b_matrices[i]).applyfunc(
        										  lambda x: mod(x,2))
        c_matrices.append(current)
        if args.v: sympy.pprint(current)
    if args.o:
        with gzip.open(args.o, 'wb') as f:
            f.write(pickle.dumps(c_matrices))
parser = argparse.ArgumentParser()
parser.add_argument('strings', metavar='Input', type=str, nargs='+',
					help='Files to add the ciphertexts of')
parser.add_argument("-v", help="Enable verbose mode", action="store_true")
parser.add_argument("-o", type=str, help="File to store output")
args = parser.parse_args()
if not len(args.strings) == 2:
    print('Include two strings to process.')
    print(parser.format_help())
    exit()
with gzip.open(args.strings[0], 'rb') as f:
    a_matrices = pickle.loads(f.read())
with gzip.open(args.strings[1], 'rb') as f:
    b_matrices = pickle.loads(f.read())
if not len(a_matrices) == len(b_matrices):
    print('Number of matrices do not match')
    exit()
applyDelta(a_matrices, b_matrices)