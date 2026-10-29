import unittest

from labels import CHARACTERS


class CharacterLabelsTests(unittest.TestCase):
    def test_mapping_has_26_classes(self):
        self.assertEqual(len(CHARACTERS), 26)

    def test_mapping_matches_existing_export_order(self):
        self.assertEqual(CHARACTERS[0], "\u0B85")
        self.assertEqual(CHARACTERS[10], "\u0B95\u0B82")
        self.assertEqual(CHARACTERS[-1], "\u0BA9\u0B82")


if __name__ == "__main__":
    unittest.main()