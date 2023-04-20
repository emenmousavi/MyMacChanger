#!/usr/bin/env python

import subprocess
import argparse
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_args():
    """Get command-line arguments using argparse module"""
    parser = argparse.ArgumentParser()
    # Add options to the parser
    parser.add_argument("-i", "--interface", dest="interface", help="The Network Interface to change its MAC Address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="The New MAC Address")
    # Parse the command-line arguments
    args = parser.parse_args()
    # Check if the user has provided both the interface and the new MAC address
    if not args.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not args.new_mac:
        parser.error("[-] Please specify a MAC Address, use --help for more info")
    return args

def change_mac(interface, new_mac):
    """Change the MAC address of a network interface"""
    # Print a message to indicate that the MAC address is being changed
    logging.info(f"Changing the MAC Address for {interface} to {new_mac}")
    # Use the subprocess module to execute the shell command that changes the MAC address
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def show_mac(interface):
    """Show the current MAC address of a network interface"""
    # Use the subprocess module to execute the shell command that shows the current MAC address
    ifconfig = subprocess.check_output(['ifconfig', interface])
    # Use regular expressions to find the MAC address in the output of the ifconfig command
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    # If a MAC address is found, return it
    if mac_result:
        return mac_result.group(0)
    else:
        logging.error("Couldn't find the MAC Address")

def main():
    # Get the command-line arguments
    options = get_args()

    # Show the current MAC address of the interface
    current_mac = show_mac(options.interface)
    logging.info(f"The current MAC Address is {current_mac}")

    # Change the MAC address of the interface
    change_mac(options.interface, options.new_mac)

    # Show the new MAC address of the interface and print a success or failure message
    current_mac = show_mac(options.interface)
    if current_mac == options.new_mac:
        logging.info(f"The MAC Address successfully has changed to {current_mac}")
    else:
        logging.error("MAC Address failed to change!")

if __name__ == "__main__":
    main()
