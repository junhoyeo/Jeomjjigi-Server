import json
import subprocess

connection_string = json.load(open('./secret.json'))['connection']

def send_to_device(device_id, msg_obj):
    msg = json.dumps(msg_obj)
    print(f'{msg} ➡️ {device_id}')
    cmd = ['iothub-explorer', 'send', device_id, msg, '--login', connection_string]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return output.decode()
