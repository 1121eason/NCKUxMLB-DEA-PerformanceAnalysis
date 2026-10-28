"""Render deterministic SVG charts from checked model output."""
import argparse
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'mlb-dea-2026',
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#bec8d3', 'text.color': '#16324f',
                     'axes.labelcolor': '#16324f', 'xtick.color': '#40566d',
                     'ytick.color': '#40566d'})


def render_all():
    data = json.loads((ROOT / 'results/reconstruction.json').read_text())
    players = data['players']
    figs = {}
    names = [p['player'] for p in players]
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.5), sharey=True)
    fig.set_facecolor('#f7fafc')
    y = np.arange(6)
    for ax, key, title, color in zip(
        axes, ['reconstructed_ccr', 'club_perspective_extension'],
        ['Historical setting\nBatting inputs → Salary output',
         'Perspective diagnostic · added in 2026\nSalary input → Batting outputs'],
        ['#267a9e', '#d28643']):
        ax.set_facecolor('#f7fafc')
        values = [p[key]['theta'] for p in players]
        ax.barh(y, values, height=.56, color=color)
        ax.set_xlim(0, 1.18)
        ax.set_xticks([0, .25, .5, .75, 1])
        ax.set_title(title, loc='left', fontsize=12, pad=18, weight='bold')
        ax.set_xlabel('Input-oriented CCR radial score')
        ax.axvline(1, color='#8195a6', linestyle='--', linewidth=.8)
        for i, v in enumerate(values):
            ax.text(v+.025, i, f'{v:.3f}', va='center', fontsize=11)
        ax.set_yticks(y, names)
    axes[0].invert_yaxis()
    fig.suptitle('One dataset. Two decision questions.', x=.025, ha='left',
                 fontsize=19, weight='bold', y=.98)
    fig.text(.025, .035, 'Six-player historical sample · Three-decimal labels · A score of 1 is relative to this model and sample.', fontsize=10)
    fig.subplots_adjust(left=.16, right=.98, top=.77, bottom=.17, wspace=.13)
    figs['efficiency-comparison.svg'] = fig

    betts = players[4]
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    fig.set_facecolor('#f7fafc')
    ax.set_facecolor('#f7fafc')
    vals = [betts['rounded_salary_ccr']['theta'], betts['reconstructed_ccr']['theta']]
    ax.barh([1, 0], vals, color=['#b0bfcd', '#267a9e'], height=.5)
    ax.set_yticks([1, 0], ['Slide summary\nUS$30,000,000', 'Projection table\nUS$30,416,667'])
    ax.set_xlim(0, 1.02)
    ax.set_xlabel('Reconstructed input-oriented CCR score')
    ax.set_xticks([0, .25, .5, .75, 1])
    for yy, v in zip([1, 0], vals):
        ax.text(v+.018, yy, f'{v:.6f}', va='center', weight='bold')
    fig.suptitle('A salary label is not always the model value.', x=.025,
                 ha='left', fontsize=18, weight='bold', y=.96)
    fig.text(.025, .85, 'Mookie Betts · Only the salary source version changes', fontsize=11)
    fig.text(.025, .035, 'The projection-table value reproduces the reported 0.738. Both source versions are retained.', fontsize=10)
    fig.subplots_adjust(left=.22, right=.97, top=.72, bottom=.18)
    figs['salary-sensitivity.svg'] = fig
    return figs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, fig in render_all().items():
        stream = io.StringIO()
        fig.savefig(stream, format='svg', metadata={'Date': None, 'Creator': 'MLB DEA case study, Matplotlib'})
        content = stream.getvalue()
        target = ROOT / 'assets' / name
        if args.check:
            assert target.read_text() == content, f'Stale chart: {name}'
        else:
            target.write_text(content)
        plt.close(fig)
    print('2 source-driven charts verified' if args.check else '2 source-driven charts written')


if __name__ == '__main__':
    main()
