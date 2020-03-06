import subprocess
import re


# test command : netsh advfirewall firewall add rule name="Open Port 80" dir=in action=allow protocol=TCP localport=80

def convert_into_list(given_command: str):
    given_command = 'cmd /c ' + given_command
    regex_string = '[a-z]+=\"[^\"]+\"'
    commands_with_space = re.findall(regex_string, given_command)
    i = 0
    for cmd in commands_with_space:
        replace_string = "regex:{}".format(i)
        i = i + 1
        given_command = given_command.replace(cmd, replace_string)
    commands = given_command.split(" ")
    for i in range(len(commands_with_space)):
        commands_with_space[i] = commands_with_space[i].replace('\"', '\'')
        regex_element = "regex:{}".format(i)
        commands.insert(commands.index(regex_element), commands_with_space[i])
        commands.remove(regex_element)
    return commands


def run_command(command):
    list_of_commands = convert_into_list(command)
    return subprocess.run(list_of_commands).returncode


def input_command():
    list_of_commands = convert_into_list(input("Enter command : "))
    print(subprocess.run(list_of_commands).returncode)
