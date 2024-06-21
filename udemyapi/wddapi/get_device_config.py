import subprocess
import os
from datetime import datetime

def get_device_info():
    device_info = {}
    device_info['mac_address'] = subprocess.check_output("cat /sys/class/net/wlan0/address", shell=True).decode('utf-8').strip()
    device_info['ip_address'] = subprocess.check_output("hostname -I", shell=True).decode('utf-8').strip()
    device_info['serial_no_pi'] = subprocess.check_output("cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2", shell=True).decode('utf-8').strip()
    device_info['subnet_mask'] = subprocess.check_output("ifconfig wlan0 | grep Mask | cut -d ':' -f 4", shell=True).decode('utf-8').strip()
    device_info['gateway'] = subprocess.check_output("ip r | grep default | awk '{print $3}'", shell=True).decode('utf-8').strip()
    device_info['dns_server'] = subprocess.check_output("cat /etc/resolv.conf | grep nameserver | awk '{print $2}'", shell=True).decode('utf-8').strip()
    device_info['wifi_ssid'] = subprocess.check_output("iwgetid -r", shell=True).decode('utf-8').strip()
    device_info['wifi_bssid'] = subprocess.check_output("iw dev wlan0 link | grep Connected | awk '{print $3}'", shell=True).decode('utf-8').strip()
    device_info['hostname'] = subprocess.check_output("hostname", shell=True).decode('utf-8').strip()
    device_info['model'] = subprocess.check_output("cat /proc/device-tree/model", shell=True).decode('utf-8').strip()
    device_info['os_version'] = subprocess.check_output("cat /etc/os-release | grep PRETTY_NAME | cut -d '\"' -f 2", shell=True).decode('utf-8').strip()
    device_info['kernel'] = subprocess.check_output("uname -r", shell=True).decode('utf-8').strip()
    device_info['shell'] = os.getenv('SHELL')
    device_info['processor'] = subprocess.check_output("lscpu | grep 'Model name' | awk -F: '{print $2}'", shell=True).decode('utf-8').strip()
    device_info['total_RAM'] = float(subprocess.check_output("free -m | grep Mem | awk '{print $2}'", shell=True).decode('utf-8').strip())
    device_info['total_ROM'] = float(subprocess.check_output("df -h --total | grep total | awk '{print $2}' | sed 's/G//'", shell=True).decode('utf-8').strip())
    device_info['notes'] = ""
    device_info['load_dt'] = datetime.now()
    device_info['created_at'] = datetime.now()
    device_info['updated_at'] = datetime.now()

    return device_info


config = get_device_info()
print(config)