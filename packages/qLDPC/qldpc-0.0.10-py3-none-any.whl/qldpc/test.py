#!/usr/bin/env python3
import numpy as np
from sympy.abc import x, y
from qldpc import codes

# codes from Table 3 of arXiv:2308.07915

for dims, poly_a, poly_b in [
    ([6, 6], x**3 + y + y**2, y**3 + x + x**2),
    ([15, 3], x**9 + y + y**2, 1 + x**2 + x**7),
    ([9, 6], x**3 + y + y**2, y**3 + x + x**2),
    ([12, 6], x**3 + y + y**2, y**3 + x + x**2),
    ([12, 12], x**3 + y**2 + y**7, y**3 + x + x**2),
    ([30, 6], x**9 + y + y**2, y**3 + x**25 + x**2),
    ([21, 18], x**3 + y**10 + y**17, y**5 + x**3 + x**19),
]:

    code = codes.QCCode(dims, poly_a, poly_b)
    max_dist = 0

    print("----------------------")
    print(f"code parameters: ({code.num_qubits}, {code.dimension})")

    max_distances = []

    toric_mappings = code.get_toric_mappings()
    for ll, (plaquette_map, torus_shape) in enumerate(toric_mappings):
        shifts_x, shifts_z = code.get_check_shifts(plaquette_map, torus_shape, open_boundaries=True)
        shifts_xz = shifts_x | shifts_z

        distances = set(np.sqrt(xx**2 + yy**2) for xx, yy in shifts_xz)
        max_distances.append(max(distances))

    min_max_distance = min(max_distances)
    print(f"maximum distance required: {min_max_distance:.1f}")
