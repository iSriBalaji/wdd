import os
import sys
import pkg_resources
import subprocess

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
wdd_directory = os.path.dirname(parent_directory)
requirements_folder_path = os.path.join(wdd_directory, 'requirements')
sys.path.append(requirements_folder_path)

import config

OS_REQUIREMENT_PATH = os.path.join(requirements_folder_path, config.OS_REQUIREMENT_PATH)
PY_REQUIREMENT_PATH = os.path.join(requirements_folder_path, config.PY_REQUIREMENT_PATH)

def get_py_installed_list():
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    return(installed_packages_list)

def is_command_installed(command):
    result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def install_packages(packages):
    try:
        subprocess.check_call(['sudo', 'apt', 'install', '-y'] + packages)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        return False
    return True

def read_packages(file_path):
    packages = []
    with open(file_path, 'r') as file:
        for line in file:
            packages.append(line.strip())
    return packages

def update_firmware():
    packages = read_packages(OS_REQUIREMENT_PATH)

    missing_commands = []

    for package in packages:
        if not is_command_installed(package):
            missing_commands.append(package)

    if not missing_commands:
        return 'firmware_is_updated'

    if not install_packages(missing_commands):
        return 'Failed to install some packages'
    
    still_missing_packages = [pkg for pkg in missing_commands if not is_command_installed(pkg)]

    if not still_missing_packages:
        return 'firmware_is_updated'
    else:
        return still_missing_packages

def install_packages_from_requirements(file_path=PY_REQUIREMENT_PATH):
    with open(file_path, 'r') as file:
        packages = file.read().splitlines()

    python_installed_list = get_py_installed_list()

    not_installed = []
    for package in packages:
        if package not in python_installed_list:
            not_installed.append(package)
            subprocess.call(['pip', 'install', package])

    # Check if all packages are installed
    for package in packages:
        if package not in python_installed_list:
            return tuple(not_installed)

    return "python_package_upto_date"

if __name__ == '__main__':
    result = update_firmware()
    py_result = install_packages_from_requirements()
    print(result)
    print(py_result)