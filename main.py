import socket
import sys
import time
import os


def main():
    print("\nWelcome to the FTP server.\n\nTo initialize Server , try to connect a client.")

def command_division(command):
        command_seperated_parts = command.split(" ", 1)
        command_opcode = command_seperated_parts[0].upper()
        arguments = command_seperated_parts[1]
        if len(arguments) < 1:
            arguments = None
            return command_opcode

        else:
            return command_opcode, arguments

def user_choice(command):
        arguments, command_opcode = command_division(command)
        print(command_opcode)
        print(arguments)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    txt = "stor .../ffgfg/t.txt .../fgfgfg"
    path = "/home/df/df/dfdf/m.text"
    d = "m.text"

    directory, filename = os.path.split(path)
    os.path.join(directory,d)
    print(os.path.join(directory,d))
    x = txt.split(" ")
    print(len(x))
    home = "F:\\home"
    g ="\home\ftp_server_log.txt"
    h= "\home\ftp_server_log.txt"
    if(h == g ):
        print("Fuc")
    print(x[0]+" " + x[2])
    user_choice("LIST /")
    main()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
