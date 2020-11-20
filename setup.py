import os
import ssl
import subprocess
import sys
import zipfile

try:
    import requests
    import urllib.request
    import urllib.parse
    import chromedriver_autoinstaller
    import xml.etree.ElementTree as elemTree
except:
    print("Required packages are not found. Installing..")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    import requests
    import urllib.request
    import urllib.parse
    import chromedriver_autoinstaller.utils
    import xml.etree.ElementTree as elemTree


def chromedriver_major(version):
    return version.split('.')[0]


def get_chromedriver_version(version):
    proxies = {
        "http": os.getenv("http_proxy", None),
        "https": os.getenv("https_proxy", os.getenv("http_proxy", None))
    }
    req = urllib.request.Request('https://chromedriver.storage.googleapis.com/')
    g_context = ssl.SSLContext()
    if proxies['http']:
        req.set_proxy(proxies['http'], "http")
    if proxies['https']:
        req.set_proxy(proxies['https'], "https")
    doc = urllib.request.urlopen(req, context=g_context).read()
    root = elemTree.fromstring(doc)
    for k in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
        if k.text.find(chromedriver_major(version) + '.') == 0:
            return k.text.split('/')[0]
    return


def setup():
    print("ChromeDriver not found. Launching installation process..")
    chrome_version = chromedriver_autoinstaller.utils.get_chrome_version()
    if not chrome_version:
        print("Chrome isn't installed. Script is shutting down..")
        exit(0)
    chromedriver_version = get_chromedriver_version(chrome_version)
    if not chromedriver_version:
        print("Can not find chromedriver for currently installed chrome version.")
        exit(0)
    url = chromedriver_autoinstaller.utils.get_chromedriver_url(chromedriver_version)
    print("Installing ChromeDriver v" + chromedriver_version)
    print(url)

    platform, _ = chromedriver_autoinstaller.utils.get_platform_architecture()
    if platform == 'mac':
        chromedriver_save_path = '/usr/local/bin/chromedriver.zip'
    else:
        chromedriver_save_path = 'chromedriver.zip'
    with open(chromedriver_save_path, "wb") as f:
        print('Downloading ChromeDriver...')
        response = requests.get(
            url,
            stream=True, proxies={
                "http": os.getenv("http_proxy", None),
                "https": os.getenv("https_proxy", os.getenv("http_proxy", None))
            })
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(100 * dl / total_length)
                sys.stdout.write("\r[%s%s] %d/100" % ('=' * done, ' ' * (100 - done), done))
                sys.stdout.flush()

    with zipfile.ZipFile(chromedriver_save_path, 'r') as file:
        file.extractall('./')

    if os.path.exists(chromedriver_save_path):
        os.remove(chromedriver_save_path)
