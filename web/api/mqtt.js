require('dotenv').config();
const mqtt = require('mqtt');
const express = require('express');
const cors = require('cors'); // Importer le middleware CORS

const app = express();
const PORT = 3000;

// Activer CORS pour toutes les requêtes
app.use(cors());

// Configuration du broker HiveMQ
const broker = process.env.MQTT_BROKER; // Adresse du broker
const port = process.env.MQTT_PORT; // Port du broker
const username = process.env.MQTT_USERNAME; // Nom d'utilisateur
const password = process.env.MQTT_PASSWORD; // Mot de passe

// Connexion au broker HiveMQ
const client = mqtt.connect(`mqtts://${broker}:${port}`, {
  username,
  password,
});

// Variable pour stocker la dernière valeur reçue
let lastMessageValue = null;

// Connexion au broker MQTT
client.on('connect', () => {
  console.log('✅ Connecté au broker HiveMQ');

  // Souscrire au topic
  const topic = 'sensor/#'; // Remplacez par le topic que vous souhaitez écouter
  client.subscribe(topic, (err) => {
    if (err) {
      console.error('❌ Erreur lors de la souscription :', err);
    } else {
      console.log(`✅ Souscrit au topic : ${topic}`);
    }
  });
});

// Gestion des erreurs de connexion
client.on('error', (err) => {
  console.error('❌ Erreur de connexion :', err);
});

// Récupérer les messages publiés sur le topic
client.on('message', (topic, message) => {
  const messageValue = parseInt(message.toString(), 10); // Convertir le message en entier
  console.log('📩 Un message a été reçu :');
  console.log(`📌 Topic : ${topic}`);
  console.log(`📄 Message : ${messageValue}`);

  // Mettre à jour la dernière valeur si elle est valide
  if (!isNaN(messageValue)) {
    lastMessageValue = messageValue;
  }
});

// Route GET pour récupérer la dernière valeur et vérifier si elle est > 0
app.get('/last-message', (req, res) => {
  if (lastMessageValue === null) {
    return res.status(404).json({ error: 'Aucun message reçu pour le moment' });
  }

  res.status(200).json({
    value: lastMessageValue,
    isGreaterThanZero: lastMessageValue > 100,
  });
});

// Démarrer le serveur
app.listen(PORT, () => {
  console.log(`✅ Serveur démarré sur http://localhost:${PORT}`);
});