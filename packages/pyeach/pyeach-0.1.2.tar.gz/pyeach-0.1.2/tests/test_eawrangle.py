"""
Test the variables in eawrangle.py
"""

import unittest
import numpy as np


class TestEAWrangle(unittest.TestCase):
    def test_bucket_continuous(self):
        from pyeach.eawrangle import bucket_continuous

        ages = np.arange(4, 80, 10)
        age_buckets = [bucket_continuous(x) for x in ages]
        buckets = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-64', '65+']
        self.assertEqual(age_buckets, buckets)


if __name__ == '__main__':
    unittest.main()
