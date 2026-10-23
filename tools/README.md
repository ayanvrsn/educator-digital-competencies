# Report sources and build

The current main PDF uses the GOST 7.32-2017 presentation rules. Its structured eleven-section content is in `report_content.py`. `build_gost_report.py` adds the title, abstract, contents, numbered citations, bibliography, conclusions and appendices. It reuses the vector diagram definitions in `build_report.py`, which retains the earlier compact layout for reference.

Install the packages in `tools/requirements.txt`. Supply locally licensed Times New Roman font files through `DIPLOMA_TIMES_FONT_DIR`; on this Mac the default is `/System/Library/Fonts/Supplemental`. Set `DIPLOMA_FONT_DIR` to a directory containing DejaVu Serif and Sans regular/bold TTF files used by the shared diagram generator. Font files are not distributed in this repository.

Run from the repository root:

```sh
python tools/build_gost_report.py
python tools/build_tracker_report.py
```

The default output is `docs/First_Submission_Report.pdf`. An alternate location can be selected with `--output`. The build also writes `docs/report-gost.html` and `docs/gost-layout-audit.json`. It uses the current task JSON, authentic screenshot files and prototype verification record for the appendices.

The tracker builder writes `docs/YouTrack_Task_Screenshots.pdf`. Both PDFs use `project-management/screenshots/selected-evidence.json` so their eight evidence views remain consistent. Five images were supplied by the student on 23 October; their original filenames and checksums are recorded in `user-supplied-provenance.json`.

After a content change, rebuild, render and visually inspect the PDF. The current verified revision has 63 pages: 55 A4 pages and eight A3 screenshot pages. No experiment, interview or supervisor approval is produced by the build.
