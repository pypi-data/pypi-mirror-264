import numpy as np
import unittest

from dataclasses import dataclass, field
from galois import Field, Poly
from galois.typing import ArrayLike, ElementLike
from typing import Dict, Tuple

from .lagrange import lagrange_interpolation
from .shamir import ShamirSharer

@dataclass
class PseudoRandom:
    """Data needed for pseudo random share generation."""

    shares: Dict[Tuple[int], ElementLike]
    """Share"""
    count: int = 0
    """The state count."""

class Node:
    """ Represents a node in the network."""

    id: int
    """Identifier for the node."""
    network_size: int
    """Number of nodes in the network."""
    field: Field
    """The finite field where the elements live in."""
    shares_db: Dict[str, ArrayLike] = field(default_factory=dict) 
    """Database for holding shares."""
    open_db: Dict[str, ArrayLike] = field(default_factory=dict)
    """Database for holding open values."""
    sharer: ShamirSharer
    """Secret sharer that handles secret sharing and recovery."""

    def __init__(self, id: int, network_size: int, threshold: int, field: Field) -> None:
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

    def get_share(self, share_id: str) -> ArrayLike:
        """Retrieve a share from the 'shares_db'.

        Parameters:
            share_id (str): The unique id for the shares of the secret.

        Returns:
            value (ArrayLike): The share value with the share_id.
        """
        return self.shares_db[share_id]

    def get_open(self, open_id: str) -> ArrayLike:
        """Retrieve an open value from the 'open_db'.

        Parameters:
            open_id (str): The unique id for the open value.

        Returns:
            value (ArrayLike): The open value with the open_id.
        """
        return self.open_db[open_id]

    def set_share(self, value: ArrayLike, share_id: str) -> None:
        """Set a share in the 'shares_db'.
       
        Parameters:
            value (ArrayLike): The share value.
            share_id (str): The unique id for the shares of the secret.
        """
        self.shares_db[share_id] = self.field(value)

    def set_open(self, value: ArrayLike,  open_id: str) -> None:
        """Set an open value in the 'open_db'.
       
        Parameters:
            value (ArrayLike): The open value.
            open_id (str): The unique id for the open value. 
        """
        self.open_db[open_id] = self.field(value)

    def pop_share(self, share_id: str) -> ArrayLike:
        """Delete and return a share from the 'shares_db'.
       
        Parameters:
            share_id (str): The unique id for the shares of the secret. 
        
        Returns:
            value (ArrayLike): The share value.
        """
        value = self.shares_db.pop(share_id)
        return value

    def pop_open(self, open_id: str) -> ArrayLike:
        """Delete and return an open value from the 'open_db'.

        Parameters:
            open_id (str): The unique id for the open value. 
        
        Returns:
            value (ArrayLike): The open value.
        """
        value = self.open_db.pop(open_id)
        return value

    def recover(self, shares_id: str, open_id: str, share_id: str=None) -> None:
        """Recover secret value from shares in the 'share_db'.
        
        Parameters:
            shares_id (str): The identifier for the shares of the secret to be recovered. 
            open_id (str): The unique id for the recovered open value. 
        """
        shares = []
        for i in range(1, self.network_size+1):
            share_i = self.pop_share(f"_{shares_id}_node_{i}")
            shares.append(share_i)
        secret = self.sharer.recover(shares)
        if share_id:
            self.set_share(secret, share_id)
        else:
            self.set_open(secret, open_id)

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