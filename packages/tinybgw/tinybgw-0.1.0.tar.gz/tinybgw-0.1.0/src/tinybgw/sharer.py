import numpy as np
import unittest

from galois import Field
from galois.typing import ArrayLike
from typing import Dict, List, Tuple

from .combinations import combinations

class SecretSharer:
    field: Field
    """The finite field where the elements live in."""
    size: int
    """The number of parties."""
    threshold: int
    """The security threshold."""

    def __init__(self, field: Field, size: int, threshold: int=None) -> None:
        """Initializes Replicated Sharer.

        Parameters:
            field (Field): The finite field where the elements live in.
            size (int): The number of parties.
            threshold (int): The security threshold.
        """
        self.field = field
        self.size = size
        self.threshold = threshold

    def share(self, secret: ArrayLike, network_size=None) -> ArrayLike:
        """Additively shares secret.

        Parameters:
            secret (ArrayLike): The secret value to be shared.
            network_size (int): The number of parties.
        
        Returns
            shares (ArrayLike): Array of additive shares.
        """
        if not network_size: network_size = self.size
        n = 1 if type(secret) == int else len(secret)
        shares = self.field.Random((network_size-1, n))
        last = self.field(secret) - np.sum(shares, axis=0)
        shares = np.append(shares, [last], axis=0)
        return shares

    def recover(self, shares: ArrayLike) -> ArrayLike:
        """Additive secret recovery.

        Parameters:
            shares (ArrayLike): Sorted list of shares from every node.

        Returns:
            secret (ArrayLike): Recovered secret value.
        """
        secret = np.sum(self.field(shares), axis=0)
        return secret

    def replicated_share(self, secret: ArrayLike) -> List[Dict[Tuple, ArrayLike]]: 
        """Replicated share secret using a random values.

        Parameters:
            secret (ArrayLike): The secret value to be shared.

        Returns:
            shares (List[Dict[Tuple, ArrayLike]]): Array of shares.
        """
        subsets = combinations(self.size, self.threshold)
        shared = self.share(secret, len(subsets))
        shares = []
        for i in range(1, self.size+1):
            subshares = {}
            for subset, s in zip(subsets, shared):
                if i in subset: subshares[tuple(subset)] = s
            shares.append(subshares)
        return shares 

class TestUtils(unittest.TestCase):
    
    def setUp(self): 
        np.random.seed(0)

    def test_share_recover_secret(self):
        GF = Field(13)
        sharer = SecretSharer(GF, 5)
        secret = 7
        shares = sharer.share(secret)
        result = sharer.recover(shares)
        self.assertEqual(result, secret)

    def test_batch_share_recover_secret(self):
        GF = Field(13)
        sharer = SecretSharer(GF, 5)
        secret = GF([1, 2, 3])
        shares = sharer.share(secret)
        result = sharer.recover(shares)
        self.assertEqual(list(result), list(secret))

if __name__ == "__main__":
    unittest.main()