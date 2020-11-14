# AIM-Sirius 3.0 - Distance Education

### Report generation
> Script will automatically download all required files and packages.

You need to generate data analysis report in json format. So, it's look like this:
```json
{
  "color": "#67b811",
  "subject": "Mathematics",
  "task_difficulty": [
    [660,687,692,713],...
  ]
}
```

In `color` you can set the main color scheme of report.

In `subject` you can set the name of subject of the olympiad.

`task_difficulty` is n&times;n matrix with task_difficulty by tasks and variants. The row is the task, the column is the variant.

#### How to generate?
To generate report you'll need to run `python3 generate_report.py -i <JSON report file>`. Example: `python3 .\generate_report.py -i report.json`. After script finish you'll get html report file with creation date.

> **IMPORTANT!** You need to use Python executable suitable for your operating system
