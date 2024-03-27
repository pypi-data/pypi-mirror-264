import unittest

def combinationUtil(arr, r, j, data, i, subsets):
    if(j == r):
        subsets.append(list(data))
        return
    if(i >= len(arr)): return

    # Include
    data[j] = arr[i]
    combinationUtil(arr, r, j + 1, data, i + 1, subsets)

    # Exclude
    combinationUtil(arr, r, j, data, i + 1, subsets)

def combinations(n, r):
    arr = list(range(1, n+1))
    subsets = []
    data = [0] * r
    combinationUtil(arr, r, 0, data, 0, subsets)
    return subsets

class TestUtils(unittest.TestCase):

    def test_combinations(self):
        c = combinations(3, 2)
        excpected = [[1, 2], [1, 3], [2, 3]]
        self.assertEqual(c, excpected)

if __name__ == "__main__":
    unittest.main()