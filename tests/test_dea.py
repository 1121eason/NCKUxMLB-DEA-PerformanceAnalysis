"""Behavioral checks: known frontiers, unit invariance, VRS nesting and zeros."""
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from dea import solve_dea


class DEATests(unittest.TestCase):
    def test_known_frontier_and_dominance(self):
        answers = solve_dea([[1], [2]], [[1], [1]])
        np.testing.assert_allclose([r['theta'] for r in answers], [1, .5])

    def test_units_do_not_change_score(self):
        x = np.array([[1, 2], [2, 1], [3, 3]])
        y = np.array([[1], [1], [1]])
        a = solve_dea(x, y)
        b = solve_dea(x * [1000, .001], y * 1e6)
        np.testing.assert_allclose([r['theta'] for r in a], [r['theta'] for r in b])

    def test_vrs_constraint_cannot_lower_input_score(self):
        x, y = [[1], [3], [4]], [[1], [2], [2]]
        crs = solve_dea(x, y)
        vrs = solve_dea(x, y, vrs=True)
        self.assertTrue(all(v['theta'] >= c['theta'] - 1e-8 for c, v in zip(crs, vrs)))
        self.assertTrue(all(abs(sum(v['lambdas'])-1) < 1e-8 for v in vrs))

    def test_zero_component_is_retained(self):
        answers = solve_dea([[1, 0], [2, 1]], [[1], [1]])
        np.testing.assert_allclose([r['theta'] for r in answers], [1, .5])

    def test_bad_values_fail(self):
        for x in [[[-1]], [[float('nan')]], [[0]]]:
            with self.assertRaises(ValueError): solve_dea(x, [[1]])


if __name__ == '__main__':
    unittest.main()
