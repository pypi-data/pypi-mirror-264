import numpy as np
import unittest

from galois import Field, Poly
from galois.typing import ArrayLike, ElementLike

class ShamirSharer:
    abscissas: ArrayLike
    """List of field elements that form the abscissas."""
    field: Field
    """The finite field where the elements live in."""
    threshold: int
    """The security threshold."""
    lagrange_coefficients: ArrayLike
    """The lagrange coefficients for interpolation."""

    def __init__(self, abscissas: ArrayLike, field: Field, threshold: int) -> None:
        """Creates a new Lagrange polynomial expression, O(n^2).

        Parameters:
            abscissas (ArrayLike): List of field elements that form the abscissas.
            field (Field): The finite field where the elements live in.
            threshold (int): The security threshold.
        """
        self.field = field
        self.abscissas = field(abscissas)
        self.threshold = threshold
        coefs = []
        w = field(0)
        for i, xi in enumerate(self.abscissas):
            wi = field(1)
            for j, xj in enumerate(self.abscissas):
                if j != i:
                    wi *= (xi - xj)
            ci = -xi**(-1) * wi**(-1)
            w += ci
            coefs.append(ci)
        self.lagrange_coefficients = field(coefs) * w**(-1)

    def single_share(self, secret: ElementLike, twice: bool=False) -> ArrayLike:
        """Shamir share secret using a random polynomial.

        Parameters:
            secret (ElementLike): The secret value to be shared.
            twice (bool): Whether to share the secret at twice the threshold.

        Returns:
            shares (ArrayLike): Array of shares.
        """
        degree = (twice + 1) * self.threshold
        poly = Poly(np.concatenate(([secret], self.field.Random(degree))), self.field, order="asc")
        shares = poly(self.abscissas)
        return shares

    def single_recover(self, shares: ArrayLike) -> ElementLike:
        """Lagrange interpolation at Zero, O(n).

        Parameters:
            shares (ArrayLike): Sorted list of shares from every node.

        Returns:
            secret (ElementLike): Recovered secret value.
        """
        secret = np.sum(self.lagrange_coefficients * self.field(shares))
        return secret

    def share(self, secrets: ArrayLike, twice: bool=False) -> ArrayLike:
        """Batch Shamir share secret using random polynomials.

        Parameters:
            secret (ArrayLike): The secret values to be shared.
            twice (bool): Whether to share the secrets at twice the threshold.

        Returns:
            shares (ArrayLike): Array of shares.
        """
        shares = []
        for secret in secrets:
            s = self.single_share(secret, twice)
            shares.append(s)
        return np.transpose(self.field(shares))

    def recover(self, shares: ArrayLike) -> ArrayLike:
        """Batch recover secrets.

        Parameters:
            shares (ArrayLike): Sorted list of shares from every node.

        Returns:
            secret (ArrayLike): Recovered secret values.
        """
        secrets = []
        for subshares in np.transpose(shares):
            secret = self.single_recover(subshares)
            secrets.append(secret)
        return secrets

class TestUtils(unittest.TestCase):
    
    def setUp(self): 
        np.random.seed(0)

    def test_share_recover_secret(self):
        GF = Field(227)
        sharer = ShamirSharer([1, 2, 3, 4, 5], GF, 2)
        secret = 7
        shares = sharer.single_share(secret)
        result = sharer.single_recover(shares)
        self.assertEqual(result, secret)

    def test_batch_share_recover(self):
        GF = Field(227)
        sharer = ShamirSharer([1, 2, 3, 4, 5], GF, 3)
        secrets = [7, 3, 5]
        shares = sharer.share(secrets)
        results = sharer.recover(shares)
        self.assertEqual(results, secrets)

    def test_share_recover_secret_two_t(self):
        GF = Field(227)
        sharer = ShamirSharer([1, 2, 3, 4, 5], GF, 2)
        secret = 7
        shares = sharer.single_share(secret, twice=True)
        result = sharer.single_recover(shares)
        self.assertEqual(result, secret)

    def test_fail_share_recover_secret(self):
        GF = Field(227)
        sharer = ShamirSharer([1, 2, 3, 4, 5], GF, 5)
        secret = 7
        shares = sharer.single_share(secret)
        result = sharer.single_recover(shares)
        self.assertNotEqual(result, secret)

    def test_fail_share_recover_secret_two_t(self):
        GF = Field(227)
        sharer = ShamirSharer([1, 2, 3, 4, 5], GF, 3)
        secret = 7
        shares = sharer.single_share(secret, twice=True)
        result = sharer.single_recover(shares)
        self.assertNotEqual(result, secret)

if __name__ == "__main__":
    unittest.main()
