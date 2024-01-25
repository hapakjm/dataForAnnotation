import os
import subprocess
import shlex

os.system('cls')

os.makedirs('data', exist_ok=True)
os.makedirs('newData', exist_ok=True)

subprocess.call(shlex.split('python -m venv ".venv" --upgrade-deps'), shell=True)

while (True):
    if (os.path.exists('.venv')):
        activate_path = os.path.join('.venv', 'Scripts', 'activate').replace('\\', '//')
        subprocess.call(shlex.split(activate_path), shell=True)

        subprocess.call(shlex.split('pip install -r requirements.txt'), shell=True)

        os.system('cls')

        subprocess.call(shlex.split('pip freeze'), shell=True)

        break