require('dotenv').config();
const express = require("express");
const mysql = require("mysql2");

const app = express();
const PORT = 3000;

// Configurer la connexion MySQL
const mysqlConnection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

// Vérifier la connexion MySQL
mysqlConnection.connect((err) => {
  if (err) {
    console.error("❌ Erreur de connexion à la base de données MySQL :", err);
    process.exit(1);
  }
  console.log("✅ Connecté à la base de données MySQL !");
});

// Route GET pour récupérer toutes les sessions
app.get("/sessions", async (req, res) => {
  try {
    const query = "SELECT * FROM sessions";
    mysqlConnection.query(query, (err, results) => {
      if (err) {
        console.error("❌ Erreur lors de la récupération des sessions :", err);
        return res.status(500).json({ error: "Erreur lors de la récupération des sessions" });
      }

      res.status(200).json(results);
    });
  } catch (error) {
    console.error("❌ Erreur lors de la récupération des sessions :", error);
    res.status(500).json({ error: "Erreur lors de la récupération des sessions" });
  }
});

// Route GET pour récupérer tous les capteurs
app.get("/capteurs", async (req, res) => {
  try {
    const query = "SELECT * FROM capteurs";
    mysqlConnection.query(query, (err, results) => {
      if (err) {
        console.error("❌ Erreur lors de la récupération des capteurs :", err);
        return res.status(500).json({ error: "Erreur lors de la récupération des capteurs" });
      }

      res.status(200).json(results);
    });
  } catch (error) {
    console.error("❌ Erreur lors de la récupération des capteurs :", error);
    res.status(500).json({ error: "Erreur lors de la récupération des capteurs" });
  }
});

// Route GET pour récupérer la dernière session avec l'état des capteurs
app.get("/sessions/last", async (req, res) => {
  try {
    const query = `
      SELECT s.id AS session_id, s.start_time, s.end_time,
             c.capteur_pression, c.minuteur, c.haut_parleur, c.vibreur
      FROM sessions s
      LEFT JOIN capteurs c ON s.id = c.session_id
      ORDER BY s.start_time DESC
      LIMIT 1;
    `;

    mysqlConnection.query(query, (err, results) => {
      if (err) {
        console.error("❌ Erreur lors de la récupération de la dernière session :", err);
        return res.status(500).json({ error: "Erreur lors de la récupération de la dernière session" });
      }

      if (results.length === 0) {
        return res.status(404).json({ error: "Aucune session trouvée" });
      }

      const row = results[0];
      const session = {
        id: row.session_id,
        start_time: row.start_time,
        end_time: row.end_time,
        capteurs: {
          capteur_pression: row.capteur_pression,
          minuteur: row.minuteur,
          haut_parleur: row.haut_parleur,
          vibreur: row.vibreur,
        },
      };

      res.status(200).json(session);
    });
  } catch (error) {
    console.error("❌ Erreur lors de la récupération de la dernière session :", error);
    res.status(500).json({ error: "Erreur lors de la récupération de la dernière session" });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Serveur démarré sur http://localhost:${PORT}`);
});