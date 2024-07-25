import subprocess
import time
import json

def run_local_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}")
        print(f"Error output: {e.stderr}")

timestamp = int(time.time())

log_entry = {"timestamp": timestamp,}

warning_words = ['ERROR', 'INFO', 'WARN']
path_file = "/var/log/syslog"
for warning_word in warning_words:
        log_entry[warning_word] = 0

with open(path_file, 'r') as log_file:
    lines = log_file.readlines()
    for line in lines:
        words = line.split()
        for warning_word in warning_words:
            try:
                if warning_word == words[5]:
                    log_entry[warning_word] += 1
            except:
                pass

print(log_entry)
log_errors_and_warnings = 'log_errors_and_warnings.json'

with open(log_errors_and_warnings, "w") as output_file:
    json.dump(log_entry, output_file, indent=4)