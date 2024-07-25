from SshToServer import SshToServer
import pandas as pd
import json
import os

def runInServer():
    my_ssh = SshToServer(r"C:\Users\ami\Downloads\linux\my-key-pair.pem","16.170.246.90","ubuntu")
    my_ssh.runRemoteCommand("python3 server_side.py")
    stdout, stderr = my_ssh.runRemoteCommand("cat log_errors_and_warnings.json")
    if len(stderr) != 0:
        print(stderr)
    else:
        try:
            data_from_server = json.loads(stdout)
            df_new = pd.DataFrame([data_from_server])
            file_path = 'data_from_server.csv'
            if os.path.exists(file_path):
                df_existing = pd.read_csv(file_path)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = df_new
            df_combined.to_csv(file_path, index=False)
        except Exception as e:
            print(e)

runInServer()
