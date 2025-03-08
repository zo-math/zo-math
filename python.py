import numpy as np
from fractions import Fraction

v = np.random.randn(2000)
# print(v)
u = v / np.linalg.norm(v)
# print(u)

V = np.random.randn(2000,15)
# print(V)
U = V / np.linalg.norm(V, axis=0)
# print(U)

dot_products = np.round(np.abs(np.dot(u,U)),5)
print(dot_products)

average_dot_product = np.mean(dot_products)
print({average_dot_product})

# print({2/np.pi})