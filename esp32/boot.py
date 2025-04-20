# boot.py
import network
from time import sleep

# Configuration du WiFi
WIFI_SSID = "iPhone" # Mettre votre WIFI_SSID
WIFI_PASSWORD = "toulouse31" # Mettre votre WIFI_PASSWORD

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connexion au WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            print(".")
            sleep(0.5)
    print("Connecté au WiFi")
    print("Adresse IP:", wlan.ifconfig()[0])

# Connexion au WiFi au démarrage
connect_wifi()


