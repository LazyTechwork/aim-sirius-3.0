# AIM-Sirius 3.0 - Distance Education

### Report generation
#### About script
* Script filename &mdash; `generate_report.py`
* `-i` &mdash; Directory where `results.csv` and `task_ids.csv` are (**required**)
* `-s` &mdash; Specify subject of Olympiad to render it in report (_default_: `Mathematics`)
* `-c` &mdash; Specify custom color scheme to generate (_default_: `#483D8B`)

#### Example
> Script will automatically download all required files and packages.

* Linux/MacOS: `python3 .\generate_report.py -i .\data\mathematics\`
* Windows: `python .\generate_report.py -i .\data\mathematics\`

#### Result
After script finish you'll get html report file with creation date.

