import numpy as np
import random
import unittest

from dataclasses import dataclass, field
from galois import Field, Poly
from galois.typing import ArrayLike, ElementLike
from typing import Dict, Tuple

from .lagrange import lagrange_interpolation
from .node import Node
from .shamir import ShamirSharer

@dataclass
class PseudoRandom:
    """Data needed for pseudo random share generation."""

    shares: Dict[Tuple[int], ElementLike]
    """Share"""
    count: int = 0
    """The state count."""

class PseudoNode(Node):
    """ Represents a node in the network."""

    ps_rand: PseudoRandom
    """Data to create pseudo random sharings."""
    ps_zero: PseudoRandom
    """Data to create pseudo random sharings of zero."""

    def __init__(self, id: int, network_size: int, threshold: int, field: Field, 
                 ps_share: Dict[Tuple[int], ElementLike]=None,
                 ps_zero_share: Dict[Tuple[int], ElementLike]=None) -> None:
        """Initialize the node.
        
        Parameters:
            id (int): The id of the Node, also used as its abscissa.
            network_size (int): The number of nodes in the network.
            threshold (int): The security threshold of the network.
            field (Field): The finite field that the shares live in.
            zero_share (Dict[Tuple[int], ElementLike]): Share to create pseudo random zero sharings.
        """
        self.id = id
        self.network_size = network_size
        self.field = field
        self.shares_db = {}
        self.open_db = {}
        self.sharer = ShamirSharer([i+1 for i in range(network_size)], field, threshold)
        if ps_share:
            self.ps_rand = PseudoRandom(ps_share)
        if ps_zero_share:
            self.ps_zero = PseudoRandom(ps_zero_share)

    def next_rand(self, batch_size: int) -> ArrayLike:
        """Generate a pseudo random share with random value.

        `Cramer et al <https://iacr.org/archive/tcc2005/3378_342/3378_342.pdf.>`_

        Parameters:
            batch_size (int): The number of random shares to create.
        Returns:
            share (ArrayLike): Share of a random value.
        """
        all = set(range(1, self.network_size+1))
        share = self.field(0)
        for subset in self.ps_rand.shares:
            diff = list(all - set(subset))
            poly = lagrange_interpolation([0] + diff, [1]+[0]*len(diff), self.field)
            f_A = poly(self.id)
            r_A = int(self.ps_rand.shares[subset][0])
            random.seed(r_A + self.ps_rand.count)
            rand = self.field([random.randrange(0, self.field.order) for _ in range(batch_size)])
            share = (share + rand * f_A)
        self.ps_rand.count += 1
        return share

    def next_zero(self, batch_size: int) -> ArrayLike:
        """Generate a pseudo random share with zero value.
        
        `Cramer et al <https://iacr.org/archive/tcc2005/3378_342/3378_342.pdf.>`_

        Parameters:
            batch_size (int): The number of random shares to create.
        Returns:
            share (ArrayLike): Share of a random value.
        """
        N = self.network_size
        T = self.sharer.threshold
        all = set(range(1, self.network_size+1))
        share = self.field(0)
        for subset in self.ps_zero.shares:
            diff = list(all - set(subset))
            for i, subset_share in enumerate(self.ps_zero.shares[subset], 1):
                poly = lagrange_interpolation(
                        [0] + diff + [k for k in range(N+1, N+T+1)],
                        [0] + [0]*len(diff) + [1]*i + [0]*(T-i),
                        self.field)
                f_A = poly(self.id)
                r_A = int(subset_share)
                random.seed(r_A + self.ps_zero.count)
                rand = self.field([random.randrange(0, self.field.order) for _ in range(batch_size)])
                share = (share + rand * f_A)
        self.ps_zero.count += 1
        return share

class TestUtils(unittest.TestCase):
    def setUp(self): 
        np.random.seed(0)

    def test_set_get_secret(self):
        N = 3; T = 1; field = Field(13)
        node = Node(1, N, T, field)
        node.set_share(2, "secret_2")
        result = node.pop_share("secret_2")
        self.assertEqual(result, 2)
        
if __name__ == "__main__":
    unittest.main()