"""Reconstruct scores, compare source salary versions, and retain model boundaries."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from dea import FEATURES, solve_dea

ROOT = Path(__file__).resolve().parents[1]


def build_results():
    with (ROOT / 'data/players.csv').open() as f:
        rows = list(csv.DictReader(f))
    perf = np.array([[float(r[c]) for c in FEATURES] for r in rows])
    salary = np.array([[float(r['salary_projection_usd']) / 1e6] for r in rows])
    labels = np.array([[float(r['salary_label_usd']) / 1e6] for r in rows])
    scenarios = {
        'reconstructed_ccr': solve_dea(perf, salary),
        'rounded_salary_ccr': solve_dea(perf, labels),
        'vrs_extension': solve_dea(perf, salary, vrs=True),
        'club_perspective_extension': solve_dea(salary, perf),
    }
    items = []
    for i, row in enumerate(rows):
        item = {'dmu_id': int(row['dmu_id']), 'player': row['player'],
                'reported_theta': float(row['reported_score'])}
        for name, values in scenarios.items():
            item[name] = values[i]
        item['difference_from_report'] = scenarios['reconstructed_ccr'][i]['theta'] - item['reported_theta']
        item['scale_efficiency_extension'] = scenarios['reconstructed_ccr'][i]['theta'] / scenarios['vrs_extension'][i]['theta']
        items.append(item)
    peers = list(csv.DictReader((ROOT / 'data/reported_peers.csv').open()))
    peer_errors = [abs(scenarios['reconstructed_ccr'][int(p['target_dmu'])-1]['lambdas'][int(p['peer_dmu'])-1] - float(p['reported_lambda'])) for p in peers]
    projections = list(csv.DictReader((ROOT / 'data/projections.csv').open()))
    arithmetic_errors = [abs(float(p['original']) + float(p['radial_movement']) + float(p['slack_movement']) - float(p['projected'])) for p in projections]
    model_projection_errors = []
    for p in projections:
        if p['variable'] == 'salary_usd':
            continue
        i = int(p['dmu_id'])-1
        j = FEATURES.index(p['variable'])
        value = float(perf[:,j] @ np.array(scenarios['reconstructed_ccr'][i]['lambdas']))
        model_projection_errors.append(abs(value-float(p['projected'])))
    return {'scope': '2026 reconstruction from 2024 team slides; no independent MLB or contract-data validation',
            'orientation': 'input', 'base_returns_to_scale': 'CRS (inferred by numeric reconstruction)',
            'dmu_count': len(rows), 'base_inputs': FEATURES, 'base_output': 'salary_projection_usd',
            'reported_mean': 0.883, 'reconstructed_mean': float(np.mean([r['theta'] for r in scenarios['reconstructed_ccr']])),
            'max_reported_score_error': max(abs(i['difference_from_report']) for i in items),
            'max_reported_peer_error': max(peer_errors),
            'projection_row_count': len(projections),
            'max_projection_arithmetic_error': max(arithmetic_errors),
            'max_model_projection_error': max(model_projection_errors),
            'players': items}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build_results()
    assert data['max_reported_score_error'] <= 0.0005
    assert data['max_reported_peer_error'] <= 0.0005
    assert data['max_projection_arithmetic_error'] <= 0.0016
    assert data['max_model_projection_error'] <= 0.002
    target = ROOT / 'results/reconstruction.json'
    if args.check:
        old = json.loads(target.read_text())
        def compare(a, b):
            if isinstance(a, dict):
                assert a.keys() == b.keys()
                for key in a: compare(a[key], b[key])
            elif isinstance(a, list):
                assert len(a) == len(b)
                for aa, bb in zip(a, b): compare(aa, bb)
            elif isinstance(a, (int, float)) and not isinstance(a, bool):
                assert abs(a-b) <= 1e-7, (a, b)
            else:
                assert a == b
        compare(data, old)
    else:
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(f"6 scores and 6 peer weights match source rounding; {data['projection_row_count']} projection rows checked.")
    print('Mean:', round(data['reconstructed_mean'], 6))
    for r in data['players']:
        print(r['player'], *(f"{r[k]['theta']:.6f}" for k in ['reconstructed_ccr', 'rounded_salary_ccr', 'vrs_extension', 'club_perspective_extension']))


if __name__ == '__main__':
    main()
