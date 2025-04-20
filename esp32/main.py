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

def update_display(value):
    """Affiche une valeur MMSS (ex: 30 min => 3000) en boucle pour garder l'affichage allumé"""
    num_str = f"{value:04d}"
    for d in range(4):
        digits[d].value(0)  # activer le digit courant
        for s in range(7):
            segments[s].value(numbers[int(num_str[d])][s])
        utime.sleep_ms(2)
        digits[d].value(1)  # désactiver après affichage

def connect_mqtt():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        print("Connecté au serveur MQTT")
        return client
    except Exception as e:
        print("Erreur MQTT:", e)
        return None

def read_pressure():
    values = [PRESSURE_SENSOR.read() for _ in range(5)]
    return sum(values) // len(values)

def main():
    mqtt_client = connect_mqtt()

    MAX_TIMER = 10  # ⏱️ 10 secondes
    timer = MAX_TIMER
    last_second = utime.time()

    while True:
        now = utime.time()

        pressure = read_pressure()
        force_applied = pressure > 100  # seuil à adapter selon ton capteur

        # Si une seconde s’est écoulée, on modifie le timer
        if now != last_second:
            last_second = now

            if force_applied:
                timer = max(0, timer - 1)
            else:
                timer = min(MAX_TIMER, timer + 1)

            print(f"Timer: {timer} sec | Pression: {pressure}")

            # Envoi MQTT
            if mqtt_client:
                try:
                    mqtt_client.publish(MQTT_TOPIC_FSR, str(pressure))
                except:
                    mqtt_client = None

            # Buzzer + vibreur si timer = 0 ET force encore présente
            if timer == 0 and force_applied:
                BUZZER.duty(512)
            else:
                BUZZER.duty(0)

        # Conversion MM.SS
        minutes = timer // 60
        seconds = timer % 60
        display_value = minutes * 100  + seconds  # ex: 0*100 + 30 => 0030

        # Maintenir affichage allumé en continu
        update_display(display_value)

        utime.sleep_ms(5)  # permet une boucle fluide sans bloquer l'affichage

main()
