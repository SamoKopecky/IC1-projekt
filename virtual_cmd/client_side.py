import sys

sys.path.insert(1, '../')
from virtual_cmd.communication import User as user

# example netsh advfirewall firewall add rule name="Open Port 80" dir=in action=allow protocol=TCP localport=80

user = user.use_user('send')
command = input("enter command : ")
user.send_data(command)
print(user.receive_data())
