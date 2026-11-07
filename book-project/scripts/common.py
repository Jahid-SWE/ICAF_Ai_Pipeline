"""Shared helpers for the book-project scripts: paths and the log.csv writer."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "pages"
WORK_DIR = ROOT / "work"
LOG_PATH = ROOT / "log.csv"

LOG_FIELDS = [
    "page", "status", "confidence", "coverage", "crop_ssim",
    "text_agreement", "text_layer", "attempts", "note",
]


def read_log_row(page: str) -> dict:
    """Return the log.csv row for `page`, or {} if it has none."""
    if LOG_PATH.is_file():
        with LOG_PATH.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["page"] == page:
                    return row
    return {}


def page_name(page_number: int, width: int = 3) -> str:
    return f"page-{page_number:0{width}d}"


def update_log(page: str, **fields) -> None:
    """Add or update the row for `page` (e.g. 'page-001') in log.csv.

    Only the fields given are changed; other columns keep their old value.
    """
    unknown = set(fields) - set(LOG_FIELDS)
    if unknown:
        raise ValueError(f"Unknown log.csv column(s): {sorted(unknown)}")

    rows = {}
    if LOG_PATH.is_file():
        with LOG_PATH.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows[row["page"]] = row

    row = rows.get(page) or {k: "" for k in LOG_FIELDS}
    row["page"] = page
    for key, value in fields.items():
        row[key] = "" if value is None else str(value)
    rows[page] = {k: row.get(k, "") for k in LOG_FIELDS}

    with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
        for name in sorted(rows):
            writer.writerow(rows[name])
