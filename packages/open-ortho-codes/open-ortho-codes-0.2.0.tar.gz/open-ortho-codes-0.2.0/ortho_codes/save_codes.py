#!/usr/bin/env python3
""" Convert Python code modules to JSON and CSV for publication.

When adding new modules:

- Import module
- Add new module to for loop in __main__
"""
import json
import csv
from pathlib import Path
from . import Code, snomed, hl7, vendors

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

def module_to_dict(module):
    Codes = {name: getattr(module, name) for name in dir(module)
             if isinstance(getattr(module, name), Code)}

    # Convert Code instances to dictionaries for JSON and CSV
    return {name: {'system': code.system, 'code': code.code, 'display': code.display}
                  for name, code in Codes.items()}


if __name__ == "__main__":
    for module in (snomed, hl7, vendors):
        dict_module = module_to_dict(module)
        save_to_json(dict_module, build_path / f'{module.__name__}.json')
        save_to_csv(dict_module, build_path / f'{module.__name__}.csv')
