import argparse
import json
import os
import signal
import subprocess
import sys
from datetime import datetime

import setup
import funcs
import kseniia
import daiwik
import gleb
import harsh_siddharth

try:
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except:
    print("Required packages are not found. Installing..")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Trying to import again..")
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    print("Import successful. Launching script..")

parser = argparse.ArgumentParser(description='Generate HTML report from Olympiad Analysis')
parser.add_argument('-i', dest='input', action='store',
                    help='Specify input directory', required=True)
parser.add_argument('-s', dest='subject', action='store',
                    help='Specify subject', default="Mathematics")
parser.add_argument('-c', dest='color', action='store',
                    help='Specify color', default="#483D8B")

args = parser.parse_args()
data = {
    'subject': args.subject,
    'color': args.color,
    'blocks': list()
}

data['blocks'].append(funcs.call_read_return(kseniia, "optimization", args.input))
data['blocks'].append(funcs.call_read_return(daiwik, "main_function", args.input))
data['blocks'].append(funcs.call_read_return(daiwik, "bad_tasks", args.input))
data['blocks'].append(funcs.call_read_return(harsh_siddharth, "compute_fraction_data", args.input))
data['blocks'].append(funcs.call_read_return(harsh_siddharth, "compute_attempt_count_data", args.input))
data['blocks'].append(funcs.call_read_return(harsh_siddharth, "make_fraction_for_task_block", args.input))
data['blocks'].extend(funcs.call_read_return_multiple(gleb, "getOlympiadScores", args.input, ["act_opt", "scores"]))

print("Making common JSON...")

with open("data.js", "w+", encoding='utf-8') as file:
    file.write('const GLOBAL_DATA = `' + json.dumps(data) + '`;' + "\n")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FILEPATH = os.getcwd()

if not (os.path.exists('chromedriver.exe') or os.path.exists('chromedriver')):
    setup.setup()
else:
    setup.specify_path()

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get(r'file://{0}/report.html'.format(FILEPATH))
print("Generating HTML page...")
driver.implicitly_wait(2)
html = BeautifulSoup(driver.page_source, 'html.parser')

for s in html.select('script'):
    s.extract()
print("Got HTML page, extracting tables...")

html_filename = "report_" + args.subject + "_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + ".html"
with open(html_filename, "w+",
          encoding='utf-8') as file:
    file.write(html.prettify())
    print("Report saved in {0}".format(html_filename))

if os.path.exists('data.js'):
    os.remove('data.js')

try:
    driver.close()
    os.kill(int(driver.service.process.pid), signal.SIGTERM)
except:
    print('Cannot kill driver process')
