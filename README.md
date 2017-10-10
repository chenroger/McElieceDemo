This is a demonstration of the McEliece cryptosystem and some simple attacks on it.

I am not a cryptographer, this is for academic purposes only. Use at your own risk.

This set of code includes implementations of:
-McEliece cryptosystem
-Sidelnikov cryptosystem
-Simple chosen ciphertext attack
-Simple information set decoding attack


Example commands for using the McEliece cryptosystem:

./McEliece.py -g -m 4 -t 2 -o m4t2 -v

./MatrixCodec.py -e 'Hello world' -k 6 -v -o plain

./McEliece.py -v -e plain -pub m4t2.mecspub -o cipher

./McEliece.py -v -d cipher.mecsc -priv m4t2.mecspriv -o plain

./MatrixCodec.py -d plain.mecsm -v


Example commands for using the Sidelnikov cryptosystem:

./Sidelnikov.py -vv -g -r 2 -m 4 -o r2m4

./MatrixCodec.py -e 'Hello world' -k 11 -v -o plain

./Sidelnikov.py -v -e plain -pub r2m4.scspub -o cipher

./Sidelnikov.py -v -d cipher.scsc -priv r2m4.scspriv -o plain

./MatrixCodec.py -d plain.scsm -v


Example commands for using the chosen ciphertext attack:

./CCADelta.py 'Send $200 to 1234 from XXXX' 'Send $999 to 4321 from XXXX' -k 6 -o delta -v

./McEliece.py -v -e delta -pub m4t2.mecspub -o delta -f

./MatrixCodec.py -e 'Send $200 to 1234 from 5678' -k 6 -v -o intercepted

./McEliece.py -v -e intercepted -pub m4t2.mecspub -o intercepted

./CCAApply.py delta.mecsc intercepted.mecsc -v -o result.mecsc

./McEliece.py -v -d result.mecsc -priv m4t2.mecspriv -o result

./MatrixCodec.py -d result.mecsm -v


Example commands for using the information set decoding attack:

./MatrixCodec.py -e "Success!" -k 6 -v -o secret

./McEliece.py -e secret -pub m4t2.mecspub -o secret -v

./InfoSet.py -v -c secret.mecsc -pub m4t2.mecspub -o attack

./MatrixCodec.py -d attack -v
