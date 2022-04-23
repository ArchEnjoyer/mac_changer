#!/bin/env python
import subprocess
import random

#use as root user or with sudo; requires ifconfig

def randommac(): # returns random mac
    alphas = "0123456789abcde"
    alphasEven = "02468ace"
    word = ""
    for i in range(6):
        word += random.choice(alphas) + random.choice(alphas) + ":"

    word = word[:-1]
    word = word[0] + random.choice(alphasEven) + word[2:]
    return word

def changer(clear_interfaces): # we talk to user and return interface and mac
    print("Your interfaces:")
    cnt = 0
    for i in clear_interfaces:
        cnt += 1
        print(f"({cnt}) - {i}")

    print("select number: ", end = "")
    num = input()
    while not num.isdigit() or int(num) > len(clear_interfaces) or int(num)<1:
        print("Maybe you missed to key? If you want to quit, press q")
        print("select number: ", end = "")
        num = input()
        if num == "q" or num == "Q" or num == "й" or num == "Й":
            print("Maybe next time)")
            exit()

    interf = clear_interfaces[int(num)-1]
    print("Your new MAC(or type r if random, first octet must be even): ", end="")
    mac = str(input())
    if mac == "r" or mac == "R" or mac == "к" or mac == "К": mac = randommac()

    while len(mac)!= 17 or int(mac[1], 16) % 2 == 1:
        print("you typed incorrect form")
        print("do it again, set random with 'r' or quit with q: ", end="")
        mac = str(input())
        if mac == "r" or mac == "R" or mac == "к" or mac == "К": mac = randommac()
        elif mac == "q" or mac == "Q" or mac == "й" or mac == "Й":
            print("Maybe next time)")
            exit()
    return interf, mac

def editor(interf, mac):  # finally setting mac to new
    print(f"Your old mac is {old_mac(interf)}")

    subprocess.call(["ifconfig", interf, "down"])
    subprocess.call(["ifconfig", interf, "hw", "ether", mac])
    subprocess.call(["ifconfig", interf, "up"])

    print(f"Your new mac is {mac}")
    print("End of program, may the Force be with you!")

def my_interfaces(): # returns all availible interfaces without lo
    interfaces = subprocess.check_output("ifconfig", universal_newlines=True).split("\n")
    clear_interfaces = []
    while interfaces.count("") != 0:
        interfaces.remove("")
    for i in interfaces:
        if i[0] == " ":
            continue
        else:
            clear_interfaces.append(i[:i.index(":")])  # we add all availible adapters to 'clear_interfaces' list
    clear_interfaces.remove("lo")
    return clear_interfaces

def old_mac(interf): # returns old mac of interface
    info = subprocess.check_output(["ifconfig", interf], universal_newlines=True).split("\n")
    for i in info:
        i = i.strip(" /n")
        if i[0:5] == "ether":
            oldMac = i[6:23]
            return oldMac
def main():
    clear_interfaces = my_interfaces()
    print("""use with sudo!

     __  __    _    ____ ____ _   _    _    _   _  ____ _____ ____
    |  \/  |  / \  / ___/ ___| | | |  / \  | \ | |/ ___| ____|  _ \   _ __  _   _
    | |\/| | / _ \| |  | |   | |_| | / _ \ |  \| | |  _|  _| | |_) | | '_ \| | | |
    | |  | |/ ___ \ |__| |___|  _  |/ ___ \| |\  | |_| | |___|  _ < _| |_) | |_| |
    |_|  |_/_/   \_\____\____|_| |_/_/   \_\_| \_|\____|_____|_| \_(_) .__/ \__, |
                                                                     |_|    |___/
    """)
    if clear_interfaces == []:
        print("Something with your internet adapter, oops")
    else:
        interf, mac = changer(clear_interfaces)
        editor(interf, mac)

if __name__ == "__main__":
    main()
