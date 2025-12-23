import os.path
import numpy as np
from itertools import combinations

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

# 273084618253552, 382626888261135, 273689280998585 @ 8, -157, 17
# 221456980555537, 346760891427937, 198873039052710 @ 8, -111, -48
# 235317931818252, 321016228988431, 221782559196323 @ 8, -29, -24


P, V = [], []
for line in data:
    pos, vel = line.split(' @ ')
    p = np.array([*map(int, pos.split(','))])
    v = np.array([*map(int, vel.split(','))])
    # if int(v[0]) != 8:
    #     continue
    P.append(p)
    V.append(v)

# we are sitting on p0
p0, p1, p2 = P[:3]
v0, v1, v2 = V[:3]


p1_rel = p1-p0
p2_rel = p2-p0
v1_rel = v1-v0
v2_rel = v2-v0

t1_nom = -np.cross(p1_rel, p2_rel).dot(v2_rel)
t1_denom = np.cross(v1_rel, p2_rel).dot(v2_rel)
t1 = t1_nom / t1_denom
t2 = -np.cross(p1_rel, p2_rel).dot(v1_rel) / np.cross(p1_rel, v2_rel).dot(v1_rel)

# crossings
c1 = p1 + t1*v1
c2 = p2 + t2*v2

v = (c2-c1)/(t2-t1)
p = c1 - t1*v

print(sum(p))
# rounding errors
