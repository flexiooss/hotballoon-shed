import unittest
from typing import Optional, List
from cmd.package.Version import Version
import semver

class TestVersion(unittest.TestCase):

    def test_empty(self):

        self.assertFalse(Version('2.0.0').satisfies('1.0.0'))
        self.assertTrue(Version('2.0.0').satisfies('>1.0.0'))
        self.assertTrue(Version('2.0.0').satisfies('~2.0.0'))

