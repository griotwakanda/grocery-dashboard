import csv
import json
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
GROCERY_DIR = SCRIPTS_DIR.parent
RECEIPTS_CSV = GROCERY_DIR / 'receipts.csv'
LINE_ITEMS_CSV = GROCERY_DIR / 'line_items.csv'
OUTPUT_JSON = GROCERY_DIR / 'grocery-data.json'

NUM_FIELDS = {
    'receipts': ['subtotal', 'tax', 'total'],
    'line_items': ['quantity', 'unit_price', 'line_total'],
}

BOOL_FIELDS = {
    'line_items': ['is_discount'],
}


def parse_csv(path, kind):
    rows = []
    with open(path, encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            parsed = {}
            for key, value in row.items():
                if value is None:
                    parsed[key] = None
                    continue
                val = value.strip()
                if key in NUM_FIELDS.get(kind, []):
                    parsed[key] = float(val) if val != '' else None
                elif key in BOOL_FIELDS.get(kind, []):
                    parsed[key] = val.lower() == 'true'
                else:
                    parsed[key] = val
            rows.append(parsed)
    return rows


def main():
    receipts = parse_csv(RECEIPTS_CSV, 'receipts')
    line_items = parse_csv(LINE_ITEMS_CSV, 'line_items')

    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'receipts': receipts,
        'line_items': line_items,
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    print(f'Wrote {OUTPUT_JSON}')


if __name__ == '__main__':
    main()
