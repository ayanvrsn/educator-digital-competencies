# Report sources and build

The current main PDF uses the GOST 7.32-2017 presentation rules. Its structured eleven-section content is in `report_content.py`. `build_gost_report.py` adds the title, abstract, contents, numbered citations, bibliography, conclusions and appendices. It reuses the vector diagram definitions in `build_report.py`, which retains the earlier compact layout for reference.

Install the packages in `tools/requirements.txt`. Supply locally licensed Times New Roman font files through `DIPLOMA_TIMES_FONT_DIR`; on this Mac the default is `/System/Library/Fonts/Supplemental`. Set `DIPLOMA_FONT_DIR` to a directory containing DejaVu Serif and Sans regular/bold TTF files used by the shared diagram generator. Font files are not distributed in this repository.

Run from the repository root:

```sh
python tools/build_gost_report.py
```

The default output is `docs/First_Submission_Report.pdf`. An alternate location can be selected with `--output`. The build also writes `docs/report-gost.html` and `docs/gost-layout-audit.json`. It uses the current task JSON, authentic screenshot files and prototype verification record for the appendices.

After a content change, rebuild, render and visually inspect the PDF. The current verified revision has 59 pages: 55 A4 pages and four A3 screenshot pages. No experiment, interview or supervisor approval is produced by the build.
