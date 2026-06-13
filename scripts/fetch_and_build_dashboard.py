from __future__ import annotations

import csv
import json
import math
import statistics
import time
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
START_DATE = "2022-01-01"
TIMEZONE = ZoneInfo("Asia/Bangkok")
END_DATE = datetime.now(TIMEZONE).date().isoformat()
GEO = "TH"
TZ_MINUTES = "-420"
HL = "en-US"
FETCHED_AT = datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Brand:
    id: str
    canonical: str
    aliases: tuple[str, ...]
    source_note: str
    source_url: str | None = None
    caveat: str | None = None

    @property
    def query(self) -> str:
        return " + ".join(self.aliases)

    @property
    def trends_url(self) -> str:
        q = urllib.parse.quote(self.query)
        date_range = urllib.parse.quote(f"{START_DATE} {END_DATE}")
        return f"https://trends.google.com/trends/explore?date={date_range}&geo={GEO}&q={q}"


BRANDS: list[Brand] = [
    Brand(
        "the_kliniq",
        "THE KLINIQ",
        ("THE KLINIQ", "THE KLINIQUE", "เดอะคลีนิกค์", "เดอะคลินิก", "เดอะคลีนิค"),
        "Official website text uses THE KLINIQUE and เดอะคลีนิกค์; user canonical kept as THE KLINIQ.",
        "https://www.theklinique.com/",
    ),
    Brand(
        "kliniq_surgery",
        "KLINIQ Surgery",
        ("KLINIQ Surgery", "THE KLINIQUE Surgery", "Klinique Surgery", "เดอะคลีนิกค์ ศัลยกรรม"),
        "Surgery wording appears on THE KLINIQUE official service navigation; long Thai surgery-center phrase omitted from the Trends query because it triggers a Google Trends bad-request response.",
        "https://www.theklinique.com/",
    ),
    Brand(
        "labx",
        "LABX",
        ("LABX", "LABX Clinic", "LAB X Clinic", "แล็บเอ็กซ์", "แลบเอ็กซ์"),
        "Seeded from user-provided brand plus Thai/English spelling variants; official source not verified in this run.",
        None,
        "Low-volume or generic lab wording can create zeros/noise.",
    ),
    Brand(
        "l_clinic",
        "L clinic",
        ("L Clinic", "L clinic", "แอลคลินิก", "แอล คลินิก"),
        "Seeded from user-provided brand plus Thai/English spelling variants.",
        None,
        "Very generic name; results may include unrelated clinics.",
    ),
    Brand(
        "acne_lab",
        "Acne lab",
        ("Acne Lab", "Acne Lab Clinic", "Acnelab", "แอคเน่แลบ", "แอคเน่ แล็บ"),
        "Seeded from user-provided brand plus Thai/English spelling variants.",
        None,
        "Generic acne wording can include non-brand search intent.",
    ),
    Brand(
        "aura_bangkok",
        "AURA Bangkok clinic",
        ("Aura Bangkok Clinic", "Aura Bangkok", "ออร่า แบงคอก คลินิก", "ออร่าแบงคอก", "ออร่า Bangkok"),
        "Official website title and page text use Aura Bangkok Clinic.",
        "https://aurabangkokclinic.com/",
    ),
    Brand(
        "aura_xpress",
        "Aura Xpress",
        ("Aura Xpress", "Aura Express", "Aura Xpress Clinic", "ออร่า เอ็กซ์เพรส", "ออร่า เอ็กซ์เพรส คลินิก"),
        "Seeded from user-provided brand plus common Xpress/Express spelling variants.",
        None,
    ),
    Brand(
        "vsquare",
        "Vsquare",
        ("V Square Clinic", "VSquare Clinic", "V Square", "วีสแควร์คลินิก", "วี สแควร์ คลินิก"),
        "Official website title and page text use V Square Clinic.",
        "https://www.vsquareclinic.com/",
    ),
    Brand(
        "slc",
        "SLC",
        ("SLC Clinic", "SLC Hospital", "SLC คลินิก", "เอสแอลซี คลินิก", "SLC Clinics Hospital"),
        "Official website title uses SLC(Clinics&Hospital).",
        "https://www.slcclinic.com/",
        "Acronym can include non-clinic meanings; clinic/hospital aliases reduce but do not remove noise.",
    ),
    Brand(
        "apex",
        "APEX",
        ("APEX Clinic", "APEX Medical Center", "Apex Profound Beauty", "เอเพ็กซ์ คลินิก", "เอเพ็กซ์"),
        "Official website title uses APEX Hospital & Clinic and Apex Beauty.",
        "https://www.apexprofoundbeauty.com/",
        "APEX is generic outside beauty clinics; clinic/medical aliases are included.",
    ),
    Brand(
        "kkc",
        "KKC clinic",
        ("KKC Clinic", "KKC คลินิก", "เคเคซี คลินิก", "เคเคซีคลินิก"),
        "Seeded from user-provided brand plus Thai/English spelling variants; official source not verified in this run.",
        None,
        "Acronym can include unrelated meanings.",
    ),
    Brand(
        "pornkasem",
        "พรเกษม",
        ("พรเกษม", "พรเกษมคลินิก", "พรเกษม คลินิก", "Pornkasem Clinic", "Pornkasem"),
        "Official website uses พรเกษม and Pornkasem.",
        "https://www.pornkasemclinic.com/",
    ),
    Brand(
        "gangnam",
        "Gangnam clinic",
        ("Gangnam Clinic", "Gangnam Consult", "กังนัมคลินิก", "กังนัม คลินิก"),
        "Official website title uses Gangnam Clinic.",
        "https://www.gangnamconsult.com/",
    ),
    Brand(
        "souel",
        "Souel clinic",
        ("Souel Clinic", "Seoul Clinic", "Seoul Clinic Thailand", "โซลคลินิก", "โซล คลินิก"),
        "User spelling retained; Seoul spelling added as likely English variant.",
        None,
        "Spelling is ambiguous: user wrote Souel; Seoul is included as a likely variant and should be reviewed.",
    ),
    Brand(
        "romrawin",
        "Romrawin",
        ("Romrawin Clinic", "Romrawin", "รมย์รวินท์", "รมย์รวินท์คลินิก", "รมย์รวินท์ คลินิก"),
        "Official website title uses รมย์รวินท์คลินิก.",
        "https://www.romrawin.com/",
    ),
    Brand(
        "nitipon",
        "นิติพล",
        ("นิติพล", "นิติพลคลินิก", "นิติพล คลินิก", "Nitipon Clinic", "Nitipon"),
        "Seeded from user-provided Thai name plus common English spelling.",
        None,
    ),
    Brand(
        "ritz",
        "THE RITZ clinic",
        ("THE RITZ Clinic", "The Ritz Clinic", "Ritz Clinic", "เดอะริทซ์คลินิก", "เดอะ ริทซ์ คลินิก"),
        "Seeded from user-provided brand plus Thai/English spelling variants.",
        None,
        "Ritz can include hotel/non-clinic intent; clinic aliases are included.",
    ),
]


class TrendsClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
            "Referer": "https://trends.google.com/trends/",
        }
        self.session.get("https://trends.google.com/trends/", headers=self.headers, timeout=25)

    @staticmethod
    def _strip_json_prefix(text: str) -> Any:
        idx = text.find("{")
        if idx < 0:
            raise ValueError(f"Google Trends response did not contain JSON: {text[:80]}")
        return json.loads(text[idx:])

    def _get_json(self, url: str, params: dict[str, Any], label: str) -> Any:
        last_error: Exception | None = None
        for attempt in range(1, 6):
            try:
                response = self.session.get(url, params=params, headers=self.headers, timeout=35)
                if response.status_code == 429:
                    wait = min(90, 12 * attempt)
                    print(f"[429] Google Trends quota throttle for {label}; waiting {wait}s")
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                return self._strip_json_prefix(response.text)
            except Exception as exc:  # noqa: BLE001 - keep fetch resilient and log context.
                last_error = exc
                wait = min(60, 5 * attempt)
                print(f"[retry {attempt}] {label}: {exc}; waiting {wait}s")
                time.sleep(wait)
        raise RuntimeError(f"Failed to fetch {label}: {last_error}")

    def interest_over_time(self, keywords: list[str], label: str) -> dict[str, Any]:
        comparison_items = [
            {"keyword": keyword, "geo": GEO, "time": f"{START_DATE} {END_DATE}"}
            for keyword in keywords
        ]
        explore_req = {
            "comparisonItem": comparison_items,
            "category": 0,
            "property": "",
        }
        explore = self._get_json(
            "https://trends.google.com/trends/api/explore",
            {
                "hl": HL,
                "tz": TZ_MINUTES,
                "req": json.dumps(explore_req, separators=(",", ":"), ensure_ascii=False),
            },
            f"explore {label}",
        )
        time.sleep(1.0)

        widgets = explore.get("widgets", [])
        timeseries = next((w for w in widgets if w.get("id") == "TIMESERIES"), None)
        if not timeseries:
            raise RuntimeError(f"No TIMESERIES widget returned for {label}")

        multiline = self._get_json(
            "https://trends.google.com/trends/api/widgetdata/multiline",
            {
                "hl": HL,
                "tz": TZ_MINUTES,
                "req": json.dumps(timeseries["request"], separators=(",", ":"), ensure_ascii=False),
                "token": timeseries["token"],
            },
            f"timeline {label}",
        )
        time.sleep(1.0)
        return multiline


def parse_series(payload: dict[str, Any], names: list[str]) -> dict[str, list[dict[str, Any]]]:
    rows = payload.get("default", {}).get("timelineData", [])
    output = {name: [] for name in names}
    for item in rows:
        week_start = datetime.fromtimestamp(int(item["time"]), tz=timezone.utc).date().isoformat()
        formatted = item.get("formattedTime", week_start)
        values = item.get("value", [])
        partials = item.get("isPartial", [False] * len(values))
        for idx, name in enumerate(names):
            value = values[idx] if idx < len(values) else None
            output[name].append(
                {
                    "date": week_start,
                    "period": formatted,
                    "value": None if value is None else float(value),
                    "is_partial": bool(partials[idx]) if isinstance(partials, list) and idx < len(partials) else bool(item.get("isPartial", False)),
                }
            )
    return output


def avg(values: list[float]) -> float | None:
    clean = [v for v in values if v is not None and math.isfinite(v)]
    if not clean:
        return None
    return float(sum(clean) / len(clean))


def latest_non_null(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    for row in reversed(rows):
        if row.get("value") is not None:
            return row
    return None


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    values = [float(r["value"]) for r in rows if r.get("value") is not None]
    latest = latest_non_null(rows)
    last_13 = [float(r["value"]) for r in rows[-13:] if r.get("value") is not None]
    prev_13 = [float(r["value"]) for r in rows[-26:-13] if r.get("value") is not None]
    latest_idx = next((idx for idx in range(len(rows) - 1, -1, -1) if rows[idx].get("value") is not None), None)
    yoy = None
    if latest_idx is not None and latest_idx - 52 >= 0:
        latest_value = rows[latest_idx]["value"]
        prior_value = rows[latest_idx - 52]["value"]
        if latest_value is not None and prior_value not in (None, 0):
            yoy = (float(latest_value) - float(prior_value)) / float(prior_value) * 100
    peak = max((r for r in rows if r.get("value") is not None), key=lambda r: r["value"], default=None)
    avg_13 = avg(last_13)
    prev_avg_13 = avg(prev_13)
    mom_13 = None
    if avg_13 is not None and prev_avg_13 not in (None, 0):
        mom_13 = (avg_13 - prev_avg_13) / prev_avg_13 * 100
    return {
        "latest_date": latest["date"] if latest else None,
        "latest_period": latest["period"] if latest else None,
        "latest_value": latest["value"] if latest else None,
        "avg_13w": avg_13,
        "change_13w_vs_prev_13w_pct": mom_13,
        "yoy_pct": yoy,
        "peak_date": peak["date"] if peak else None,
        "peak_period": peak["period"] if peak else None,
        "peak_value": peak["value"] if peak else None,
        "nonzero_weeks": sum(1 for v in values if v > 0),
        "weeks": len(rows),
        "mean": avg(values),
        "median": statistics.median(values) if values else None,
    }


def build_single_series(client: TrendsClient) -> dict[str, list[dict[str, Any]]]:
    single: dict[str, list[dict[str, Any]]] = {}
    for idx, brand in enumerate(BRANDS, 1):
        print(f"[single {idx}/{len(BRANDS)}] {brand.canonical}")
        payload = client.interest_over_time([brand.query], f"single {brand.canonical}")
        parsed = parse_series(payload, [brand.id])
        single[brand.id] = parsed[brand.id]
    return single


def build_comparison_series(client: TrendsClient) -> dict[str, list[dict[str, Any]]]:
    anchor = BRANDS[0]
    others = [b for b in BRANDS if b.id != anchor.id]
    chunks = [others[i : i + 4] for i in range(0, len(others), 4)]
    raw_by_brand: dict[str, list[dict[str, Any]]] = {}
    base_anchor: list[float] | None = None

    for chunk_idx, chunk in enumerate(chunks, 1):
        group = [anchor, *chunk]
        print(f"[compare group {chunk_idx}/{len(chunks)}] " + ", ".join(b.canonical for b in group))
        payload = client.interest_over_time([b.query for b in group], f"compare group {chunk_idx}")
        parsed = parse_series(payload, [b.id for b in group])
        group_anchor = [float(r["value"]) for r in parsed[anchor.id] if r.get("value") is not None]

        if base_anchor is None:
            base_anchor = group_anchor
            scale = 1.0
            raw_by_brand[anchor.id] = parsed[anchor.id]
        else:
            ratios = []
            for base, current in zip(base_anchor, group_anchor):
                if current > 0:
                    ratios.append(base / current)
            scale = statistics.median(ratios) if ratios else 1.0

        for brand in group:
            if brand.id == anchor.id and chunk_idx > 1:
                continue
            scaled_rows = []
            for row in parsed[brand.id]:
                value = row["value"]
                scaled_rows.append(
                    {
                        **row,
                        "value": None if value is None else float(value) * scale,
                        "anchor_scale": scale,
                    }
                )
            raw_by_brand[brand.id] = scaled_rows

    global_max = max(
        (row["value"] for rows in raw_by_brand.values() for row in rows if row.get("value") is not None),
        default=0,
    )
    if global_max <= 0:
        return raw_by_brand

    normalized: dict[str, list[dict[str, Any]]] = {}
    for brand_id, rows in raw_by_brand.items():
        normalized[brand_id] = [
            {
                **row,
                "value": None if row["value"] is None else round(float(row["value"]) / global_max * 100, 4),
            }
            for row in rows
        ]
    return normalized


def write_csvs(single: dict[str, list[dict[str, Any]]], comparison: dict[str, list[dict[str, Any]]]) -> None:
    weekly_path = OUTPUTS / "google_trends_weekly.csv"
    with weekly_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["canonical", "brand_id", "mode", "date", "period", "value", "is_partial"],
        )
        writer.writeheader()
        for mode, dataset in (("single_index", single), ("comparison_index", comparison)):
            for brand in BRANDS:
                for row in dataset.get(brand.id, []):
                    writer.writerow(
                        {
                            "canonical": brand.canonical,
                            "brand_id": brand.id,
                            "mode": mode,
                            "date": row["date"],
                            "period": row["period"],
                            "value": row["value"],
                            "is_partial": row.get("is_partial", False),
                        }
                    )

    alias_path = OUTPUTS / "alias_map.csv"
    with alias_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["canonical", "brand_id", "alias", "source_note", "source_url", "caveat", "trends_url"],
        )
        writer.writeheader()
        for brand in BRANDS:
            for alias in brand.aliases:
                writer.writerow(
                    {
                        "canonical": brand.canonical,
                        "brand_id": brand.id,
                        "alias": alias,
                        "source_note": brand.source_note,
                        "source_url": brand.source_url or "",
                        "caveat": brand.caveat or "",
                        "trends_url": brand.trends_url,
                    }
                )


def dashboard_payload(single: dict[str, list[dict[str, Any]]], comparison: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    brands = []
    for brand in BRANDS:
        brands.append(
            {
                "id": brand.id,
                "canonical": brand.canonical,
                "aliases": list(brand.aliases),
                "query": brand.query,
                "source_note": brand.source_note,
                "source_url": brand.source_url,
                "caveat": brand.caveat,
                "trends_url": brand.trends_url,
                "metrics": compute_metrics(single.get(brand.id, [])),
                "comparison_metrics": compute_metrics(comparison.get(brand.id, [])),
            }
        )
    return {
        "metadata": {
            "title": "Google Trends Beauty Clinic Dashboard",
            "geo": GEO,
            "geo_label": "Thailand",
            "start_date": START_DATE,
            "end_date": END_DATE,
            "fetched_at_utc": FETCHED_AT,
            "grain": "weekly",
            "source": "Google Trends",
            "source_url": "https://trends.google.com/trends/",
            "methodology": [
                "Each canonical brand is represented by an alias expression joined with '+', which Google Trends parses as multiple broad keywords within one comparison item.",
                "single_index is the standard Google Trends 0-100 index for each canonical alias group, normalized within that brand over the selected time range.",
                "comparison_index is anchored through THE KLINIQ because Google Trends direct comparison is limited to small groups; groups were rescaled using the shared THE KLINIQ series and then normalized to the cross-brand maximum.",
                "The data is weekly, Thailand-only, web search, all categories, from 2022-01-01 through 2026-06-13.",
            ],
            "limitations": [
                "Google Trends values are relative indices, not absolute search volumes.",
                "Low-volume terms can return zeros due to rounding/privacy thresholds.",
                "Generic names such as APEX, SLC, L Clinic, Acne Lab, Ritz, and acronym-style brands can include non-brand intent despite clinic aliases.",
                "Alias mapping is a query design, not a legal-brand verification table; review ambiguous names before making investment decisions.",
            ],
        },
        "brands": brands,
        "series": {
            "single_index": single,
            "comparison_index": comparison,
        },
        "sources": [
            {
                "title": "Google Trends",
                "url": "https://trends.google.com/trends/",
                "publication_date": "Live service; extracted 2026-06-13",
                "used_for": "Weekly Thailand search-interest source data.",
            },
            {
                "title": "THE KLINIQUE official website",
                "url": "https://www.theklinique.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for THE KLINIQUE / เดอะคลีนิกค์ and surgery wording.",
            },
            {
                "title": "Aura Bangkok Clinic official website",
                "url": "https://aurabangkokclinic.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for Aura Bangkok Clinic.",
            },
            {
                "title": "V Square Clinic official website",
                "url": "https://www.vsquareclinic.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for V Square Clinic.",
            },
            {
                "title": "SLC Clinic official website",
                "url": "https://www.slcclinic.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for SLC Clinics & Hospital.",
            },
            {
                "title": "APEX Profound Beauty official website",
                "url": "https://www.apexprofoundbeauty.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for APEX Hospital & Clinic / Apex Beauty.",
            },
            {
                "title": "Pornkasem Clinic official website",
                "url": "https://www.pornkasemclinic.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for พรเกษม / Pornkasem.",
            },
            {
                "title": "Gangnam Clinic official website",
                "url": "https://www.gangnamconsult.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for Gangnam Clinic.",
            },
            {
                "title": "Romrawin official website",
                "url": "https://www.romrawin.com/",
                "publication_date": "Live website; retrieved 2026-06-13",
                "used_for": "Alias sanity check for Romrawin / รมย์รวินท์.",
            },
        ],
    }


HTML_TEMPLATE = r"""<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Google Trends Clinic Dashboard</title>
  <style>
    :root {
      --bg: #f7f8fa;
      --surface: #ffffff;
      --ink: #17202a;
      --muted: #607080;
      --line: #d9e0e8;
      --accent: #0f766e;
      --accent-2: #b45309;
      --accent-3: #2563eb;
      --danger: #b91c1c;
      --shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
      --radius: 8px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: "Segoe UI", Tahoma, Arial, sans-serif;
      line-height: 1.45;
    }
    header {
      background: #10232f;
      color: #fff;
      padding: 18px 24px 16px;
      border-bottom: 4px solid #eab308;
    }
    h1 {
      margin: 0 0 8px;
      font-size: 24px;
      letter-spacing: 0;
      font-weight: 700;
    }
    .subhead {
      margin: 0;
      color: #cbd5e1;
      font-size: 13px;
    }
    main {
      width: min(1500px, calc(100vw - 32px));
      margin: 18px auto 32px;
    }
    .toolbar {
      display: grid;
      grid-template-columns: 1.1fr 1fr 1fr auto;
      gap: 10px;
      align-items: end;
      margin-bottom: 14px;
    }
    .control {
      display: grid;
      gap: 5px;
    }
    label {
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
    }
    select, input[type="search"], button {
      height: 38px;
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--ink);
      border-radius: 6px;
      padding: 0 11px;
      font: inherit;
    }
    button {
      cursor: pointer;
      font-weight: 700;
      background: #0f766e;
      color: #fff;
      border-color: #0f766e;
      white-space: nowrap;
    }
    button.secondary {
      color: var(--ink);
      background: var(--surface);
      border-color: var(--line);
    }
    button:focus, select:focus, input:focus {
      outline: 2px solid #38bdf8;
      outline-offset: 2px;
    }
    .tabs {
      display: flex;
      gap: 8px;
      margin: 8px 0 16px;
      flex-wrap: wrap;
    }
    .tab {
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--ink);
      border-radius: 6px;
      height: 36px;
      padding: 0 13px;
    }
    .tab.active {
      background: #10232f;
      color: #fff;
      border-color: #10232f;
    }
    .panel {
      display: none;
    }
    .panel.active {
      display: block;
    }
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(140px, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }
    .metric {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 12px;
      min-height: 88px;
    }
    .metric .label {
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 7px;
    }
    .metric .value {
      font-size: 24px;
      font-weight: 750;
    }
    .metric .note {
      color: var(--muted);
      font-size: 12px;
      margin-top: 5px;
    }
    .chart-shell, .section {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 14px;
      margin-bottom: 14px;
    }
    .chart-head {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 12px;
      margin-bottom: 8px;
    }
    .chart-title {
      font-size: 17px;
      font-weight: 750;
      margin: 0;
    }
    .chart-caption {
      color: var(--muted);
      margin: 3px 0 0;
      font-size: 12px;
    }
    canvas {
      width: 100%;
      display: block;
      border: 1px solid #edf1f5;
      border-radius: 6px;
      background: #fff;
    }
    #singleChart, #compareChart { height: 420px; }
    .mini-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }
    .mini-card {
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 10px;
      background: var(--surface);
      min-width: 0;
    }
    .mini-card h3 {
      margin: 0 0 3px;
      font-size: 14px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .mini-card .mini-meta {
      color: var(--muted);
      font-size: 11px;
      min-height: 32px;
    }
    .mini-card canvas {
      height: 150px;
      margin-top: 8px;
    }
    .compare-grid {
      display: grid;
      grid-template-columns: 300px 1fr;
      gap: 14px;
      align-items: start;
    }
    .checkbox-list {
      display: grid;
      gap: 7px;
      max-height: 520px;
      overflow: auto;
      padding-right: 5px;
    }
    .check-row {
      display: grid;
      grid-template-columns: 18px 1fr;
      gap: 8px;
      align-items: start;
      padding: 8px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fbfcfd;
    }
    .check-row span {
      display: block;
      font-size: 13px;
      font-weight: 650;
    }
    .check-row small {
      color: var(--muted);
      display: block;
      margin-top: 1px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    th, td {
      border-bottom: 1px solid var(--line);
      padding: 8px 7px;
      text-align: left;
      vertical-align: top;
    }
    th {
      color: var(--muted);
      font-weight: 700;
      background: #f8fafc;
      position: sticky;
      top: 0;
      z-index: 1;
    }
    .table-wrap {
      max-height: 560px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 6px;
    }
    .pill {
      display: inline-block;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 3px 7px;
      margin: 2px 3px 2px 0;
      font-size: 11px;
      background: #f8fafc;
      color: #334155;
    }
    .source-list {
      display: grid;
      gap: 8px;
      font-size: 13px;
      color: #334155;
    }
    .source-list a { color: #0f766e; }
    .warning {
      border-left: 4px solid #eab308;
      background: #fffbeb;
      padding: 10px 12px;
      border-radius: 6px;
      color: #554000;
      margin: 0 0 12px;
      font-size: 13px;
    }
    .tooltip {
      position: fixed;
      display: none;
      background: #111827;
      color: #fff;
      padding: 8px 9px;
      border-radius: 6px;
      font-size: 12px;
      max-width: 260px;
      pointer-events: none;
      z-index: 20;
      box-shadow: var(--shadow);
    }
    .empty {
      color: var(--muted);
      padding: 20px;
      text-align: center;
    }
    @media (max-width: 1050px) {
      .toolbar { grid-template-columns: 1fr 1fr; }
      .summary-grid { grid-template-columns: repeat(2, minmax(140px, 1fr)); }
      .mini-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .compare-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 640px) {
      main { width: min(100vw - 18px, 1500px); margin-top: 10px; }
      header { padding: 14px 12px; }
      h1 { font-size: 20px; }
      .toolbar { grid-template-columns: 1fr; }
      .summary-grid { grid-template-columns: 1fr; }
      .mini-grid { grid-template-columns: 1fr; }
      #singleChart, #compareChart { height: 330px; }
      .chart-head { display: block; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Google Trends Clinic Dashboard</h1>
    <p class="subhead">Thailand weekly search interest, 2022-01-01 to 2026-06-13. Data source: Google Trends. Extracted: <span id="fetchedAt"></span>.</p>
  </header>

  <main>
    <div class="warning">
      Google Trends เป็นดัชนีเชิงสัมพัทธ์ ไม่ใช่จำนวน search volume จริง. ชื่อที่ทั่วไปมาก เช่น APEX, SLC, L Clinic, Acne Lab และ Ritz อาจมี noise จาก intent อื่น แม้จะใส่ alias คำว่า clinic แล้ว.
    </div>

    <div class="toolbar">
      <div class="control">
        <label for="brandSelect">ดูรายชื่อเดี่ยว</label>
        <select id="brandSelect"></select>
      </div>
      <div class="control">
        <label for="searchBox">กรอง mini charts / table</label>
        <input id="searchBox" type="search" placeholder="พิมพ์ชื่อ เช่น Romrawin, พรเกษม, APEX">
      </div>
      <div class="control">
        <label for="sortSelect">เรียงตาราง</label>
        <select id="sortSelect">
          <option value="latest_desc">Latest index สูงสุด</option>
          <option value="avg13_desc">13-week average สูงสุด</option>
          <option value="yoy_desc">YoY สูงสุด</option>
          <option value="name_asc">ชื่อ A-Z</option>
        </select>
      </div>
      <button id="downloadCsv">Download CSV</button>
    </div>

    <div class="tabs" role="tablist" aria-label="Dashboard tabs">
      <button class="tab active" data-tab="singlePanel">รายชื่อเดี่ยว</button>
      <button class="tab" data-tab="comparePanel">เปรียบเทียบ</button>
      <button class="tab" data-tab="allPanel">กราฟแยกทั้งหมด</button>
      <button class="tab" data-tab="dataPanel">ตารางและแหล่งข้อมูล</button>
    </div>

    <section id="singlePanel" class="panel active">
      <div class="summary-grid" id="metricCards"></div>
      <div class="chart-shell">
        <div class="chart-head">
          <div>
            <h2 class="chart-title" id="singleTitle"></h2>
            <p class="chart-caption" id="singleCaption"></p>
          </div>
          <button class="secondary" id="openTrends">Open in Google Trends</button>
        </div>
        <canvas id="singleChart"></canvas>
      </div>
      <div class="section">
        <h2 class="chart-title">Aliases Used</h2>
        <p class="chart-caption" id="aliasNote"></p>
        <div id="aliasPills"></div>
      </div>
    </section>

    <section id="comparePanel" class="panel">
      <div class="compare-grid">
        <div class="section">
          <h2 class="chart-title">เลือกชื่อเพื่อเปรียบเทียบ</h2>
          <p class="chart-caption">ค่าในกราฟนี้ใช้ comparison_index ที่ normalize ข้ามแบรนด์ผ่าน THE KLINIQ anchor. ค่าเหมาะสำหรับดู direction และ relative attention ไม่ใช่ absolute search volume.</p>
          <div style="display:flex; gap:8px; margin:10px 0;">
            <button class="secondary" id="selectTop5">Top 5</button>
            <button class="secondary" id="clearCompare">Clear</button>
          </div>
          <div class="checkbox-list" id="compareChecks"></div>
        </div>
        <div class="chart-shell">
          <div class="chart-head">
            <div>
              <h2 class="chart-title">Comparison View</h2>
              <p class="chart-caption">Cross-brand index, anchored/rescaled; hover for weekly value.</p>
            </div>
          </div>
          <canvas id="compareChart"></canvas>
        </div>
      </div>
    </section>

    <section id="allPanel" class="panel">
      <div class="section">
        <h2 class="chart-title">กราฟแยก: 1 ชื่อ ต่อ 1 กราฟ</h2>
        <p class="chart-caption">แต่ละ mini chart เป็น single_index 0-100 ของแบรนด์นั้นเอง จึงดูแรงค้นหาภายในแบรนด์ได้ดี แต่ไม่ควรเทียบระดับดัชนีข้ามแบรนด์โดยตรง.</p>
      </div>
      <div class="mini-grid" id="miniGrid"></div>
    </section>

    <section id="dataPanel" class="panel">
      <div class="section">
        <h2 class="chart-title">Metric Table</h2>
        <div class="table-wrap">
          <table id="metricTable">
            <thead>
              <tr>
                <th>Canonical</th>
                <th>Latest</th>
                <th>13W Avg</th>
                <th>YoY</th>
                <th>Peak</th>
                <th>Non-zero Weeks</th>
                <th>Aliases</th>
                <th>Source / Caveat</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
      <div class="section">
        <h2 class="chart-title">Methodology</h2>
        <div id="methodology"></div>
      </div>
      <div class="section">
        <h2 class="chart-title">Sources</h2>
        <div class="source-list" id="sources"></div>
      </div>
    </section>
  </main>
  <div id="tooltip" class="tooltip"></div>

  <script>
    const DATA = __DATA__;
    const COLORS = [
      '#0f766e', '#2563eb', '#b45309', '#7c3aed', '#dc2626', '#0891b2',
      '#65a30d', '#c2410c', '#9333ea', '#be123c', '#0d9488', '#4f46e5',
      '#a16207', '#15803d', '#1d4ed8', '#b91c1c', '#475569', '#0369a1'
    ];
    const brandById = Object.fromEntries(DATA.brands.map(b => [b.id, b]));
    const tooltip = document.getElementById('tooltip');

    function fmtNum(v, digits = 1) {
      if (v === null || v === undefined || Number.isNaN(v)) return 'n/a';
      return Number(v).toLocaleString('en-US', { maximumFractionDigits: digits, minimumFractionDigits: digits });
    }
    function fmtPct(v) {
      if (v === null || v === undefined || Number.isNaN(v)) return 'n/a';
      const sign = v > 0 ? '+' : '';
      return sign + fmtNum(v, 1) + '%';
    }
    function escapeHtml(s) {
      return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }
    function seriesFor(mode, brandId) {
      return (DATA.series[mode] && DATA.series[mode][brandId]) || [];
    }
    function filteredBrands() {
      const q = document.getElementById('searchBox').value.trim().toLowerCase();
      if (!q) return DATA.brands.slice();
      return DATA.brands.filter(b => {
        const hay = [b.canonical, b.query, ...(b.aliases || [])].join(' ').toLowerCase();
        return hay.includes(q);
      });
    }

    function setupControls() {
      document.getElementById('fetchedAt').textContent = DATA.metadata.fetched_at_utc;
      const select = document.getElementById('brandSelect');
      select.innerHTML = DATA.brands.map(b => `<option value="${b.id}">${escapeHtml(b.canonical)}</option>`).join('');
      select.addEventListener('change', () => renderSingle(select.value));
      document.getElementById('searchBox').addEventListener('input', () => { renderMiniGrid(); renderTable(); });
      document.getElementById('sortSelect').addEventListener('change', renderTable);
      document.querySelectorAll('.tab').forEach(button => {
        button.addEventListener('click', () => {
          document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
          document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
          button.classList.add('active');
          document.getElementById(button.dataset.tab).classList.add('active');
          setTimeout(() => {
            renderSingle(document.getElementById('brandSelect').value);
            renderCompare();
            renderMiniGrid();
          }, 20);
        });
      });
      document.getElementById('downloadCsv').addEventListener('click', downloadCsv);
      document.getElementById('openTrends').addEventListener('click', () => {
        const brand = brandById[select.value];
        window.open(brand.trends_url, '_blank', 'noopener');
      });
      document.getElementById('selectTop5').addEventListener('click', () => {
        const top = DATA.brands
          .slice()
          .sort((a, b) => (b.comparison_metrics.avg_13w || 0) - (a.comparison_metrics.avg_13w || 0))
          .slice(0, 5)
          .map(b => b.id);
        document.querySelectorAll('[name="compareBrand"]').forEach(cb => cb.checked = top.includes(cb.value));
        renderCompare();
      });
      document.getElementById('clearCompare').addEventListener('click', () => {
        document.querySelectorAll('[name="compareBrand"]').forEach(cb => cb.checked = false);
        renderCompare();
      });
    }

    function renderCards(brand) {
      const m = brand.metrics;
      const rows = [
        ['Latest single index', fmtNum(m.latest_value, 0), m.latest_period || 'latest weekly point'],
        ['13-week average', fmtNum(m.avg_13w, 1), fmtPct(m.change_13w_vs_prev_13w_pct) + ' vs prior 13W'],
        ['YoY', fmtPct(m.yoy_pct), 'latest week vs 52 weeks earlier'],
        ['Peak week', fmtNum(m.peak_value, 0), m.peak_period || 'n/a'],
        ['Non-zero weeks', `${m.nonzero_weeks || 0}/${m.weeks || 0}`, 'low-volume terms may round to zero']
      ];
      document.getElementById('metricCards').innerHTML = rows.map(([label, value, note]) => `
        <div class="metric"><div class="label">${escapeHtml(label)}</div><div class="value">${escapeHtml(value)}</div><div class="note">${escapeHtml(note)}</div></div>
      `).join('');
    }

    function renderSingle(brandId) {
      const brand = brandById[brandId] || DATA.brands[0];
      document.getElementById('singleTitle').textContent = brand.canonical;
      document.getElementById('singleCaption').textContent = 'single_index: Google Trends 0-100 within this canonical alias group.';
      document.getElementById('aliasNote').textContent = brand.source_note + (brand.caveat ? ' Caveat: ' + brand.caveat : '');
      document.getElementById('aliasPills').innerHTML = brand.aliases.map(a => `<span class="pill">${escapeHtml(a)}</span>`).join('');
      renderCards(brand);
      drawLineChart(document.getElementById('singleChart'), [
        { label: brand.canonical, color: COLORS[0], rows: seriesFor('single_index', brand.id) }
      ], { yMax: 100, mode: 'single' });
    }

    function drawLineChart(canvas, seriesList, options = {}) {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      const cssWidth = Math.max(320, rect.width || canvas.clientWidth || 800);
      const cssHeight = Math.max(180, rect.height || canvas.clientHeight || 320);
      canvas.width = Math.floor(cssWidth * dpr);
      canvas.height = Math.floor(cssHeight * dpr);
      const ctx = canvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, cssWidth, cssHeight);

      const pad = { left: 48, right: 22, top: 24, bottom: 42 };
      const w = cssWidth - pad.left - pad.right;
      const h = cssHeight - pad.top - pad.bottom;
      const allRows = seriesList.flatMap(s => s.rows || []);
      if (!allRows.length) {
        ctx.fillStyle = '#607080';
        ctx.textAlign = 'center';
        ctx.fillText('No data', cssWidth / 2, cssHeight / 2);
        return;
      }
      const labels = (seriesList[0].rows || []).map(r => r.date);
      const maxVal = options.yMax || Math.max(1, ...seriesList.flatMap(s => (s.rows || []).map(r => r.value || 0)));
      const yMax = options.yMax || Math.ceil(maxVal / 10) * 10;
      const yMin = 0;
      const x = i => pad.left + (labels.length <= 1 ? 0 : (i / (labels.length - 1)) * w);
      const y = v => pad.top + h - ((v - yMin) / (yMax - yMin || 1)) * h;

      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 1;
      ctx.fillStyle = '#607080';
      ctx.font = '11px Segoe UI, Arial';
      ctx.textAlign = 'right';
      for (let i = 0; i <= 5; i++) {
        const val = yMin + (i / 5) * (yMax - yMin);
        const yy = y(val);
        ctx.beginPath();
        ctx.moveTo(pad.left, yy);
        ctx.lineTo(pad.left + w, yy);
        ctx.stroke();
        ctx.fillText(fmtNum(val, 0), pad.left - 8, yy + 4);
      }
      ctx.strokeStyle = '#94a3b8';
      ctx.beginPath();
      ctx.moveTo(pad.left, pad.top);
      ctx.lineTo(pad.left, pad.top + h);
      ctx.lineTo(pad.left + w, pad.top + h);
      ctx.stroke();

      const yearMarks = [];
      labels.forEach((label, i) => {
        const yr = label.slice(0, 4);
        if (i === 0 || labels[i - 1].slice(0, 4) !== yr) yearMarks.push([i, yr]);
      });
      ctx.fillStyle = '#607080';
      ctx.textAlign = 'center';
      yearMarks.forEach(([i, yr]) => ctx.fillText(yr, x(i), pad.top + h + 24));

      seriesList.forEach((series, idx) => {
        const rows = series.rows || [];
        ctx.strokeStyle = series.color || COLORS[idx % COLORS.length];
        ctx.lineWidth = options.mode === 'mini' ? 1.7 : 2.2;
        ctx.beginPath();
        let started = false;
        rows.forEach((row, i) => {
          if (row.value === null || row.value === undefined) return;
          const xx = x(i);
          const yy = y(row.value);
          if (!started) {
            ctx.moveTo(xx, yy);
            started = true;
          } else {
            ctx.lineTo(xx, yy);
          }
        });
        ctx.stroke();
      });

      if (options.mode !== 'mini' && seriesList.length > 1) {
        let legendX = pad.left;
        let legendY = 10;
        ctx.font = '12px Segoe UI, Arial';
        seriesList.forEach((series, idx) => {
          const color = series.color || COLORS[idx % COLORS.length];
          ctx.fillStyle = color;
          ctx.fillRect(legendX, legendY, 10, 10);
          ctx.fillStyle = '#334155';
          ctx.textAlign = 'left';
          const label = series.label;
          ctx.fillText(label, legendX + 14, legendY + 10);
          legendX += Math.min(210, 22 + ctx.measureText(label).width);
          if (legendX > cssWidth - 180) {
            legendX = pad.left;
            legendY += 18;
          }
        });
      }

      canvas.onmousemove = evt => {
        if (options.mode === 'mini') return;
        const bounds = canvas.getBoundingClientRect();
        const mx = evt.clientX - bounds.left;
        const idx = Math.round(((mx - pad.left) / w) * (labels.length - 1));
        if (idx < 0 || idx >= labels.length) {
          tooltip.style.display = 'none';
          return;
        }
        const rows = seriesList.map(s => {
          const row = s.rows[idx];
          return row ? `<div><b style="color:${s.color}">${escapeHtml(s.label)}</b>: ${fmtNum(row.value, 1)}</div>` : '';
        }).join('');
        tooltip.innerHTML = `<div>${escapeHtml(seriesList[0].rows[idx].period || labels[idx])}</div>${rows}`;
        tooltip.style.left = Math.min(evt.clientX + 14, window.innerWidth - 280) + 'px';
        tooltip.style.top = (evt.clientY + 14) + 'px';
        tooltip.style.display = 'block';
      };
      canvas.onmouseleave = () => { tooltip.style.display = 'none'; };
    }

    function setupCompareChecks() {
      const topFive = DATA.brands
        .slice()
        .sort((a, b) => (b.comparison_metrics.avg_13w || 0) - (a.comparison_metrics.avg_13w || 0))
        .slice(0, 5)
        .map(b => b.id);
      document.getElementById('compareChecks').innerHTML = DATA.brands.map((brand, idx) => `
        <label class="check-row">
          <input type="checkbox" name="compareBrand" value="${brand.id}" ${topFive.includes(brand.id) ? 'checked' : ''}>
          <span>${escapeHtml(brand.canonical)}<small>13W avg ${fmtNum(brand.comparison_metrics.avg_13w, 1)}</small></span>
        </label>
      `).join('');
      document.querySelectorAll('[name="compareBrand"]').forEach(cb => cb.addEventListener('change', renderCompare));
    }

    function renderCompare() {
      const selected = [...document.querySelectorAll('[name="compareBrand"]:checked')].map(cb => cb.value);
      const series = selected.map((id, idx) => ({
        label: brandById[id].canonical,
        color: COLORS[idx % COLORS.length],
        rows: seriesFor('comparison_index', id)
      }));
      drawLineChart(document.getElementById('compareChart'), series, { yMax: 100, mode: 'compare' });
    }

    function renderMiniGrid() {
      const grid = document.getElementById('miniGrid');
      const brands = filteredBrands();
      grid.innerHTML = brands.map(brand => `
        <div class="mini-card">
          <h3 title="${escapeHtml(brand.canonical)}">${escapeHtml(brand.canonical)}</h3>
          <div class="mini-meta">Latest ${fmtNum(brand.metrics.latest_value, 0)} | 13W ${fmtNum(brand.metrics.avg_13w, 1)} | YoY ${fmtPct(brand.metrics.yoy_pct)}</div>
          <canvas data-mini="${brand.id}"></canvas>
        </div>
      `).join('') || '<div class="empty">No matching brands.</div>';
      grid.querySelectorAll('canvas[data-mini]').forEach((canvas, idx) => {
        const id = canvas.getAttribute('data-mini');
        drawLineChart(canvas, [{ label: brandById[id].canonical, color: COLORS[idx % COLORS.length], rows: seriesFor('single_index', id) }], { yMax: 100, mode: 'mini' });
      });
    }

    function renderTable() {
      const sort = document.getElementById('sortSelect').value;
      const brands = filteredBrands().slice();
      const sorters = {
        latest_desc: (a, b) => (b.metrics.latest_value || -1) - (a.metrics.latest_value || -1),
        avg13_desc: (a, b) => (b.metrics.avg_13w || -1) - (a.metrics.avg_13w || -1),
        yoy_desc: (a, b) => (b.metrics.yoy_pct || -9999) - (a.metrics.yoy_pct || -9999),
        name_asc: (a, b) => a.canonical.localeCompare(b.canonical)
      };
      brands.sort(sorters[sort] || sorters.latest_desc);
      document.querySelector('#metricTable tbody').innerHTML = brands.map(brand => `
        <tr>
          <td><b>${escapeHtml(brand.canonical)}</b><br><a href="${brand.trends_url}" target="_blank" rel="noopener">Google Trends query</a></td>
          <td>${fmtNum(brand.metrics.latest_value, 0)}<br><small>${escapeHtml(brand.metrics.latest_period || '')}</small></td>
          <td>${fmtNum(brand.metrics.avg_13w, 1)}<br><small>${fmtPct(brand.metrics.change_13w_vs_prev_13w_pct)} vs prior</small></td>
          <td>${fmtPct(brand.metrics.yoy_pct)}</td>
          <td>${fmtNum(brand.metrics.peak_value, 0)}<br><small>${escapeHtml(brand.metrics.peak_period || '')}</small></td>
          <td>${brand.metrics.nonzero_weeks || 0}/${brand.metrics.weeks || 0}</td>
          <td>${brand.aliases.map(a => `<span class="pill">${escapeHtml(a)}</span>`).join('')}</td>
          <td>${escapeHtml(brand.source_note)}${brand.source_url ? `<br><a href="${brand.source_url}" target="_blank" rel="noopener">source</a>` : ''}${brand.caveat ? `<br><b>Caveat:</b> ${escapeHtml(brand.caveat)}` : ''}</td>
        </tr>
      `).join('');
    }

    function renderMethodology() {
      const m = DATA.metadata;
      document.getElementById('methodology').innerHTML = `
        <p><b>Scope:</b> ${escapeHtml(m.geo_label)}, web search, all categories, weekly grain, ${escapeHtml(m.start_date)} to ${escapeHtml(m.end_date)}.</p>
        <ul>${m.methodology.map(x => `<li>${escapeHtml(x)}</li>`).join('')}</ul>
        <p><b>Limitations:</b></p>
        <ul>${m.limitations.map(x => `<li>${escapeHtml(x)}</li>`).join('')}</ul>
      `;
      document.getElementById('sources').innerHTML = DATA.sources.map(src => `
        <div><a href="${src.url}" target="_blank" rel="noopener">${escapeHtml(src.title)}</a> — ${escapeHtml(src.publication_date)}. ${escapeHtml(src.used_for)}</div>
      `).join('');
    }

    function downloadCsv() {
      const rows = [['canonical','mode','date','period','value']];
      for (const mode of ['single_index','comparison_index']) {
        for (const brand of DATA.brands) {
          for (const row of seriesFor(mode, brand.id)) {
            rows.push([brand.canonical, mode, row.date, row.period, row.value]);
          }
        }
      }
      const csv = rows.map(r => r.map(v => `"${String(v ?? '').replaceAll('"', '""')}"`).join(',')).join('\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'google_trends_clinic_dashboard.csv';
      a.click();
      URL.revokeObjectURL(url);
    }

    function renderAll() {
      setupControls();
      setupCompareChecks();
      renderSingle(DATA.brands[0].id);
      renderCompare();
      renderMiniGrid();
      renderTable();
      renderMethodology();
    }
    window.addEventListener('resize', () => {
      renderSingle(document.getElementById('brandSelect').value);
      renderCompare();
      renderMiniGrid();
    });
    renderAll();
  </script>
</body>
</html>
"""


def write_html(payload: dict[str, Any]) -> Path:
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    path = OUTPUTS / "index.html"
    path.write_text(html, encoding="utf-8")
    return path


def write_methodology(payload: dict[str, Any]) -> Path:
    path = OUTPUTS / "methodology.md"
    lines = [
        "# Google Trends Clinic Dashboard Methodology",
        "",
        f"- Generated: {FETCHED_AT}",
        f"- Geography: {GEO} / Thailand",
        f"- Range: {START_DATE} to {END_DATE}",
        f"- Grain: weekly",
        f"- Source: Google Trends <https://trends.google.com/trends/>",
        "",
        "## Methodology",
        "",
    ]
    lines += [f"- {item}" for item in payload["metadata"]["methodology"]]
    lines += ["", "## Limitations", ""]
    lines += [f"- {item}" for item in payload["metadata"]["limitations"]]
    lines += ["", "## Alias Map", ""]
    for brand in payload["brands"]:
        lines.append(f"### {brand['canonical']}")
        lines.append(f"- Query: `{brand['query']}`")
        lines.append(f"- Source note: {brand['source_note']}")
        if brand.get("source_url"):
            lines.append(f"- Source URL: {brand['source_url']}")
        if brand.get("caveat"):
            lines.append(f"- Caveat: {brand['caveat']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_validation_report(payload: dict[str, Any], html_path: Path) -> Path:
    path = OUTPUTS / "validation_report.md"
    single_lengths = sorted({len(rows) for rows in payload["series"]["single_index"].values()})
    comparison_lengths = sorted({len(rows) for rows in payload["series"]["comparison_index"].values()})
    html_size = html_path.stat().st_size if html_path.exists() else 0
    data_embedded = False
    if html_path.exists():
        sample = html_path.read_text(encoding="utf-8", errors="ignore")
        data_embedded = "__DATA__" not in sample and "Google Trends Clinic Dashboard" in sample

    lines = [
        "# Google Trends Clinic Dashboard Validation",
        "",
        f"- Generated: {FETCHED_AT}",
        f"- Requested range: {START_DATE} to {END_DATE}",
        f"- Geography: {GEO} / Thailand",
        f"- Canonical brand count: `{len(payload['brands'])}`",
        f"- Single-brand weekly series lengths: `{single_lengths}`",
        f"- Comparison weekly series lengths: `{comparison_lengths}`",
        f"- HTML exists: `{html_path.exists()}`",
        f"- HTML size bytes: `{html_size}`",
        f"- HTML embeds generated data: `{data_embedded}`",
        "",
        "## Caveats",
        "",
    ]
    lines += [f"- {item}" for item in payload["metadata"]["limitations"]]
    lines += [
        "",
        "## Automation Notes",
        "",
        "- This validation is file/data validation suitable for GitHub Actions.",
        "- Browser rendering should be checked manually after material HTML or JavaScript changes.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    client = TrendsClient()
    single = build_single_series(client)
    comparison = build_comparison_series(client)
    payload = dashboard_payload(single, comparison)

    (OUTPUTS / "google_trends_data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_csvs(single, comparison)
    html_path = write_html(payload)
    methodology_path = write_methodology(payload)
    validation_path = write_validation_report(payload, html_path)
    print(f"[done] HTML: {html_path}")
    print(f"[done] JSON: {OUTPUTS / 'google_trends_data.json'}")
    print(f"[done] CSV: {OUTPUTS / 'google_trends_weekly.csv'}")
    print(f"[done] Methodology: {methodology_path}")
    print(f"[done] Validation: {validation_path}")


if __name__ == "__main__":
    main()
