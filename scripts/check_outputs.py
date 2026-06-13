from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
DATA_PATH = OUTPUTS / "google_trends_data.json"
HTML_PATH = OUTPUTS / "index.html"


def fail(message: str) -> None:
    raise SystemExit(f"[validation failed] {message}")


def main() -> None:
    if not DATA_PATH.exists():
        fail(f"missing {DATA_PATH}")
    if not HTML_PATH.exists():
        fail(f"missing {HTML_PATH}")

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    brands = data.get("brands", [])
    if len(brands) != 17:
        fail(f"expected 17 canonical brands, found {len(brands)}")

    for mode in ("single_index", "comparison_index"):
        series = data.get("series", {}).get(mode, {})
        if set(series) != {brand["id"] for brand in brands}:
            fail(f"{mode} brand ids do not match canonical brand list")
        lengths = {len(rows) for rows in series.values()}
        if len(lengths) != 1:
            fail(f"{mode} has inconsistent series lengths: {sorted(lengths)}")
        only_length = next(iter(lengths))
        if only_length < 200:
            fail(f"{mode} has too few weekly points: {only_length}")

    html = HTML_PATH.read_text(encoding="utf-8", errors="ignore")
    if "__DATA__" in html:
        fail("index.html still contains the unrendered __DATA__ placeholder")
    if "Google Trends Clinic Dashboard" not in html:
        fail("index.html does not look like the dashboard")

    print("[validation ok] outputs are complete and deployable")


if __name__ == "__main__":
    main()
