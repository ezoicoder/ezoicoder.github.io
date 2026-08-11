#!/usr/bin/env python3
"""Verify the three-state obstruction to original block aperiodicity.

This script is intentionally finite.  On three states there are only 3^3 = 27
transformations.  It enumerates all aperiodic submonoids of this finite
transformation monoid, keeps the maximal ones under inclusion, and verifies a
real-spectrum certificate for each maximal class.
"""

from itertools import permutations, product
from fractions import Fraction


N = 3
MAPS = list(product(range(N), repeat=N))
INDEX = {mapping: i for i, mapping in enumerate(MAPS)}
IDENTITY = INDEX[tuple(range(N))]
V = ((1, 0, 0), (1, 1, 0), (1, 0, 1))
V_INVERSE = ((1, 0, 0), (-1, 1, 0), (-1, 0, 1))


def compose(left, right):
    """Return left after right."""
    return tuple(left[right[state]] for state in range(N))


def matrix_product(left, right):
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column] for middle in range(N))
            for column in range(N)
        )
        for row in range(N)
    )


def transformation_matrix(mapping):
    return tuple(
        tuple(int(mapping[row] == column) for column in range(N))
        for row in range(N)
    )


def state_difference_block(census_matrix):
    """Return the lower-right block of V^{-1} M_{tau_bullet} V."""
    transformed = matrix_product(
        matrix_product(V_INVERSE, census_matrix), V
    )
    assert transformed[1][0] == 0 and transformed[2][0] == 0
    return transformed[1][1:], transformed[2][1:]


COMPOSE = [
    [INDEX[compose(left, right)] for right in MAPS]
    for left in MAPS
]


def closure(mask, extra):
    """Close an existing submonoid mask after adding one transformation."""
    mask |= 1 << extra
    elements = [i for i in range(len(MAPS)) if (mask >> i) & 1]
    cursor = 0
    while cursor < len(elements):
        left = elements[cursor]
        cursor += 1
        for right in elements[:]:
            for value in (COMPOSE[left][right], COMPOSE[right][left]):
                if not ((mask >> value) & 1):
                    mask |= 1 << value
                    elements.append(value)
    return mask


def is_aperiodic(mask):
    """A finite transformation monoid is aperiodic iff powers stabilize."""
    elements = [i for i in range(len(MAPS)) if (mask >> i) & 1]
    for value in elements:
        power = IDENTITY
        for _ in range(len(elements) + 1):
            next_power = COMPOSE[power][value]
            if next_power == power:
                break
            power = next_power
        else:
            return False
    return True


def enumerate_aperiodic_monoids():
    """Enumerate all aperiodic submonoids of the three-point full monoid."""
    seen = {1 << IDENTITY}
    pending = list(seen)
    while pending:
        mask = pending.pop()
        for value in range(len(MAPS)):
            if (mask >> value) & 1:
                continue
            candidate = closure(mask, value)
            if candidate not in seen and is_aperiodic(candidate):
                seen.add(candidate)
                pending.append(candidate)
    return seen


def conjugate(mapping, permutation):
    inverse = [0] * N
    for state, image in enumerate(permutation):
        inverse[image] = state
    return tuple(permutation[mapping[inverse[state]]] for state in range(N))


def mask_of(mappings):
    return sum(1 << INDEX[mapping] for mapping in mappings)


# Representatives for the three conjugacy classes of maximal aperiodic
# submonoids of the three-point transformation monoid.
REPRESENTATIVES = (
    {
        (0, 0, 0), (0, 0, 2), (0, 1, 0), (0, 1, 2), (1, 1, 0),
        (1, 1, 1), (1, 1, 2), (2, 0, 2), (2, 1, 2), (2, 2, 2),
    },
    {
        (0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 1, 2), (1, 1, 0),
        (1, 1, 1), (1, 1, 2), (2, 1, 1), (2, 1, 2), (2, 2, 2),
    },
    {
        (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1),
        (0, 1, 2), (1, 1, 0), (1, 1, 1), (1, 1, 2), (2, 2, 2),
    },
)


def induced_state_difference_matrix(mapping):
    """Return B_tau, the lower-right block of V^{-1} M_tau V.

    Equivalently, this is the matrix on coordinates
    x = v_1 - v_0 and y = v_2 - v_0.
    """
    return state_difference_block(transformation_matrix(mapping))


def determinant(left, right):
    return left[0] * right[1] - left[1] * right[0]


def matrix_vector(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(2))
        for row in range(2)
    )


def in_cone(vector, first_ray, second_ray):
    return vector == (0, 0) or (
        determinant(first_ray, vector) >= 0
        and determinant(vector, second_ray) >= 0
    )


def verify_maximal_classification():
    monoids = enumerate_aperiodic_monoids()
    maximal = []
    for mask in sorted(monoids, key=int.bit_count, reverse=True):
        if not any(mask != other and mask & ~other == 0 for other in maximal):
            maximal.append(mask)

    expected_maximal = set()
    for representative in REPRESENTATIVES:
        for permutation in permutations(range(N)):
            expected_maximal.add(
                mask_of(conjugate(mapping, permutation)
                        for mapping in representative)
            )

    assert len(monoids) == 401
    assert len(maximal) == 9
    assert {mask.bit_count() for mask in maximal} == {10}
    assert set(maximal) == expected_maximal


def verify_real_spectrum_certificates():
    """Verify certificates inherited by every nonnegative integer sum.

    For every transformation tau, induced_state_difference_matrix returns B_tau.
    For the first two maximal classes, every B_tau preserves a common proper
    cone. In the cone basis, B_{tau_bullet} = sum_u B_{tau_u} has nonnegative
    entries, hence real eigenvalues.

    For the third maximal class, every B_tau is triangular in the displayed
    coordinates, and B_{tau_bullet} remains triangular.
    """
    cones = (((0, -1), (1, 0)), ((0, -1), (1, 1)))
    for representative, (first_ray, second_ray) in zip(REPRESENTATIVES[:2], cones):
        assert determinant(first_ray, second_ray) > 0
        for mapping in representative:
            matrix = induced_state_difference_matrix(mapping)
            assert in_cone(matrix_vector(matrix, first_ray), first_ray, second_ray)
            assert in_cone(matrix_vector(matrix, second_ray), first_ray, second_ray)

    for mapping in REPRESENTATIVES[2]:
        assert induced_state_difference_matrix(mapping)[0][1] == 0


def verify_counterexample_spectrum():
    """Verify the spectrum obstruction for the transition-count matrix T."""
    transition = ((1, 0, 1), (2, 0, 0), (0, 2, 0))
    block = state_difference_block(transition)
    assert block == ((0, -1), (2, -1))

    # chi_{B_T}(lambda) = lambda^2 + lambda + 2.
    trace = block[0][0] + block[1][1]
    determinant_2 = block[0][0] * block[1][1] - block[0][1] * block[1][0]
    assert (trace, determinant_2) == (-1, 2)

    # The nontrivial eigenvalues are (-1 +- i sqrt(7)) / 2.  Their ratio has
    # real part -3/4.  A root of unity in a quadratic extension has order
    # 1, 2, 3, 4, or 6, so its real part is one of the following values.
    # Hence no positive power makes both nontrivial eigenvalues real.
    possible_degree_two_root_real_parts = {
        Fraction(1), Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(-1, 2)
    }
    assert Fraction(-3, 4) not in possible_degree_two_root_real_parts


def main():
    verify_maximal_classification()
    verify_real_spectrum_certificates()
    verify_counterexample_spectrum()
    print("aperiodic submonoids of the three-point transformation monoid: 401")
    print("maximal aperiodic submonoids: 9, in three conjugacy classes")
    print("each maximal class has a real-spectrum certificate")
    print("the transition-count matrix T has a non-real eigenvalue")
    print("therefore no original-state aperiodic block census realizes T^b")


if __name__ == "__main__":
    main()
