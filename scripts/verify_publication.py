"""Check local relative links, public file types and data/result consistency."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.venv', '.mplconfig', '__pycache__'}


def public_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(s in SKIP for s in p.relative_to(ROOT).parts))


def main():
    files = public_files()
    links = 0
    for p in files:
        assert p.suffix.lower() in {'.md', '.py', '.csv', '.json', '.svg', '.txt'} or p.name == '.gitignore', p
        text = p.read_text()
        assert (chr(47) + 'Users' + chr(47)) not in text, f'Absolute local path in {p.name}'
        assert not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}', text), p
        assert ('-----BEGIN ' + 'PRIVATE KEY-----') not in text, p
        if p.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if re.match(r'^[a-z]+:', link) or link.startswith('#'):
                    continue
                target = (p.parent / link.split('#')[0]).resolve()
                assert target.is_relative_to(ROOT), link
                assert target.exists(), (p.name, link)
                links += 1
    players = list(csv.DictReader((ROOT/'data/players.csv').open()))
    data = json.loads((ROOT/'results/reconstruction.json').read_text())
    assert len(players) == data['dmu_count'] == 6
    for source, result in zip(players, data['players']):
        assert source['player'] == result['player']
        assert abs(float(source['reported_score'])-result['reconstructed_ccr']['theta']) <= .0005
    assert int(players[4]['salary_projection_usd']) == 30416667
    assert int(players[4]['salary_label_usd']) == 30000000
    for p in data['players']:
        for scenario in ['reconstructed_ccr', 'rounded_salary_ccr', 'vrs_extension', 'club_perspective_extension']:
            assert 0 < p[scenario]['theta'] <= 1 + 1e-8
            assert p[scenario]['max_scaled_violation'] <= 1e-7
    print(f'{len(files)} public files, {links} local links and 24 scenario scores checked.')


if __name__ == '__main__':
    main()
