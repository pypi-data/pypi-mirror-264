import math
import numpy as np

def dct(x: np.array, M):
    N = len(x)
    DCT = []
    for i in range(1, M+1):
        DK = 1 if i==1 else 0         
        summation = sum(x[n] * (1/math.sqrt(1+DK)) * math.cos((math.pi*(2*n-1)*(i-1))/(2*N)) for n in range(N))
        DCT.append(math.sqrt(2/N) * summation)

    return DCT