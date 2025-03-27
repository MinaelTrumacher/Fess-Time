from machine import Pin, ADC, PWM
from umqtt.simple import MQTTClient
import utime

# MQTT
MQTT_BROKER = "172.20.10.10"
MQTT_CLIENT_ID = "ESP32Client"
MQTT_TOPIC_FSR = "sensor/fsr"

# Buzzer
BUZZER = PWM(Pin(25))
BUZZER.freq(1000)
BUZZER.duty(0)

# Capteur pression
PRESSURE_SENSOR = ADC(Pin(34))
PRESSURE_SENSOR.atten(ADC.ATTN_11DB)

# Afficheur
digits = [Pin(23, Pin.OUT), Pin(13, Pin.OUT), Pin(12, Pin.OUT), Pin(14, Pin.OUT)]
segments = [Pin(18, Pin.OUT), Pin(5, Pin.OUT), Pin(4, Pin.OUT), Pin(2, Pin.OUT),
            Pin(15, Pin.OUT), Pin(19, Pin.OUT), Pin(21, Pin.OUT)]

numbers = [
    [1,1,1,1,1,1,0], [0,1,1,0,0,0,0], [1,1,0,1,1,0,1], [1,1,1,1,0,0,1],
    [0,1,1,0,0,1,1], [1,0,1,1,0,1,1], [1,0,1,1,1,1,1], [1,1,1,0,0,0,0],
    [1,1,1,1,1,1,1], [1,1,1,1,0,1,1]
]

def display_number(num):
    num_str = f"{num:04d}"
    for _ in range(50):
        for d in range(4):
            digits[d].value(0)
            for s in range(7):
                segments[s].value(numbers[int(num_str[d])][s])
            utime.sleep_ms(3)
            digits[d].value(1)

def play_ecg_bip(pressure):
    interval = int(1000 - (pressure / 4095) * 1500)
    BUZZER.duty(512)
    utime.sleep_ms(100)
    BUZZER.duty(0)
    utime.sleep_ms(interval)

def connect_mqtt():
    print("coucou")
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        print("Connecté au serveur MQTT")
        return client
    except Exception as e:
        print("Erreur MQTT:", e)
        return None

def main():
    mqtt_client = connect_mqtt()

    while True:
        if not mqtt_client:
            mqtt_client = connect_mqtt()

        values = [PRESSURE_SENSOR.read() for _ in range(5)]
        pressure = sum(values) // len(values)
        scaled = int((pressure / 4095) * 9999)

        display_number(scaled)
        print("Pression:", scaled, "/ 9999")

        if scaled > 1000:
            play_ecg_bip(pressure)

        try:
            mqtt_client.publish(MQTT_TOPIC_FSR, str(scaled))
        except:
            mqtt_client = None

        utime.sleep(2)

main()

