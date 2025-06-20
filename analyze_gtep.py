#!/usr/bin/env python3
"""Simple analysis of gtep CSV dataset."""
import csv
from collections import defaultdict

CSV_FILE = 'gtepu.csv'

NUMERIC_FIELDS = [
    'PCL5_T0', 'BDI_T0', 'BAI_T0', 'WHO5_T0', 'BRS_T0', 'Symptomslist_T0',
    'PCL5_T1', 'BDI_T1', 'BAI_T1', 'WHO5_T1', 'BRS_T1', 'Symptomslist_T1',
]


def parse_float(value: str):
    value = value.strip()
    if not value:
        return None
    value = value.replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return None


def main():
    # dataset is encoded in Windows-1251
    with open(CSV_FILE, newline='', encoding='cp1251') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)
        # drop the first unnamed column
        header = [h.strip() for h in header][1:]
        indexes = {field: header.index(field) for field in NUMERIC_FIELDS}
        sex_index = header.index('Sex')

        sums = defaultdict(float)
        counts = defaultdict(int)
        diff_sums = defaultdict(float)
        diff_counts = defaultdict(int)
        sex_counts = defaultdict(int)

        for row in reader:
            row = row[1:]  # drop first column
            sex = row[sex_index].strip()
            sex_counts[sex] += 1
            for field in NUMERIC_FIELDS:
                val = parse_float(row[indexes[field]])
                if val is not None:
                    sums[field] += val
                    counts[field] += 1

            # compute differences between T1 and T0 where possible
            for prefix in ['PCL5', 'BDI', 'BAI', 'WHO5', 'BRS', 'Symptomslist']:
                v0 = parse_float(row[indexes[f'{prefix}_T0']])
                v1 = parse_float(row[indexes[f'{prefix}_T1']])
                if v0 is not None and v1 is not None:
                    diff_sums[prefix] += v1 - v0
                    diff_counts[prefix] += 1

    total = sum(sex_counts.values())
    print(f'Total entries: {total}')
    for sex, count in sex_counts.items():
        print(f'Sex {sex}: {count}')
    print()

    for field in NUMERIC_FIELDS:
        if counts[field]:
            avg = sums[field] / counts[field]
            print(f'Average {field}: {avg:.2f}')
    print()

    for prefix in ['PCL5', 'BDI', 'BAI', 'WHO5', 'BRS', 'Symptomslist']:
        if diff_counts[prefix]:
            avg_diff = diff_sums[prefix] / diff_counts[prefix]
            print(f'Average change {prefix}: {avg_diff:.2f}')


if __name__ == '__main__':
    main()
