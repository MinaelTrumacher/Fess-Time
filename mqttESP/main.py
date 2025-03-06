from machine import Pin
from time import sleep
import dht
from umqtt.simple import MQTTClient

# Configuration du serveur MQTT
MQTT_BROKER = "192.168.69.29"
MQTT_CLIENT_ID = "ESP32Client"
MQTT_TOPIC_TEMP = "sensor/temperature"
MQTT_TOPIC_HUM = "sensor/humidity"

# Configuration du capteur DHT11
DHT_PIN = Pin(4, Pin.IN)
dht_sensor = dht.DHT11(DHT_PIN)

# Connexion au serveur MQTT
def connect_mqtt():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        print("Connecté au serveur MQTT")
        return client
    except Exception as e:
        print("Erreur de connexion MQTT:", e)
        return None

# Lecture des données du capteur DHT11
def read_sensor():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("Erreur de lecture du capteur DHT:", e)
        return None, None

# Programme principal
def main():
    mqtt_client = connect_mqtt()

    while True:
        if not mqtt_client:
            print("Tentative de reconnexion au serveur MQTT...")
            mqtt_client = connect_mqtt()

        temperature, humidity = read_sensor()
        if temperature is not None and humidity is not None:
            try:
                mqtt_client.publish(MQTT_TOPIC_TEMP, str(temperature).encode())
                mqtt_client.publish(MQTT_TOPIC_HUM, str(humidity).encode())
                print(f"Température: {temperature} °C, Humidité: {humidity} %")
            except Exception as e:
                print("Erreur de publication MQTT:", e)
                mqtt_client = None  # Forcer la reconnexion

        sleep(2)  # Attendre 2 secondes entre chaque lecture

# Démarrer le programme
if __name__ == "__main__":
    main()
