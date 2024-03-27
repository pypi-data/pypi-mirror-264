import numpy as np
import unittest

from galois import Field

from .bits import bits_to_arithmetic, rand_quaternary
from .lessthan import log_bitwise_less_than
from .network import Network
from .pseudo_network import PseudoNetwork


def trunc(network: Network, share_id: str, k: int, m: int, bitwise_id: str, 
          quat_id: str, result_id: str) -> None:
    """Compares open value with bitwise shared number in the network.

    Parameters:
        network (Network): The MPC network.
        share_id (str): The unique id of the share.
        bitwise_id (str): The unique id of the bitwise number.
        quat_id (str): The unique id of the multiplied of bits of the bitwise number.
        result_id (str): The unique id of the less than result.
    """
    bits_to_arithmetic(network, bitwise_id, "_r")
    bits_to_arithmetic(network, bitwise_id, "_r_m", m)
    for node in network.nodes:
        s = node.get_share(share_id)
        r = node.pop_share("_r")
        two_k = network.field(2)**(k-1)
        c = two_k + s + r
        node.set_share(c, "_c")
    network.reveal("_c", "_c", True)
    log_bitwise_less_than(network, "_c", bitwise_id, quat_id, "_c<r")
    p = network.prime()
    one = network.field(1)
    two_m = 2**m
    two_m_inv = network.field(2)**(-m)
    for node in network.nodes:
        c = int(node.pop_open("_c")[0])
        o = node.pop_share("_c<r")[0]
        cp = network.field(c % two_m)*(one-o) + network.field((p+c) % two_m)*o
        s = node.get_share(share_id)
        r_m = node.pop_share("_r_m")
        t = s + r_m - cp
        d = t * two_m_inv
        node.set_share(d, result_id)

class TestUtils(unittest.TestCase): 
    def setUp(self): 
        np.random.seed(0)

    def test_trunc(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_quaternary(network, "r", "rr")
        network.share([67], "share")
        trunc(network, "share", 8, 4, "r", "rr", "trunked")
        network.reveal("trunked", "trunked")
        for node in network.nodes:
            result = node.get_open("trunked")
            self.assertEqual(result, field(4))

if __name__ == "__main__":
    unittest.main()