
from heartbreak import *

A = Site(1)

get_int = RF('get_int', A)
calculate = RF('calculate', A)

int_a = get_int()

result = calculate(arg1=int_a, arg2=1)
res_sum = result['sum']
res_dif = result['dif']
print(res_sum, res_dif)

