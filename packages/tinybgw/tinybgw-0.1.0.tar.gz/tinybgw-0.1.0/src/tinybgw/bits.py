import numpy as np
import unittest

from galois import Field

from .network import Network
from .pseudo_network import PseudoNetwork

def rand_bit(network: Network, batch_size: int, bit_share_id: str) -> None:
    """Generates shared bits in the network.

    Parameters:
        network (Network): The MPC network.
        batch_size (int): The number of bits to be created.
        bit_share_id (str): The unique id of the bits created.
    """
    network.rand("_r", batch_size)
    network.pubmult("_r", "_r", "_r^2")
    # [b] = 2^-1 * (sqrt(r^2)^-1 * [r] + 1)
    two_inv = network.field(2)**(-1)
    one = network.field(1)
    for node in network.nodes:
        r2 = node.pop_open("_r^2")
        q = np.sqrt(network.field(r2))**(-1)
        r = node.pop_share("_r")
        b = two_inv * (q*r + one)
        node.set_share(b, bit_share_id)

def rand_bitwise(network: Network, bit_share_id: str) -> None:
    """Generates shared bitwise number in the network.

    Parameters:
        network (Network): The MPC network.
        bit_share_id (str): The unique id of the bitwise number created.

    Raises:
        Exception: Bitwise number larger than prime.
    """
    p = network.prime()
    l = int(np.ceil(np.log2(p)))
    # Generate the bitwise number ([r])
    rand_bit(network, l, bit_share_id)
    # Generate randomness to check if r < p
    def bit(x, i): return (x >> i) & 1
    def fbit(x, i): return network.field(bit(x, i))
    m = 1 + sum([1 - bit(p, i) for i in range(l)])
    network.rand("_s", m)
    # [d_i] = 1 - [r_i] + sum_{j=i+1}^l (p_j + (1-2p_j)*[r_j])
    one = network.field(1)
    two = network.field(2)
    for node in network.nodes:
        r = node.get_share(bit_share_id)
        d = []; f_i = network.field(0)
        for i in range(l-2, -1, -1):
            f_i += fbit(p, i+1) + (one-two*fbit(p, i+1)) * r[i+1]
            if bit(p-1, i) == 0:
                d.append(one - r[i] + f_i)
        node.set_share(network.field(d), "_d")
    network.pubmult("_s", "_d", "_e", True)
    # Check
    exception = False
    for node in network.nodes:
        e = node.pop_open("_e")
        for e_i in e: 
            if e_i == 0: exception = True
    if exception: raise Exception("Bitwise number larger than prime.")

def bits_to_arithmetic(network: Network, bit_share_id: str, share_id: str,
                        m: int=None) -> None:
    """Converts bitwise number to arithmetic sharing.

    Parameters:
        network (Network): The MPC network.
        bit_share_id (str): The unique id of the bitwise number.
        share_id (str): The unique id of the arithmetic sharing created.
        m (int): 
    """
    two = network.field(2)
    for node in network.nodes:
        b = node.get_share(bit_share_id)
        if not m: m = len(b)
        t = network.field([two**i for i in range(m)])
        r = np.sum(t*b[:m])
        node.set_share([r], share_id)

def rand_quaternary(network: Network, bit_share_id: str, quat_share_id: str) -> None:
    """Generates shared bitwise number in the network.

    Parameters:
        network (Network): The MPC network.
        bit_share_id (str): The unique id of the bitwise number created.
        quat_share_id (str): The unique id of the multiplied of bits.

    Raises:
        Exception: Bitwise number larger than prime.
    """
    rand_bitwise(network, bit_share_id)
    for node in network.nodes:
        r = node.get_share(bit_share_id)
        r_low = [r[i] for i in range(0, len(r), 2)]
        r_high = [r[i] for i in range(1, len(r), 2)]
        if len(r_low) > len(r_high): r_low.pop()
        node.set_share(r_low, "_r_low")
        node.set_share(r_high, "_r_high")
    network.mult("_r_low", "_r_high", quat_share_id, True)

class TestUtils(unittest.TestCase): 
    def setUp(self): 
        np.random.seed(0)

    def test_bits(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_bit(network, 10, "b")
        network.reveal("b", "b")
        for node in network.nodes:
            b = node.get_open("b")
            for b_i in b:
                self.assertTrue(int(b_i) in (0, 1))

if __name__ == "__main__":
    unittest.main()
