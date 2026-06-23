import csv
import json
import os


def export_csv(rows: list, output_path: str):
    if not rows:
        print('No data to export.')
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f'Exported {len(rows)} rows to {output_path}')


def export_json(rows: list, output_path: str):
    if not rows:
        print('No data to export.')
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None

    data = [list(row) for row in rows]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

    print(f'Exported {len(rows)} rows to {output_path}')