import sys
import subprocess

sys.path.insert(1, '../')
from virtual_cmd.communication import User as user

user = user.use_user('receive')
received_command = user.receive_data()
user.send_data(subprocess.getoutput(received_command))
