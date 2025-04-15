#!/bin/bash

set -e

echo "Début de l'installation et configuration du bridge Mosquitto -> HiveMQ..."

# Configuration utilisateur (à remplacer par les informations utilisateurs)
HIVEMQ_ADDRESS="79ccad09e94e4d9ea9e2652324bb5a64.s1.eu.hivemq.cloud" # Votre adresse HiveMQ
HIVEMQ_PORT=8883 # Votre port HiveMQ
HIVEMQ_USERNAME="admin" # Votre nom d'utilisateur HiveMQ
HIVEMQ_PASSWORD="Admin31!" # Votre mot de passe HiveMQ
CLIENT_ID="mosq_bridge_01" # Votre ID client
TOPIC="sensor/#" # Votre topic
CERT_PATH="/etc/mosquitto/certs/hivemq_ca.pem" # Votre chemin de certificat
BRIDGE_CONF_PATH="/etc/mosquitto/conf.d/hivemq_bridge.conf" # Votre chemin de configuration bridge
MOSQ_CONF="/etc/mosquitto/mosquitto.conf" # Votre chemin de configuration Mosquitto

# Installation de Mosquitto si non présent
if ! command -v mosquitto &> /dev/null; then
    echo "Installation de Mosquitto..."
    sudo apt update && sudo apt install -y mosquitto mosquitto-clients
fi

# Création du dossier de certificats
echo "Création du dossier des certificats..."
sudo mkdir -p /etc/mosquitto/certs

# Téléchargement du certificat ISRG Root X1
echo "Téléchargement du certificat de confiance Let's Encrypt..."
sudo wget -q https://letsencrypt.org/certs/isrgrootx1.pem -O "$CERT_PATH"

# Configuration du bridge
echo "Écriture de la configuration du bridge..."
sudo tee "$BRIDGE_CONF_PATH" > /dev/null <<EOF
connection bridge-to-hivemq
address $HIVEMQ_ADDRESS:$HIVEMQ_PORT

topic $TOPIC both 0

bridge_cafile $CERT_PATH
tls_version tlsv1.2
bridge_protocol_version mqttv311

clientid $CLIENT_ID
username $HIVEMQ_USERNAME
password $HIVEMQ_PASSWORD

keepalive_interval 60
cleansession true
try_private false
EOF

# Ajout du include_dir si manquant
if ! grep -q "include_dir /etc/mosquitto/conf.d" "$MOSQ_CONF"; then
    echo "Ajout de include_dir dans $MOSQ_CONF"
    echo "include_dir /etc/mosquitto/conf.d" | sudo tee -a "$MOSQ_CONF" > /dev/null
fi

# Redémarrage du service
echo "Redémarrage du service Mosquitto..."
sudo systemctl restart mosquitto

echo "Configuration terminée. Vérifiez les logs avec :"
echo "sudo journalctl -u mosquitto -f"
