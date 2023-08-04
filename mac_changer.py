import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC addr")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC addr")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC ddr for " + interface + " to " + new_mac)
    subprocess.call(["ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", "dev", interface, "up"])

def get_mac(interface):
    ip_results = subprocess.check_output(["ip", "addr", "show", interface]).decode()
    search_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ip_results)

    if search_res:
        return search_res.group(0)
    else:
        print("[-] Could not find a MAC address.")

options = get_arguments()
current_mac = get_mac(options.interface)
print("Current MAC: " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Successfuly changed the MAC address to " + current_mac + ".")
else:
    print("[-] Error while changing the MAC address.")




