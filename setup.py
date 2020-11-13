import os
import platform
import subprocess
import sys
import zipfile

try:
    import requests
    from PyInquirer import prompt
except:
    print("Required packages are not found. Installing..")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    import requests
    from PyInquirer import prompt


def setup():
    print("ChromeDriver not found. Launching installation process..")
    system = platform.uname().system.lower()
    if system == 'darwin':
        system = 'macos'

    osystems = ['Windows', 'MacOS', 'Linux']
    si = list(map(lambda it: it.lower(), osystems)).index(system)
    osystems[si], osystems[0] = osystems[0], osystems[si]
    print('Detected OS:', osystems[0])
    questions = [
        {
            'type': 'list',
            'message': 'Select your OS',
            'name': 'system',
            'choices': [{'name': it} for it in osystems]
        }
    ]

    answers = prompt(questions)
    print('Selected OS:', answers['system'])
    if answers['system'] == 'MacOS':
        answers['system'] = 'mac64'
    elif answers['system'] == 'Windows':
        answers['system'] = 'win32'
    elif answers['system'] == 'Linux':
        answers['system'] = 'linux64'

    with open('chromedriver.zip', "wb") as f:
        print('Downloading ChromeDriver...')
        response = requests.get(
            'https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_%s.zip' % answers['system'],
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

    with zipfile.ZipFile('chromedriver.zip', 'r') as file:
        file.extractall('./')

    if os.path.exists('chromedriver.zip'):
        os.remove('chromedriver.zip')
