import sys

sys.path.insert(1, '../')
from virtual_cmd.communication import User as user

user = user.use_user('send')
user.send_data(input())
