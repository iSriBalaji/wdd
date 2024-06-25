import os
import re
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


def get_device_dynamic_config():
    device_dynamic_config = {}
    
    try:
        subprocess.check_output(['ping', '-c', '1', '8.8.8.8'])
        device_dynamic_config['is_connected_internet'] = True
    except Exception:
        device_dynamic_config['is_connected_internet'] = False

    try:
        device_dynamic_config['cpu_usage_percent'] = float(os.popen("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").readline().strip())
    except Exception:
        device_dynamic_config['cpu_usage_percent'] = None

    try:
        device_dynamic_config['cpu_temperature'] = float(os.popen("vcgencmd measure_temp").readline().replace("temp=", "").replace("'C\n", ""))
    except Exception:
        device_dynamic_config['cpu_temperature'] = None

    try:
        memory_info = os.popen("free -m").readlines()[1].split()
        memory_total = float(memory_info[1])
        memory_used = float(memory_info[2])
        device_dynamic_config['memory_usage'] = (memory_used / memory_total) * 100
    except Exception:
        device_dynamic_config['memory_usage'] = None

    try:
        disk_info = os.popen("df -h /").readlines()[1].split()
        device_dynamic_config['disk_usage'] = float(disk_info[4].replace('%', ''))
    except Exception:
        device_dynamic_config['disk_usage'] = None

    try:
        device_dynamic_config['uptime'] = os.popen("uptime -p").readline().strip()
    except Exception:
        device_dynamic_config['uptime'] = None

    try:
        device_dynamic_config['wifi_info'] = get_wifi_info()
    except Exception:
        device_dynamic_config['wifi_info'] = None

    return device_dynamic_config

def get_wifi_info():
    wifi_info = {}
    
    try:
        wpa_supplicant_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
        if not os.path.exists(wpa_supplicant_file):
            return wifi_info

        with open(wpa_supplicant_file, 'r') as f:
            content = f.read()
        
        # Regex to find network blocks
        network_blocks = re.findall(r'network=\{(.*?)\}', content, re.DOTALL)
        
        for block in network_blocks:
            ssid_match = re.search(r'ssid="([^"]+)"', block)
            psk_match = re.search(r'psk="([^"]+)"', block)
            if ssid_match:
                ssid = ssid_match.group(1)
                psk = psk_match.group(1) if psk_match else None
                wifi_info[ssid] = psk

        # Get current connected Wi-Fi name
        try:
            current_ssid = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
            current_psk = wifi_info.get(current_ssid, None)
            wifi_info['current'] = {'ssid': current_ssid, 'password': current_psk}
        except subprocess.CalledProcessError:
            wifi_info['current'] = {'ssid': None, 'password': None}
        
        return wifi_info
    except Exception as e:
        return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    device_info = get_device_info(device_id=1)
    print(device_info)
    device_dynamic_config = get_device_dynamic_config()
    print(device_dynamic_config)