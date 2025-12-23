import os.path
from sympy import Symbol
from sympy import symbols
from sympy import solve_poly_system

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

P = []
V = []
for line in data[:3]:
    pos, vel = line.split(' @ ')
    p = [*map(int, pos.split(','))]
    v = [*map(int, vel.split(','))]
    P.append(p)
    V.append(v)


unknown = x, y, z, vx, vy, vz = symbols('x y z vx vy vz')
equations = []
ts = []

for i, (p, u) in enumerate(zip(P, V)):
    (px, py, pz) = p
    (ux, uy, uz) = u
    t = Symbol('t'+str(i))
    eqx = x + vx*t - px - ux*t
    eqy = y + vy*t - py - uy*t
    eqz = z + vz*t - pz - uz*t

    equations.extend([eqx, eqy, eqz])
    ts.append(t)

res = solve_poly_system(equations, list(unknown)+ts)

if res:
    print('Part2:', sum(p for p in res[0][:3]))
