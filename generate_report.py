import argparse
import json
import os
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import setup

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
if not (os.path.exists('chromedriver.exe') or os.path.exists('chromedriver')):
    setup.setup()
FILEPATH = os.getcwd()
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
