#!/usr/bin/env python3

from sympy.abc import x, y
from qldpc import codes

# the [[90, 8, 10]] code from arXiv:2308.07915
dims = (15, 3)
poly_a = x**9 + y + y**2
poly_b = 1 + x**2 + x**7


code = codes.QCCode(dims, poly_a, poly_b)
print("code parameters:", code.get_code_params(bound=10))

toric_mappings = code.get_toric_mappings()
for plaquette_map, torus_shape in toric_mappings:
    shifts_x, shifts_z = code.get_check_shifts(plaquette_map, torus_shape)
    print()
    print("torus shape:", torus_shape)
    print(shifts_x)
    print(shifts_z)
