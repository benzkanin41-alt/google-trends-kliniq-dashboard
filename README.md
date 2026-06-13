# Google Trends Clinic Dashboard

Interactive Google Trends dashboard for the Thailand clinic and beauty-clinic watchlist.

## Online Dashboard

This repository publishes `outputs/index.html` to GitHub Pages through GitHub Actions.

## Refresh Schedule

The workflow runs every Monday at 14:00 Asia/Bangkok, represented as `0 7 * * 1` in GitHub Actions cron because scheduled workflows run in UTC by default.

Manual refresh is also available from the Actions tab with `workflow_dispatch`.

## Local Refresh

```powershell
python -m pip install -r requirements.txt
python .\scripts\fetch_and_build_dashboard.py
python .\scripts\check_outputs.py
```

The dashboard data source is Google Trends. Values are relative indices, not absolute search volume.
