import czastc
import unittest
class TestModule(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(czastc.greet("CZAsTc"), "Hello, CZAsTc!")
        self.assertEqual(czastc.greet("world"), "Hello, world!")
if __name__ == "__main__":
    unittest.main()