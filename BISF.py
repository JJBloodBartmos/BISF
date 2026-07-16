import subprocess
import argparse
import re
import random

def BISF_mac(inter, new_mac):
    
    subprocess.call(["ip", "link", "set", "dev", inter, "down"])
    subprocess.call(["ip", "link", "set", "dev", inter, "address", new_mac])
    subprocess.call(["ip", "link", "set", "dev", inter, "up"])
def get_arguments():
    parser=argparse.ArgumentParser(description="change ur net interface's MAC address")
    parser.add_argument("--i","--interface", dest="inter", required=True, help="interface to be modified(exp: eth0)")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("-m", "--mac", dest="new_mac", help="New manual MAC address")
    grupo.add_argument("-r", "--random", action="store_true", help="Generate a random MAC address")
    
    
    return parser.parse_args()
    
def generate_random_MAC():
    mac = [f"{random.randint(0, 255):02x}" for _ in range(6)]
    mac[0] = "00" 
    return ":".join(mac)

options=get_arguments()

if options.random:
    MAC_to_use=generate_random_MAC()
    print("[*] Generating random MAC address")

else:
    MAC_to_use=options.new_mac
        
print(f"[*] Initiating change for interface {options.inter} -> New MAC: {MAC_to_use}")
BISF_mac(options.inter, MAC_to_use)
   
def check_mac(inter):
    
    confirmation = subprocess.check_output(["ip", "link", "show", inter]).decode("utf-8")
    
    
    mac_serch = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", confirmation)
    
    if mac_serch:
        return mac_serch.group(0) 
    else:
        print("[-] the MAC address of the interface could not be read...")
        return None


mac_actual = check_mac(options.inter)

if mac_actual == MAC_to_use:
    print(f"[+]  the MAC address was successfully changed to {mac_actual}")
else:
    print("[-] Error: The MAC wasn't changed---> check sudo")