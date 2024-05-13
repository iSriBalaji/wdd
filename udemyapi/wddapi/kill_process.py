import subprocess
import re

# Run the lsof command
output = subprocess.check_output(["lsof", "-i:8000"]).decode("utf-8")

# Extract PIDs using regex
pids = re.findall(r"\b(\d+)\b", output)

# Kill the PIDs
for pid in pids:
    subprocess.run(["kill", "-9", pid])
    print(f"Killed PID {pid}")
