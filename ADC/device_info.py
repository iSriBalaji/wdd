import os
import subprocess
from datetime import datetime
from pytz import timezone
def get_device_info(device_id):
    device_info = {}

    try:
        device_info['mac_address'] = subprocess.check_output("cat /sys/class/net/wlan0/address", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['mac_address'] = '0.0.0.0'

    try:
        device_info['ip_address'] = subprocess.check_output("hostname -I", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['ip_address'] = None

    try:
        device_info['serial_no_pi'] = subprocess.check_output("cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['serial_no_pi'] = None

    try:
        device_info['subnet_mask'] = subprocess.check_output("ifconfig wlan0 | grep Mask | cut -d ':' -f 4", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['subnet_mask'] = None

    try:
        device_info['gateway'] = subprocess.check_output("ip r | grep default | awk '{print $3}'", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['gateway'] = None

    try:
        device_info['dns_server'] = subprocess.check_output("cat /etc/resolv.conf | grep nameserver | awk '{print $2}'", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['dns_server'] = None

    try:
        device_info['wifi_ssid'] = subprocess.check_output("iwgetid -r", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['wifi_ssid'] = None

    try:
        device_info['wifi_bssid'] = subprocess.check_output("iw dev wlan0 link | grep Connected | awk '{print $3}'", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['wifi_bssid'] = None

    try:
        device_info['hostname'] = subprocess.check_output("hostname", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['hostname'] = None

    try:
        device_info['model'] = subprocess.check_output("cat /proc/device-tree/model", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['model'] = None

    try:
        device_info['os_version'] = subprocess.check_output("cat /etc/os-release | grep PRETTY_NAME | cut -d '\"' -f 2", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['os_version'] = None

    try:
        device_info['kernel'] = subprocess.check_output("uname -r", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['kernel'] = None

    try:
        device_info['shell'] = os.getenv('SHELL')
    except Exception:
        device_info['shell'] = None

    try:
        device_info['processor'] = subprocess.check_output("lscpu | grep 'Model name' | awk -F: '{print $2}'", shell=True).decode('utf-8').strip()
    except Exception:
        device_info['processor'] = None

    try:
        device_info['total_RAM'] = float(subprocess.check_output("free -m | grep Mem | awk '{print $2}'", shell=True).decode('utf-8').strip())
    except Exception:
        device_info['total_RAM'] = None

    try:
        device_info['total_ROM'] = float(subprocess.check_output("df -h --total | grep total | awk '{print $2}' | sed 's/G//'", shell=True).decode('utf-8').strip())
    except Exception:
        device_info['total_ROM'] = None

    device_info['notes'] = ""

    all_none = all(value is None for key, value in device_info.items() if key not in ['notes', 'load_dt', 'created_at', 'updated_at'])

    return device_info, all_none