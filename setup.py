import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])


contents = open("requirements.txt","r+")
for package in contents:
	if package:
		print(f'installing {package}')
		install(package)





