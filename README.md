# AIM-Sirius 3.0 - Distance Education

### Report generation
So, firstly install requirements for Python and ChromeDriver ([download here](https://chromedriver.storage.googleapis.com/index.html?path=85.0.4183.87/)). Put downloaded driver in the same folder with `generate_report.py`.

After that you need to generate data analysis report in json format. So, it's look like this:
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
To generate report you'll need to run `python generate_report.py -i <JSON report file>`. Example: `python .\generate_report.py -i report.json`. After script finish you'll get html report file with creation date.
