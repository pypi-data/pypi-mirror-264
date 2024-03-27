import numpy as np
import unittest

from galois import Field
from galois.typing import ArrayLike, ElementLike
from typing import List

from .pseudo_node import PseudoNode
from .network import Network
from .shamir import ShamirSharer
from .sharer import SecretSharer
    
class PseudoNetwork(Network):
    """Represents a network of nodes and clients.
    
    Manages the interactions and cryptographic operations within the network, including sharing 
    secrets, resharing shares, broadcasting values, revealing shares by reconstructing shared values
    and multiplying two secret shared values.
    """

    nodes: List[PseudoNode]
    """List of clients in the network."""
    
    def __init__(self, size: int, threshold: int, field: Field) -> None:
        """Initialize the network.
        
        Parameters:
            size (int): The number of nodes in the network.
            threshold (int): The security threshold of the network.
            field (Field): The finite field that the shares live in.
        """
        sharer = SecretSharer(field, size, size-threshold)
        shares = sharer.replicated_share(1)
        zero_shares = sharer.replicated_share([1 for _ in range(threshold)])
        self.nodes = [PseudoNode(i+1, size, threshold, field, shares[i], zero_shares[i]) for i in range(size)]
        self.sharer = ShamirSharer([i+1 for i in range(size)], field, threshold)

    def rand(self, share_id: str, batch_size: int=1) -> None:
        """Locally generate a pseudo random share.

        Parameters:
            share_id (str): The unique id of the new random share.
            batch_size (int): The number of random shares to create.
        """
        for node in self.nodes:
            rand = node.next_rand(batch_size)
            node.set_share(rand, share_id)

    def zero(self, share_id: str, batch_size: int=1) -> None:
        """Locally generate a pseudo zero share.

        Parameters:
            share_id (str): The unique id of the new zero share.
            batch_size (int): The number of zero shares to create.
        """
        for node in self.nodes:
            zero = node.next_zero(batch_size)
            node.set_share(zero, share_id)

    def pubmult(self, left_id: str, right_id: str, product_id: str, delete_shares: bool=False) -> None:
        """Multiplies two shares and reveals the result.
        
        Parameters:
            left_id (str): The unique id for the left share.
            right_id (str): The unique id for the right share.
            product_id (str): The unique id for the resulting product of the shares.
            delete_share (bool): Whether to delete the shares after multiplying.
        """
        # Local: Every node locally multiplies the two shares.
        for node in self.nodes:
            p = node.get_share(left_id) * node.get_share(right_id)
            z = node.next_zero(len(p))
            node.set_share(p+z, product_id)
        # Round 1: Every node reshares their product to reduce the degree.
        self.reveal(product_id, product_id, True)

        if delete_shares:
            for node in self.nodes:
                node.pop_share(left_id)
                node.pop_share(right_id)

class TestUtils(unittest.TestCase):
    
    def setUp(self): 
        np.random.seed(0)

    def test_rand(self):
        N = 3; T = 2; field = Field(13)
        network = PseudoNetwork(N, T, field)
        network.rand("random", 5)
        network.reveal("random", "revealed")
        
    def test_zero(self):
        N = 5; T = 2; field = Field(13)
        network = PseudoNetwork(N, T, field)
        network.zero("zero", 5)
        network.reveal("zero", "zero")
        for node in network.nodes:
            z = node.get_open("zero")
            for i in range(len(z)):
                self.assertEqual(z[i], 0)

    def test_pubmult(self):
        N = 3; T = 1; field = Field(13)
        network = PseudoNetwork(N, T, field)
        network.share([2, 3], "secret_2")
        network.share([3, 4], "secret_3")
        network.pubmult("secret_2", "secret_3", "product")
        for node in network.nodes:
            self.assertEqual(node.get_open("product"), [6, 12])
        
if __name__ == "__main__":
    unittest.main()