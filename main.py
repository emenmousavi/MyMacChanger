#!/usr/bin/env python

import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="The Network Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="mymac", help="The New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.mymac:
        parser.error("[-] Please specify a MAC Address, use --help for more info")
    return options


def changeMac(interface, mymac):
    print(" [+] Changing the MAC Address for " + interface + " to " + mymac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface], "hw", "ether", mymac)
    subprocess.call(["ifcofnfig", interface, "up"])


def showMac(interface):
    ifconfig = subprocess.check_output(['ifconfig', interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)
    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Couldn't find the MAC Address")


options = get_args()

currentMac = showMac(options.interface)
print("The current MAC Address is " + str(currentMac))

changeMac(options.interface, options.mymac)

currentMac = showMac(options.interface)
if currentMac == options.mymac:
    print("[+] The MAC Address successfully has changed to " + currentMac)
else:
    print("[-] MAC Address failed to change!")