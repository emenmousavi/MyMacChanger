#!/usr/bin/env python

import subprocess
import argparse
import re

# Get command-line arguments using optparse module
def get_args():
    parser = argparse.ArgumentParser()
    # Add options to the parser
    parser.add_argument("-i", "--interface", dest="interface", help="The Network Interface to change its MAC Address")
    parser.add_argument("-m", "--mac", dest="mymac", help="The New MAC Address")
    # Parse the command-line arguments
    args = parser.parse_args()
    # Check if the user has provided both the interface and the new MAC address
    if not args.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not args.mymac:
        parser.error("[-] Please specify a MAC Address, use --help for more info")
    return args

# Change the MAC address of a network interface
def changeMac(interface, mymac):
    # Print a message to indicate that the MAC address is being changed
    print(" [+] Changing the MAC Address for " + interface + " to " + mymac)
    # Use the subprocess module to execute the shell command that changes the MAC address
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mymac])
    subprocess.call(["ifcofnfig", interface, "up"])

# Show the current MAC address of a network interface
def showMac(interface):
    # Use the subprocess module to execute the shell command that shows the current MAC address
    ifconfig = subprocess.check_output(['ifconfig', interface])
    # Use regular expressions to find the MAC address in the output of the ifconfig command
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    # If a MAC address is found, return it
    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Couldn't find the MAC Address")

# Get the command-line arguments
options = get_args()

# Show the current MAC address of the interface
currentMac = showMac(options.interface)
print("The current MAC Address is " + str(currentMac))

# Change the MAC address of the interface
changeMac(options.interface, options.mymac)

# Show the new MAC address of the interface and print a success or failure messagecurrentMac = showMac(options.interface)
if currentMac == options.mymac:
    print("[+] The MAC Address successfully has changed to " + currentMac)
else:
    print("[-] MAC Address failed to change!")
