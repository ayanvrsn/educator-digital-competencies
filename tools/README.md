# Rebuild the report

The structured report content is in `report_content.py`; vector diagrams and layout are in `build_report.py`. The editable HTML, JSON and SVG exports can also be revised directly.

Use Python 3.11 or newer with ReportLab 4 and DejaVu Serif/Sans regular and bold TTF fonts. Install the Python dependency in an isolated virtual environment. Set `DIPLOMA_FONT_DIR` to the font directory, then run from the repository root:

```sh
python tools/build_report.py
```

This overwrites `docs/First_Submission_Report.pdf`, the HTML sections, JSON source and diagram exports. It does not change the tracker, submit the form or create release tags. Re-render and visually check the PDF after changes. The screenshots PDF must be rebuilt only from new authentic captures when the board changes.
