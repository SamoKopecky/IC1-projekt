import sys
import subprocess
import os
import re

sys.path.insert(1, '../')
from virtual_cmd.communication import User as user


class Server:
    def __init__(self):
        self.communication = user.User(sys.argv[1], sys.argv[2])
        self.current_directory = os.getcwd()
        self.communication.use_user('receive')

    def receive_command(self):
        """
            the command from client side is first detected here
            :return:
        """
        received_command = self.communication.receive_data()
        self.communication.send_data(subprocess.getoutput(received_command))
        self.detect_changing_directory(received_command)

    def detect_changing_directory(self, received_command: str):
        """
            this function checks if the command cd is contained in the whole command chain
            if so then it removes whitespaces and updated the directory
            :param received_command: command received from server side
            :return:
        """
        if received_command.__contains__('cd'):
            directories = re.findall("cd .*;?", received_command)
            for directory in directories:
                directory = re.sub('\s+', '', directory[3:])
                try:
                    os.chdir(directory)
                except FileNotFoundError:
                    pass
            self.current_directory = os.getcwd()
            self.sync_my_directory()

    def sync_my_directory(self):
        """
            function for syncing the directory with the client side
            :return:
        """
        self.communication.send_data(self.current_directory)


def main_loop():
    server = Server()
    server.sync_my_directory()
    while True:
        server.receive_command()


main_loop()
