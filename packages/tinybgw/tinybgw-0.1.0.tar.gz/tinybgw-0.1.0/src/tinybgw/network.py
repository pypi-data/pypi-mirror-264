import numpy as np
import unittest

from galois import Field
from galois.typing import ArrayLike, ElementLike
from typing import List

from .node import Node
from .shamir import ShamirSharer
from .sharer import SecretSharer

class Network:
    """Represents a network of nodes and clients.
    
    Manages the interactions and cryptographic operations within the network, including sharing 
    secrets, resharing shares, broadcasting values, revealing shares by reconstructing shared values
    and multiplying two secret shared values.
    """

    nodes: List[Node]
    """List of clients in the network."""
    sharer: ShamirSharer
    """Secret sharer that handles secret sharing and recovery."""

    def __init__(self, size: int, threshold: int, field: Field) -> None:
        """Initialize the network.
        
        Parameters:
            size (int): The number of nodes in the network.
            threshold (int): The security threshold of the network.
            field (Field): The finite field that the shares live in.
        """
        self.nodes = [Node(i+1, size, threshold, field) for i in range(size)]
        self.sharer = ShamirSharer([i+1 for i in range(size)], field, threshold)

    def print(self):
        """Print a readable representation of the network, including nodes with their databases."""
        print(f"Network(N={len(self.nodes)}, T={self.nodes[0].sharer.threshold}, F={self.nodes[0].sharer.field.order}")
        print("  nodes=[")
        for node in self.nodes:
            print(f"    Node(id={node.id},")
            print("      shares_db={")
            for key, value in node.shares_db.items():
                print(f"        {key}: {value},")
            print("      },")
            print("      open_db={")
            for key, value in node.open_db.items():
                print(f"        {key}: {value},")
            print("      }")
            print("    )")
        print("  ]\n)")

    def field(self, value: ArrayLike) -> Field:
        """Returns the values as field elements.

        Parameters:
            value (ArrayLike): The values to be converted.
        
        Returns:
            value (ArrayLike): The values as field elements.
        """
        return self.sharer.field(value)

    def prime(self) -> int:
        """Returns the order of the field.
        
        Returns:
            prime (int): The order of the field.
        """
        return self.sharer.field.order

    def share(self, secret: ArrayLike, share_id: str) -> None:
        """Share secret value with all nodes.

        Parameters:
            secret (ArrayLike): Secret value to be shared.
            share_id (str): The unique id for the shares of the secret.
        """
        shares = self.sharer.share(secret)
        for node in self.nodes:
            node.set_share(shares[node.id - 1], share_id)

    def reshare(self, share_id: str) -> None:
        """Reshare shared value with all nodes. 
        
        Resharing reduces the degree of the sharings back to the threshold.

        Parameters:
            share_id (str): The unique id for the shares of the secret.
        """
        # Round 1: Every node reshares their secret.
        for node in self.nodes:
            self.share(node.get_share(share_id), f"_{share_id}_node_{node.id}")
        # Local: Every node locally reconstructs the new secret.
        for node in self.nodes:
            node.recover(share_id, None, share_id)

    def broadcast(self, value: ArrayLike, open_id: str) -> None:
        """Send value to all nodes.
        
        Parameters:
            value (ArrayLike): The open value to be broadcast.
            open_id (str): The unique id for the open value.
        """
        for node in self.nodes:
            node.set_open(value, open_id)

    def reveal(self, share_id: str, open_id: str, delete_share: bool=False) -> None:
        """Reveal share to all nodes.
        
        Parameters:
            share_id (str): The unique id for the share.
            open_id (str): The unique id for the revealed value.
            delete_share (bool): Whether to delete the share after revealing.
        """
        # Round 1: Every node sends their share to every other node.
        for node in self.nodes:
            for receiver_node in self.nodes:
                receiver_node.set_share(node.get_share(share_id), f"_reveal_node_{node.id}")
        # Local: Every node locally reconstructs and sets open value.
        for node in self.nodes:
            node.recover("reveal", open_id)

        if delete_share:
            for node in self.nodes:
                node.pop_share(share_id)

    def add(self, left_id: str, right_id: str, sum_id: str, delete_shares: bool=False) -> None:
        """Adds two shares.
        
        Parameters:
            left_id (str): The unique id for the left share.
            right_id (str): The unique id for the right share.
            product_id (str): The unique id for the resulting product of the shares.
            delete_share (bool): Whether to delete the shares after multiplying.
        """
        # Local: Every node locally adds the two shares.
        for node in self.nodes:
            left = node.get_share(left_id)
            right = node.get_share(right_id)
            node.set_share(left + right, sum_id)

        if delete_shares:
            for node in self.nodes:
                node.pop_share(left_id)
                node.pop_share(right_id)

    def mult(self, left_id: str, right_id: str, product_id: str, delete_shares: bool=False) -> None:
        """Multiplies two shares.
        
        Parameters:
            left_id (str): The unique id for the left share.
            right_id (str): The unique id for the right share.
            product_id (str): The unique id for the resulting product of the shares.
            delete_share (bool): Whether to delete the shares after multiplying.
        """
        # Local: Every node locally multiplies the two shares.
        for node in self.nodes:
            left = node.get_share(left_id)
            right = node.get_share(right_id)
            node.set_share(left * right, product_id)
        # Round 1: Every node reshares their product to reduce the degree.
        self.reshare(product_id)

        if delete_shares:
            for node in self.nodes:
                node.pop_share(left_id)
                node.pop_share(right_id)
    
    def xor(self, left_id: str, right_id: str, xor_id: str, delete_shares: bool=False) -> None:
        """Xors two shares.
        
        Parameters:
            left_id (str): The unique id for the left share.
            right_id (str): The unique id for the right share.
            xor_id (str): The unique id for the resulting product of the shares.
            delete_share (bool): Whether to delete the shares after multiplying.
        """
        # Local: Every node locally multiplies the two shares.
        for node in self.nodes:
            left = node.get_share(left_id)
            right = node.get_share(right_id)
            xor = left + right - self.field(2) * left * right
            node.set_share(xor, xor_id)
        # Round 1: Every node reshares their product to reduce the degree.
        self.reshare(xor_id)

        if delete_shares:
            for node in self.nodes:
                node.pop_share(left_id)
                node.pop_share(right_id)

class TestUtils(unittest.TestCase):
    
    def setUp(self): 
        np.random.seed(0)

    def test_share_recover_secret(self):
        N = 3; T = 1; field = Field(13)
        network = Network(N, T, field)
        secret = [7]
        network.share(secret, "secret_2")
        network.reveal("secret_2", "revealed")
        for node in network.nodes:
            self.assertEqual(node.get_open("revealed"), secret)

    def test_batch_share_recover_secret(self):
        N = 3; T = 1; field = Field(13)
        network = Network(N, T, field)
        secrets = [2, 3, 4, 5]
        network.share(secrets, "secret_2")
        network.reveal("secret_2", "revealed")
        for node in network.nodes:
            self.assertEqual(node.get_open("revealed"), secrets)

    def test_reshare(self):
        N = 3; T = 1; field = Field(13)
        network = Network(N, T, field)
        network.share([3], "secret_3")
        network.reshare("secret_3")
        network.reveal("secret_3", "revealed")
        for node in network.nodes:
            self.assertEqual(node.get_open("revealed"), [3])

    def test_mult(self):
        N = 3; T = 1; field = Field(13)
        network = Network(N, T, field)
        network.share([2, 3], "secret_2")
        network.share([3, 4], "secret_3")
        network.mult("secret_2", "secret_3", "product")
        network.reveal("product", "revealed")
        for node in network.nodes:
            self.assertEqual(node.get_open("revealed"), [6, 12])

    def test_xor(self):
        N = 3; T = 1; field = Field(13)
        network = Network(N, T, field)
        network.share([0, 1, 0, 1], "secret_0")
        network.share([0, 0, 1, 1], "secret_1")
        network.xor("secret_0", "secret_1", "xor")
        network.reveal("xor", "revealed")
        for node in network.nodes:
            self.assertEqual(node.get_open("revealed"), [0, 1, 1, 0])
        
if __name__ == "__main__":
    unittest.main()