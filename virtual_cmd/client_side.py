import sys

sys.path.insert(1, '../')
from virtual_cmd.communication import User as user


class Client:
    def __init__(self):
        self.communication = user.User(input("choose an ip address of your CA : "),
                                       input("choose an ip address of your server : "))
        self.server_current_directory = ''
        self.communication.use_user('send')

    def input_command(self):
        """
            this function runs in a loop waiting for user to input a command
            :return:
        """
        sent_command = input(self.server_current_directory + '>')
        self.communication.send_data(sent_command)
        print(self.communication.receive_data())
        if sent_command.__contains__('cd'):
            self.sync_server_directory()

    def sync_server_directory(self):
        """
            method used for syncing current directory with the server side
            :return:
        """
        self.server_current_directory = self.communication.receive_data()


def main_loop():
    client = Client()
    client.sync_server_directory()
    while True:
        client.input_command()


main_loop()
