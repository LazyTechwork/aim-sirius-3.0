import argparse
import json
import os
import signal
import subprocess
import sys
from datetime import datetime

import setup

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
                    help='Specify input file', required=True)
parser.add_argument('--driver', action='store', help='Path to ChromeDriver')

args = parser.parse_args()
with open(args.input, "r") as file:
    data = json.load(file)
with open("data.js", "w+") as file:
    file.write('const GLOBAL_DATA = `' + json.dumps(data) + '`;' + "\n")

os.chdir(os.path.dirname(__file__))
FILEPATH = os.getcwd()

if not (os.path.exists('chromedriver.exe') or os.path.exists('chromedriver')):
    setup.setup()

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path=(args.driver or "chromedriver"))

driver.get(r'file://{0}/report.html'.format(FILEPATH))
driver.implicitly_wait(2)
html = BeautifulSoup(driver.page_source, 'html.parser')

for s in html.select('script'):
    s.extract()

with open("report_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + ".html", "w+") as file:
    file.write(html.prettify())

if os.path.exists('data.js'):
    os.remove('data.js')
if os.path.exists('debug.log'):
    os.remove('debug.log')

try:
    driver.close()
    os.kill(int(driver.service.process.pid), signal.SIGTERM)
except:
    print('Cannot kill driver process')
