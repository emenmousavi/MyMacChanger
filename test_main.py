import pytest
import main

def test_mac_changer():
    assert main.change_mac_address("eth0") == "New MAC address: 00:11:22:33:44:55"
