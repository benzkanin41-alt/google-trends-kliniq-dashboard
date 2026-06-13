# Google Trends Clinic Dashboard Validation

Generated on 2026-06-13.

## Local URL

- URL: http://127.0.0.1:8877/
- Served file: `outputs/index.html`
- HTTP GET check: `200`, response size `839401` bytes.

## Data Completeness

- Canonical brand count: `17`
- Single-brand weekly series length: `233` weekly points for every brand.
- Comparison weekly series length: `233` weekly points for every brand.
- Data range requested from Google Trends: `2022-01-01` to `2026-06-13`.
- Geography: Thailand (`TH`).
- Grain: weekly.

## Browser QA

- Desktop load check: `17` brand options, `5` metric cards, active `singlePanel`, no console errors returned by the browser log check.
- Interaction check: selecting `Romrawin` updated the selected brand and chart title; compare tab opened with `17` checkboxes and `5` default selected names.
- Desktop layout check: no horizontal overflow detected at default viewport.
- Mobile layout check: no horizontal overflow detected at `390 x 844`; toolbar collapsed to one column; single chart remained visible.
- Screenshot QA file saved under `work/qa_desktop.png`.

## Known Caveats

- Google Trends reports relative search interest indices, not absolute search volume.
- `single_index` is normalized within each brand alias group and should not be compared level-for-level across brands.
- `comparison_index` is anchored/rescaled through `THE KLINIQ` so selected brands can be compared on one chart; it is directional and relative, not a replacement for raw search-volume data.
- Generic or acronym-like names such as `APEX`, `SLC`, `L clinic`, `Acne lab`, `KKC clinic`, and `THE RITZ clinic` may include unrelated search intent despite clinic-oriented aliases.
- `Souel clinic` is ambiguous; `Seoul Clinic` was included as a likely spelling variant and should be reviewed if this is used for an investment memo.
