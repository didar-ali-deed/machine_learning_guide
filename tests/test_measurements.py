"""Verify the contract used by the modules-and-packages lesson."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from academy.measurements import finite_mean


class FiniteMeanTests(unittest.TestCase):
    def test_known_values_and_zero(self):
        self.assertEqual(finite_mean([0, 3, 6]), 3)
        self.assertEqual(finite_mean([0]), 0)

    def test_accepts_one_pass_iterable(self):
        self.assertEqual(finite_mean(value for value in [2, 4]), 3)

    def test_does_not_mutate_source(self):
        source = [1, 2, 6]
        self.assertEqual(finite_mean(source), 3)
        self.assertEqual(source, [1, 2, 6])

    def test_rejects_missing_flags_and_nonfinite_values(self):
        for invalid in ([], [None], [True], ['2'], [float('nan')], [float('inf')]):
            with self.subTest(values=invalid), self.assertRaises(ValueError):
                finite_mean(invalid)

    def test_translation_and_scale_properties(self):
        self.assertEqual(finite_mean([12, 14]), finite_mean([2, 4]) + 10)
        self.assertEqual(finite_mean([4, 8]), 2 * finite_mean([2, 4]))


if __name__ == '__main__':
    unittest.main()
