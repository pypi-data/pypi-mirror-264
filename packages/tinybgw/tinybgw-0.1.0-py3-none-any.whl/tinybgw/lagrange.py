import unittest

from galois import Field, Poly
from galois.typing import ArrayLike
from typing import List


def _polynomials(abscissas: ArrayLike, field: Field) -> None:
    """Create the lagrange polynomials given the abscissas.

    Parameters:
        abscissas (ArrayLike): List of field elements that form the abscissas.
        field (Field): The finite field that the elements live in.
    """
    abscissas = field(abscissas)
    polys = []
    for i, xi in enumerate(abscissas):
        numerator = Poly(field([1]), order="asc")
        denominator = field(1)
        for j, xj in enumerate(abscissas):
            if i == j: continue
            numerator   = numerator * Poly(field([-xj, 1]), order="asc")
            denominator = denominator * (xi - xj)
        poly = numerator * denominator**(-1)
        polys.append(poly)
    return polys

def lagrange_interpolation(abscissas: ArrayLike, ordinates: ArrayLike, field: Field) -> Poly:
    """Build the polynomial which the ordinates came from.

    Parameters:
        abscissas (ArrayLike): List of field elements that form the abscissas.
        ordinates (ArrayLike): List of field elements that form the ordinates.
        field (Field): The finite field that the elements live in.

    Returns:
        poly (Poly): The polynomial that ordinates came from.
    """
    polys = _polynomials(abscissas, field)
    poly = Poly(field(0), order="asc")
    ordinates = field(ordinates)
    for i in range(len(ordinates)):
        term = polys[i] * ordinates[i]
        poly = poly + term
    return poly

class TestUtils(unittest.TestCase):

    def test_polynomials(self):
        field = Field(227)
        polys = _polynomials([1, 2, 3], field)
        expected = [
            Poly([3, 111, 114], field, order="asc"),
            Poly([224, 4, 226], field, order="asc"),
            Poly([1, 112, 114], field, order="asc"),
        ]
        self.assertEqual(polys, expected)

    def test_interpolation(self):
        field = Field(227)
        p = lagrange_interpolation([0, 1, 2, 3, 4], [1, 0, 0, 0, 0], field)
        expected = Poly([1, 206, 219, 132, 123], field, order="asc")
        self.assertEqual(p, expected)

if __name__ == "__main__":
    unittest.main()
