import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))

from motif import *
def main():
    A = Site(1)
    B = Site(2)

    secret_a = private_data(name='secret_a', site=A)
    secret_b = private_data(name='secret_b', site=B)

    result = secret_a.at(A) + secret_b.at(A)

    print(result.evaluate())

main()
