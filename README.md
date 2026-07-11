# Google Trends Clinic Dashboard

Interactive Google Trends dashboard for the Thailand clinic and beauty-clinic watchlist.

## Online Dashboard

This repository publishes `outputs/index.html` to GitHub Pages through GitHub Actions.

## Refresh Schedule

The workflow runs every Monday at 09:00 Asia/Bangkok using GitHub Actions' timezone-aware schedule (`cron: 0 9 * * 1`, `timezone: Asia/Bangkok`).

Manual refresh is also available from the Actions tab with `workflow_dispatch`.

## Local Refresh

```powershell
python -m pip install -r requirements.txt
python .\scripts\fetch_and_build_dashboard.py
python .\scripts\check_outputs.py
```

The dashboard data source is Google Trends. Values are relative indices, not absolute search volume.
