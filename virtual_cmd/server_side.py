import sys
import subprocess
import os
import re

sys.path.insert(1, '../')
from virtual_cmd.communication import User as user


class Server:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.communication = user.use_user('receive')

    def receive_command(self):
        received_command = self.communication.receive_data()
        self.communication.send_data(subprocess.getoutput(received_command))
        self.detect_changing_directory(received_command)

    def detect_changing_directory(self, received_command: str):
        if received_command.__contains__('cd'):
            directories = re.findall("cd .*;?", received_command)
            for directory in directories:
                os.chdir(directory[3:])
            self.sync_my_directory()

    def sync_my_directory(self):
        self.communication.send_data(self.current_directory)


def main_loop():
    server = Server()
    server.sync_my_directory()
    while True:
        server.receive_command()


main_loop()
