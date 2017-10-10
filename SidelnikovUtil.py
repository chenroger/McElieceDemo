#!/usr/bin/python3
import argparse
import gzip
import pickle

def writeCipher(output, filename):
    with gzip.open(filename + '.scsc', 'wb') as f:
        f.write(pickle.dumps(output))
def writePlain(output, filename):
    with gzip.open(filename + '.scsm', 'wb') as f:
        f.write(pickle.dumps(output))
def readFromFile(filename):
    with gzip.open(filename, 'rb') as f:
        contents = pickle.loads(f.read())
    return contents
def writeKeys(G_matrix, t_val, S_matrix, H_matrix, P_matrix, filename):
    with gzip.open(filename + '.scspub', 'wb') as f:
        f.write(pickle.dumps([G_matrix, t_val]))
    with gzip.open(filename + '.scspriv', 'wb') as f:
        f.write(pickle.dumps([S_matrix, H_matrix, P_matrix, t_val]))
parser = argparse.ArgumentParser()
parser.add_argument("-v", help="Enable verbose mode", action="store_true")
parser.add_argument("-vv", help="Enable very verbose mode",
					action="store_true")
parser.add_argument("-g", help="Generate key pairs", action="store_true")
parser.add_argument("-r", type=int, help="Generate key pairs")
parser.add_argument("-m", type=int, help="Generate key pairs")
parser.add_argument("-o", type=str, help="Output file (always needed)")
parser.add_argument("-e", type=str,
					help="File with data in matrices to encrypt")
parser.add_argument("-d", type=str,
					help="File with data in matrices to decrypt")
parser.add_argument("-pub", type=str, help="Key to encrypt with")
parser.add_argument("-priv", type=str, help="Key to decrypt with")
parser.add_argument("-f",
					help="Encrypt without errors in ciphertext", action="store_true")
args = parser.parse_args()