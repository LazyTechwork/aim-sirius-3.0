import argparse
import json
import os
import signal
import subprocess
import sys
from datetime import datetime

import setup
import funcs

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

# funcs.make_answers_count_block(args.input, "make_answers_count_block.json")
# with open("make_answers_count_block.json", "r") as file:
#     obj = json.load(file)
#     obj['id'] = 'make_answers_count_block'
#     data['blocks'].append(obj)
# os.remove("make_answers_count_block.json")

data['blocks'].append(funcs.call_read_return(funcs, "make_answers_count_block", args.input))
data['blocks'].append(funcs.call_read_return(funcs, "make_fraction_for_task_num_block", args.input))

with open("data.js", "w+") as file:
    file.write('const GLOBAL_DATA = `' + json.dumps(data) + '`;' + "\n")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FILEPATH = os.getcwd()

if not (os.path.exists('chromedriver.exe') or os.path.exists('chromedriver')):
    setup.setup()

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get(r'file://{0}/report.html'.format(FILEPATH))
driver.implicitly_wait(2)
html = BeautifulSoup(driver.page_source, 'html.parser')

for s in html.select('script'):
    s.extract()

with open("report_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + ".html", "w+") as file:
    file.write(html.prettify())

if os.path.exists('data.js'):
    os.remove('data.js')

try:
    driver.close()
    os.kill(int(driver.service.process.pid), signal.SIGTERM)
except:
    print('Cannot kill driver process')
