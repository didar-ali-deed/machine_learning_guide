"""Render saved notebook PNG outputs into a headless review contact sheet."""
import argparse
import base64
import io
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat
from academy_tools import ROOT, inventory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='+', required=True)
    parser.add_argument('--output', required=True, help='Filename under reports/, ending .png')
    args = parser.parse_args()
    destination = (ROOT / 'reports' / args.output).resolve()
    if not destination.is_relative_to((ROOT / 'reports').resolve()) or destination.suffix != '.png':
        parser.error('Use a PNG destination inside reports/.')
    records = {record['id']: record for record in inventory()}
    plots = []
    for ident in args.ids:
        if ident not in records:
            parser.error(f'Unknown lesson ID: {ident}')
        notebook = nbformat.read(ROOT / 'reports/executed' / records[ident]['path'], as_version=4)
        print(f"LESSON {ident}: {records[ident]['title']}")
        for cell in notebook.cells:
            if cell.cell_type != 'code':
                continue
            for output in cell.outputs:
                if output.output_type == 'stream':
                    print(output.text.strip())
                if 'image/png' in output.get('data', {}):
                    pixels = plt.imread(io.BytesIO(base64.b64decode(output.data['image/png'])))
                    plots.append((ident, pixels))
    if not plots:
        raise SystemExit('Selected executed copies contain no rendered PNG figures.')
    figure, axes = plt.subplots(len(plots), 1, figsize=(11, 3.8 * len(plots)), squeeze=False)
    for axis, (ident, pixels) in zip(axes[:, 0], plots):
        axis.imshow(pixels)
        axis.set_title(f"{ident}: {records[ident]['title']}")
        axis.axis('off')
    figure.tight_layout()
    figure.savefig(destination, dpi=140)
    plt.close(figure)
    print(f'Saved {len(plots)} plots to {destination.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
