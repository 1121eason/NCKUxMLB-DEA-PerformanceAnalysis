"""Explicit input-oriented radial DEA; 2026 reconstruction, not original code."""
import numpy as np
from scipy.optimize import linprog

FEATURES = ['runs', 'hits', 'doubles', 'triples', 'home_runs', 'rbi',
            'walks', 'stolen_bases', 'avg', 'obp', 'slg', 'ops']


def solve_dea(inputs, outputs, vrs=False):
    """Min theta: X' lambda <= theta*x_o, Y' lambda >= y_o.

    VRS adds sum(lambda)=1. Zeros are retained; no epsilon replacement.
    Columns are scaled for numerical conditioning, without changing the LP.
    Scores near one establish radial efficiency only; inspect slacks separately.
    """
    raw_x = np.asarray(inputs, dtype=float)
    raw_y = np.asarray(outputs, dtype=float)
    if raw_x.ndim != 2 or raw_y.ndim != 2 or len(raw_x) != len(raw_y):
        raise ValueError('Inputs and outputs must be aligned 2D matrices')
    if not np.isfinite(raw_x).all() or not np.isfinite(raw_y).all():
        raise ValueError('Non-finite values are not allowed')
    if (raw_x < 0).any() or (raw_y < 0).any():
        raise ValueError('Negative values are not supported')
    if (raw_x.sum(axis=1) == 0).any() or (raw_y.sum(axis=1) == 0).any():
        raise ValueError('Each DMU needs positive aggregate input and output')
    x = raw_x / np.where(raw_x.max(axis=0) > 0, raw_x.max(axis=0), 1)
    y = raw_y / np.where(raw_y.max(axis=0) > 0, raw_y.max(axis=0), 1)
    n, m = x.shape
    s = y.shape[1]
    answers = []
    for o in range(n):
        a = np.vstack([np.column_stack([x.T, -x[o]]),
                       np.column_stack([-y.T, np.zeros(s)])])
        b = np.r_[np.zeros(m), -y[o]]
        result = linprog(np.r_[np.zeros(n), 1.0], A_ub=a, b_ub=b,
                         A_eq=[np.r_[np.ones(n), 0]] if vrs else None,
                         b_eq=[1] if vrs else None,
                         bounds=[(0, None)] * (n + 1), method='highs')
        if not result.success:
            raise RuntimeError(f'DMU {o + 1}: {result.message}')
        residual = float(max(0.0, np.max(a @ result.x - b)))
        if residual > 1e-7:
            raise RuntimeError(f'DMU {o + 1}: constraint violation {residual}')
        answers.append({'theta': float(result.fun),
                        'lambdas': result.x[:n].tolist(),
                        'max_scaled_violation': residual,
                        'input_slack': (result.fun * raw_x[o] - raw_x.T @ result.x[:n]).tolist(),
                        'output_slack': (raw_y.T @ result.x[:n] - raw_y[o]).tolist()})
    return answers
