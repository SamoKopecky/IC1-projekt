import sys

sys.path.insert(1, '../')
from utils import execute_cmd_command as exe_cmd
from virtual_cmd.communication import User as user

user = user.use_user('receive')
print(user.receive_data())
