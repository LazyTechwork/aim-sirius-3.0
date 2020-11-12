import argparse
import json
import os

from bs4 import BeautifulSoup

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path=(args.driver or "chromedriver"))

driver.get('file://' + FILEPATH + "/report.html")
driver.implicitly_wait(2)
html = BeautifulSoup(driver.page_source, 'html.parser')

for s in html.select('script'):
    s.extract()

with open("report_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + ".html", "w+") as file:
    file.write(html.prettify())
