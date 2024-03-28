#!/usr/bin/env python3

import json
import csv
from pathlib import Path
from codes import NAMESPACE, Codes

build_path = Path('.', 'build')

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'System', 'Code', 'Display'])
        for key, value in data.items():
            writer.writerow([key, value['system'], value['code'], value['display']])

if __name__ == "__main__":
    save_to_json(Codes, build_path / 'codes.json')
    save_to_csv(Codes, build_path / 'codes.csv')
