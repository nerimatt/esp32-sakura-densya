import network
from utime import sleep
import json

def connect_to_wifi():


    with open("wifis.json", "r") as wififile:
        WIFI_DATA = json.load(wififile) # (SSID, PASSWORD)


    station = network.WLAN(network.STA_IF)
    station.active(True)

    # get available networks
    networks = station.scan()
    available_networks = [network[0].decode() for network in networks]
    while not available_networks:
        print("no wifi found... \nretrying...")
        networks = station.scan()
        available_networks = [network[0].decode() for network in networks]
        sleep(2)

    print("available networks:", available_networks)


    for wifi in WIFI_DATA:
        if wifi not in available_networks: continue
        
        print(f"connecting to '{wifi}'... ", end = "")
        
        # Connect to Wi-Fi
        try:
            station.connect(wifi, WIFI_DATA[wifi])
            # Wait for the Wi-Fi connection
            while not station.isconnected():
                sleep(0.2)
            
            print("[V]")
            print('IP address:', station.ifconfig()[0])

            break

        except OSError as e:
            # this is only to ignore impossibility to connect to wifi
            if e.args[0] != "Wifi Internal Error":
                raise e
            
            print(f"[X] \ncannot connect to '{wifi}'")
            station.disconnect()  # Disconnect before moving to the next network
            station.active(False)  # Disable Wi-Fi interface
            sleep(1)  # Give some time for cleanup and reinitialization
            station.active(True)
    
    return station
        
if __name__ == "__main__":
    station = connect_to_wifi()
    
    import urequests
    response = urequests.get('http://192.168.1.161:8000/anime')
    print(response.content.decode()[:100])

    station.disconnect()  # Disconnect before moving to the next network
    station.active(False)  # Disable Wi-Fi interface



