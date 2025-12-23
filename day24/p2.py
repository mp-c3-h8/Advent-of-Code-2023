import os.path
import numpy as np
from scipy.optimize import root

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()


OFFSET = 320595954009642
OFFSET2 = 1

A = np.zeros((9, 9))
A[0:3, 0:3] = np.eye(3)
A[3:6, 0:3] = np.eye(3)
A[6:9, 0:3] = np.eye(3) 

B = np.array([0]*9)

for i, line in enumerate(data[-3:]):
    pos, vel = line.split(' @ ')
    b = [*map(int, pos.split(','))]
    v = [*map(int, vel.split(','))]
    A[3*i:3*(i+1), 3+i:4+i] = -1 * np.array(v, ndmin=2).T
    B[3*i:3*(i+1)] = b - np.array([OFFSET]*3)


def fun(x):
    res = A @ x - B
    t1 = x[3] * x[6:]
    t2 = x[4] * x[6:]
    t3 = x[5] * x[6:]
    C = np.hstack((t1, t2, t3))
    res += C
    return res


x0 = np.array([1]*9) * OFFSET
ans = root(fun, x0, method='lm')
res = ans.x
res[:3] = res[:3] + np.array([1]*3) * OFFSET
print(ans)
print(res)
# doesnt work...
