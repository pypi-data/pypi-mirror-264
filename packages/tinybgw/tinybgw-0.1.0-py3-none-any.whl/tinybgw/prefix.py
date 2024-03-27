import numpy as np
import unittest

from galois import Field

from .pseudo_network import PseudoNetwork

def invrand(network: PseudoNetwork, share_id: str, batch_size: int) -> None:
    """Generate an invertible random share.

    Parameters:
        share_id (str): The unique id of the new random share.
        batch_size (int): The number of random shares to create.

    Raises:
        ZeroDivisionError: A random number can be zero with negligble probability.
    """
    network.rand(share_id, batch_size)
    network.rand("_s", batch_size)
    network.pubmult(share_id, "_s", "_rs")
    # [r^{-1}] = (rs)^{-1} * [s]
    for node in network.nodes:
        s = node.pop_share("_s")
        rs = node.pop_open("_rs")
        r_inv = s / rs
        node.set_share(r_inv, share_id+"_inv")

def prefix(network: PseudoNetwork, mask_id: str, domino_id: str, size: int) -> None:
    """Generate prefix multiplication masks.

    Parameters:
        mask_id (str): The unique id of the masks.
        domino_id (str): The unique id of the domino masks.
        size (int): The number of random shares to create.

    Raises:
        ZeroDivisionError: A random number can be zero with negligble probability.
    """
    invrand(network, mask_id, size)
    for node in network.nodes:
        mask = node.get_share(mask_id)
        node.set_share(mask[:-1], "_mask")
        inv = node.get_share(mask_id+"_inv")
        node.set_share(inv[1:], "_mask_inv")
    network.mult("_mask", "_mask_inv", "_domino", True)
    for node in network.nodes:
        d = node.pop_share("_domino")
        inv = node.pop_share(mask_id+"_inv")
        d = np.concatenate(([inv[0]], d))
        node.set_share(d, domino_id)

def postfix(network: PseudoNetwork, mask_id: str, domino_id: str, size: int) -> None:
    """Generate postfix multiplication masks.

    Parameters:
        mask_id (str): The unique id of the masks.
        domino_id (str): The unique id of the domino masks.
        size (int): The number of random shares to create.

    Raises:
        ZeroDivisionError: A random number can be zero with negligble probability.
    """
    prefix(network, mask_id, domino_id, size)
    for node in network.nodes:
        mask = node.pop_share(mask_id)
        domino = node.pop_share(domino_id)
        node.set_share(mask[::-1], mask_id)
        node.set_share(domino[::-1], domino_id)

class TestUtils(unittest.TestCase): 
    def setUp(self): 
        np.random.seed(0)

    def test_invran(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        invrand(network, "r", 10)
        network.reveal("r", "r")
        network.reveal("r_inv", "r_inv")
        for node in network.nodes:
            r = node.get_open("r")
            r_inv = node.get_open("r_inv")
            result = r*r_inv
            for res in result:
                self.assertEqual(res, field(1))

    def test_prefix(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        prefix(network, "m", "d", 10)
        network.reveal("m", "m")
        network.reveal("d", "d")
        for node in network.nodes:
            m = node.pop_open("m")
            d = node.pop_open("d")
            res = 1
            for di in d:
                res *= di
            self.assertEqual(res, m[-1]**(-1))
    
    def test_postfix(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        postfix(network, "m", "d", 10)
        network.reveal("m", "m")
        network.reveal("d", "d")
        for node in network.nodes:
            m = node.pop_open("m")
            d = node.pop_open("d")
            res = 1
            for di in d:
                res *= di
            self.assertEqual(res, m[0]**(-1))

if __name__ == "__main__":
    unittest.main()