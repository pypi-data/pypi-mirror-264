# Contract 2

import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))

from heartbreak import *

A = Site(1)

calculate = RF("calculate", A)
secret_a = 10

res = calculate(arg1=secret_a, arg2=secret_a)

sum = res['sum']
print(res)
print(sum)