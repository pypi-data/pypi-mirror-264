import numpy as np
import operator
import unittest

from functools import reduce
from galois import Field
from galois.typing import ArrayLike, ElementLike

from .bits import rand_bitwise, rand_quaternary, bits_to_arithmetic
from .network import Network
from .prefix import postfix
from .pseudo_network import PseudoNetwork

def prod(iterable: ArrayLike) -> ElementLike:
    """Multiply all values in the iterable.
    
    Parameters:
        iterable (ArrayLike): Elements to iterate over.

    Returns:
        product (ElementLike): Product of all elements.
    """
    return reduce(operator.mul, iterable, 1)

def _bit(bit_index: int, value: int) -> int:
    """The bit of value at index.

    Parameters:
        bit_index (int): The index of quat.
        value (int): The open value.

    Returns:
        bit (int): The bit at i of the open value.
    """
    return (value >> bit_index) & 1

def _quat(quat_index: int, value: int) -> int:
    """The quat of value at index.

    Parameters:
        quat_index (int): The index of quat.
        value (int): The open value.

    Returns:
        quat (int): The quat at i of the open value.
    """
    return (value >> (2*quat_index)) & 3

def _equals(i: int, c: int, r: ArrayLike, rr: ArrayLike, field: Field) -> ElementLike:
    """Compares if the open value is equal to bitwise shared value.

    Parameters:
        i (int): The index of comparison.
        c (int): The open value.
        r (ArrayLike): The bitwise shared number.
        rr (ArrayLike): The multiplied bits of the bitwise shared number.

    Returns:
        equal (ElementLike): The shared value if quat at i of c is equal to r.
    """
    r0, r1 =  r[2*i], r[2*i+1]
    switch = {
        0: field(1) - r0 - r1 + rr[i],
        1: r0 - rr[i],
        2: r1 - rr[i],
        3: rr[i],
    }
    return switch[_quat(i, int(c))]

def _less(i: int, c: int, r: ArrayLike, rr: ArrayLike, field: Field) -> ElementLike:
    """Compares if open value is less than the bitwise shared value.

    Parameters:
        i (int): The index of comparison.
        c (int): The open value.
        r (ArrayLike): The bitwise shared number.
        rr (ArrayLike): The multiplied bits of the bitwise shared number.

    Returns:
        less (ElementLike): The shared value if quat at i of c is less than r.
    """
    r0, r1 =  r[2*i], r[2*i+1]
    # (1-c0)*(1-c1)*r0 + (1-c1)*r1 + (1-c0)*(2*c1-1)*rr[i]
    switch = {
        0: r0 + r1 - rr[i],
        1: r1,
        2: rr[i],
        3: field(0),
    }
    return switch[_quat(i, int(c))]

def log_bitwise_less_than(network: Network, open_id: str, bitwise_id: str, quat_id: str, 
                      result_id: str) -> None:
    """Compares open value with bitwise shared number in the network.

    Parameters:
        network (Network): The MPC network.
        open_id (str): The unique id of the open number.
        bitwise_id (str): The unique id of the bitwise number.
        quat_id (str): The unique id of the multiplied of bits of the bitwise number.
        result_id (str): The unique id of the less than result.
    """
    L2 = int(np.ceil(np.ceil(np.log2(network.prime())) / 2))
    # Compare each bit locally
    for node in network.nodes:
        c = node.get_open(open_id)
        c = np.reshape(c, (1))[0]
        r = node.get_share(bitwise_id)
        rr = node.get_share(quat_id)
        a = [_less(i, c, r, rr, network.field) for i in range(L2)]
        b = [_equals(i, c, r, rr, network.field) for i in range(L2)]
        node.set_share(a, "_a")
        node.set_share(b, "_b")
    # Recursively reduce results, log2(L/2) rounds
    l = int(np.log2(L2))
    for _ in range(l):
        for node in network.nodes:
            a = node.get_share("_a")
            node.set_share([a[2*i] for i in range(len(a)//2)], "_a_left")
            node.set_share([a[2*i+1] for i in range(len(a)//2)], "_a_right")
            b = node.get_share("_b")
            node.set_share([b[2*i] for i in range(len(b)//2)], "_b_left")
            node.set_share([b[2*i+1] for i in range(len(b)//2)], "_b_right")
        network.mult("_a_left", "_b_right", "_ab")
        network.mult("_b_left", "_b_right", "_b", True)
        network.add("_a_right", "_ab", "_a", True)
    # Set result and clean up
    for node in network.nodes:
        node.pop_share("_a_left")
        node.pop_share("_b")
        a = node.pop_share("_a")
        node.set_share(a, result_id)

def log_less_than_zero(network: Network, share_id: str, bitwise_id: str, quat_id: str, 
                       result_id: str) -> None:
    """Compares share value to zero using bitwise shared number in the network.

    Parameters:
        network (Network): The MPC network.
        share_id (str): The unique id of the share to be compared.
        bitwise_id (str): The unique id of the bitwise number.
        quat_id (str): The unique id of the multiplied of bits of the bitwise number.
        result_id (str): The unique id of the less than result.
    """
    # Reveal c + r
    bits_to_arithmetic(network, bitwise_id, "_r")
    for node in network.nodes:
        a = node.get_share(share_id)
        r = node.get_share("_r")
        c = network.field(2) * a + r
        node.set_share(c, "_c")
    network.reveal("_c", "_c", True)
    # Compare c and r
    log_bitwise_less_than(network, "_c", bitwise_id, quat_id, "_w")
    for node in network.nodes:
        w = node.get_share("_w")
        r = node.get_share(bitwise_id)
        y = network.field(1) - 2 * r[0]
        node.set_share(y, "_y")
        node.set_share(r[0], "_r0")
    network.mult("_y", "_w", "_p", True)
    network.add("_p", "_r0", "_z", True)
    # Set result
    for node in network.nodes:
        c = node.pop_open("_c")[0]
        c0 = c & 1
        result = c0 + (network.field(1) - 2*c0) * node.get_share("_z")
        node.set_share(result, result_id)
        # Clean Up
        node.pop_share("_r")

def log_less_than(network: Network, left_id: str, right_id: str, bitwise_id: str, quat_id: str, 
                  result_id: str) -> None:
    """Compares left share value to right share value using bitwise shared number in the network.

    Parameters:
        network (Network): The MPC network.
        left_id (str): The unique id of the left share to be compared.
        right_id (str): The unique id of the right shared to be compared.
        bitwise_id (str): The unique id of the bitwise number.
        quat_id (str): The unique id of the multiplied of bits of the bitwise number.
        result_id (str): The unique id of the less than result.
    """
    # Local: Every node locally subtracts the two shares.
    for node in network.nodes:
        left = node.get_share(left_id)
        right = node.get_share(right_id)
        node.set_share(left - right, "_diff")
    log_less_than_zero(network, "_diff", bitwise_id, quat_id, result_id)
    
def prep_less_than_zero(network: PseudoNetwork, prefix: str) -> None:
    """Compares share value to zero using bitwise shared number in the network.

    Parameters:
        network (Network): The MPC network.
        prefix (str): The prefix for the unique ids of the prep elements.
    """
    rand_quaternary(network, prefix+"_r", prefix+"_rr")
    rand_bitwise(network, prefix+"_s")
    for node in network.nodes:
        r = node.get_share(prefix+"_r")
        s = node.get_share(prefix+"_s")
        node.set_share([r[0]], prefix+"_r0")
        node.set_share([s[0]], prefix+"_s0")
        node.set_share([s[-1]], prefix+"_sL-1")
    # w0 = r[0] ^ s[0]
    network.xor(prefix+"_r0", prefix+"_s0", prefix+"_w0")
    # w1 = w0 ^ s[L-1]
    network.xor(prefix+"_w0", prefix+"_sL-1", prefix+"_w1")
    L = int(np.ceil(int(np.ceil(np.log2(network.prime()))) / 2) - 1)
    postfix(network, prefix+"_e", prefix+"_f", L)
    # Cleanup
    for node in network.nodes:
        node.pop_share(prefix+"_r0")
        node.pop_share(prefix+"_s0")
        node.pop_share(prefix+"_sL-1")
    
def less_than_zero(network: PseudoNetwork, share_id: str, prefix: str, result_id: str) -> None:
    """Compares share value to zero using bitwise shared number in the network.

    Parameters:
        network (Network): The MPC network.
        share_id (str): The unique id of the share to be compared.
        prefix (str): The prefix for the unique ids of the prep elements.
        result_id (str): The unique id of the less than result.
    """
    # Round 1: Reveal 2*share + r
    bits_to_arithmetic(network, prefix+"_r", "_r")
    for node in network.nodes:
        a = node.get_share(share_id)
        r = node.pop_share("_r")
        c = network.field(2) * a + r
        node.set_share(c, "_c")
    network.reveal("_c", "_c", True)
    # Round 2: Pub Mults
    L = int(np.ceil(np.log2(network.prime())))
    L2 = int(np.ceil(L / 2))
    for node in network.nodes:
        c = node.get_open("_c")
        c = np.reshape(c, (1))[0]
        r = node.pop_share(prefix+"_r")
        rr = node.pop_share(prefix+"_rr")
        v = [network.field(2) - _equals(i+1, c, r, rr, network.field) for i in range(L2-1)]
        node.set_share(v, "_v")
        m = [_less(i, c, r, rr, network.field) for i in range(L2-1)]
        node.set_share(m, "_m")
        m_last = [_less(L2-1, c, r, rr, network.field)]
        node.set_share(m_last, "_m_last")
    network.pubmult(prefix+"_f", "_v", "_cv", True)
    # Round 3: Inner Product
    bits_to_arithmetic(network, prefix+"_s", "_s")
    for node in network.nodes:
        m = node.pop_share("_m") * node.pop_share(prefix+"_e")
        v = node.pop_open("_cv")
        m = network.field([m[i] * prod(v[i:]) for i in range(L2-1)])
        x = np.sum(m) + node.pop_share("_m_last")
        s = node.pop_share("_s")
        zero = node.next_zero(1)
        node.set_share(x+s+zero, "_d")
    network.reveal("_d", "_d", True)
    # Result
    for node in network.nodes:
        d = node.pop_open("_d")
        dlast = _bit(L-1, d)
        w0 = node.pop_share(prefix+"_w0")
        w1 = node.pop_share(prefix+"_w1")
        w2 = w0 * dlast + w1 * (network.field(1) - dlast)
        c = node.pop_open("_c")
        w = _bit(0, c) ^ _bit(0, d)
        w = w + (network.field(1) - network.field(2) * w) * w2
        node.set_share(w, result_id)
        # Cleanup
        node.pop_share(prefix+"_s")

def less_than(network: Network, left_id: str, right_id: str, prefix: str, 
                  result_id: str) -> None:
    """Compares left share value to right share value using bitwise shared number in the network.

    Parameters:
        network (Network): The MPC network.
        left_id (str): The unique id of the left share to be compared.
        right_id (str): The unique id of the right shared to be compared.
        prefix (str): The prefix for the unique ids of the prep elements.
        result_id (str): The unique id of the less than result.
    """
    # Local: Every node locally subtracts the two shares.
    for node in network.nodes:
        left = node.get_share(left_id)
        right = node.get_share(right_id)
        node.set_share(left - right, "_diff")
    less_than_zero(network, "_diff", prefix, result_id)

class TestUtils(unittest.TestCase): 
    def setUp(self): 
        np.random.seed(0)

    def test_log_bit_less_than_lesser(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_quaternary(network, "r", "rr")
        network.broadcast(1, "c")
        log_bitwise_less_than(network, "c", "r", "rr", "c<r")
        network.reveal("c<r", "c<r")
        for node in network.nodes:
            result = node.get_open("c<r")
            self.assertEqual(result, field(1))

    def test_log_bit_less_than_greater(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_quaternary(network, "r", "rr")
        network.broadcast(65266, "c")
        log_bitwise_less_than(network, "c", "r", "rr", "c<r")
        network.reveal("c<r", "c<r")
        for node in network.nodes:
            result = node.get_open("c<r")
            self.assertEqual(result, field(0))

    def test_log_less_than_zero_lesser(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_quaternary(network, "r", "rr")
        network.share([65123], "a")
        log_less_than_zero(network, "a", "r", "rr", "a<0")
        network.reveal("a<0", "a<0")
        for node in network.nodes:
            result = node.get_open("a<0")
            self.assertEqual(result, field(1))
        
    def test_log_less_than_zero_greater(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_quaternary(network, "r", "rr")
        network.share([10], "a")
        log_less_than_zero(network, "a", "r", "rr", "a<0")
        network.reveal("a<0", "a<0")
        for node in network.nodes:
            result = node.get_open("a<0")
            self.assertEqual(result, field(0))

    def test_log_less_than_lesser(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_quaternary(network, "r", "rr")
        network.share([10], "a")
        network.share([12], "b")
        log_less_than(network, "a", "b", "r", "rr", "a<b")
        network.reveal("a<b", "a<b")
        for node in network.nodes:
            result = node.get_open("a<b")
            self.assertEqual(result, field(1))

    def test_log_less_than_greater(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        rand_quaternary(network, "r", "rr")
        network.share([54], "a")
        network.share([31], "b")
        log_less_than(network, "a", "b", "r", "rr", "a<b")
        network.reveal("a<b", "a<b")
        for node in network.nodes:
            result = node.get_open("a<b")
            self.assertEqual(result, field(0))

    def test_less_than_zero_lesser(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        prep_less_than_zero(network, "prep")
        network.share([65261], "a")
        less_than_zero(network, "a", "prep", "a<0")
        network.reveal("a<0", "a<0")
        for node in network.nodes:
            result = node.get_open("a<0")
            self.assertEqual(result, field(1))
        
    def test_less_than_zero_greater(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        prep_less_than_zero(network, "prep")
        network.share([10], "a")
        less_than_zero(network, "a", "prep", "a<0")
        network.reveal("a<0", "a<0")
        for node in network.nodes:
            result = node.get_open("a<0")
            self.assertEqual(result, field(0))

    def test_less_than_lesser(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        prep_less_than_zero(network, "prep")
        network.share([13], "a")
        network.share([41], "b")
        less_than(network, "a", "b", "prep", "a<b")
        network.reveal("a<b", "a<b")
        for node in network.nodes:
            result = node.get_open("a<b")
            self.assertEqual(result, field(1))

    def test_less_than_greater(self):
        N = 3; T = 1; field = Field(65267)
        network = PseudoNetwork(N, T, field)
        prep_less_than_zero(network, "prep")
        network.share([46], "a")
        network.share([31], "b")
        less_than(network, "a", "b", "prep", "a<b")
        network.reveal("a<b", "a<b")
        for node in network.nodes:
            result = node.get_open("a<b")
            self.assertEqual(result, field(0))

if __name__ == "__main__":
    unittest.main()
