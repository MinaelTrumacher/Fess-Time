<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fesse Time</title>
    <link rel="stylesheet" href="index.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <!-- Icônes de statut -->
        <i id="status-chair" class="status red fas fa-chair"></i>
        <i id="status-electric" class="status red fas fa-bolt"></i>
        <i id="status-speaker" class="status red fas fa-volume-up"></i>

        <!-- Décompte -->
        <div id="countdown"></div>
    </div>

    <script>
        // Initialisation des capteurs depuis la session
        const capteurs = <?= json_encode($lastSession['capteurs'] ?? []) ?>;
        let countdownActive = false; // Variable pour suivre l'état du décompte
        let countdownInterval = null; // Référence à l'intervalle du décompte
        let incrementingInterval = null; // Référence à l'intervalle d'incrémentation
        let remainingTime = 0; // Temps restant pour le décompte
        let incrementing = false; // Variable pour suivre si le timer est en mode incrémentation
        let countdownFinished = false; // Variable pour indiquer si le décompte est terminé

        // Fonction pour récupérer les données de l'API
        async function fetchLastMessage() {
            try {
                const response = await fetch('http://localhost:3000/last-message');
                if (!response.ok) {
                    throw new Error(`Erreur HTTP : ${response.status}`);
                }
                const data = await response.json();

                // Mise à jour de l'interface utilisateur avec les données
                const chairIcon = document.getElementById('status-chair');
                if (data.isGreaterThanZero) {
                    chairIcon.classList.remove('red');
                    chairIcon.classList.add('green');

                    // Démarrer le décompte si ce n'est pas déjà actif et s'il n'est pas terminé
                    if (!countdownActive && !countdownFinished) {
                        startCountdown(10); // Décompte de 10 secondes
                    }

                    // Arrêter l'incrémentation si la chaise redevient verte
                    if (incrementing) {
                        stopIncrementing();
                    }
                } else {
                    chairIcon.classList.remove('green');
                    chairIcon.classList.add('red');

                    // Si le décompte est actif ou terminé, passer en mode incrémentation
                    if ((!countdownActive || countdownFinished) && !incrementing) {
                        startIncrementing();
                    }
                }
            } catch (error) {
                console.error('Erreur lors de la récupération des données :', error);
            }
        }

        // Fonction pour démarrer le décompte
        function startCountdown(duration) {
            const countdown = document.getElementById('countdown');

            if (countdownActive || incrementing) {
                return; // Empêche de démarrer un nouveau décompte si un est déjà actif
            }

            remainingTime = duration; // Initialise le temps restant
            countdownActive = true; // Indique qu'un décompte est actif
            countdownFinished = false; // Réinitialise l'état terminé

            countdown.textContent = remainingTime;

            countdownInterval = setInterval(() => {
                remainingTime--;

                // Met à jour le décompte
                countdown.textContent = remainingTime;

                // Lorsque le temps est écoulé, arrête le décompte
                if (remainingTime <= 0) {
                    clearInterval(countdownInterval);
                    countdown.textContent = "0"; // Affiche "0" au lieu de "Terminé"
                    countdownActive = false; // Décompte terminé
                    countdownFinished = true; // Marque le décompte comme terminé

                    // Rendre le haut-parleur vert
                    const speakerIcon = document.getElementById('status-speaker');
                    speakerIcon.classList.remove('red');
                    speakerIcon.classList.add('green');
                }
            }, 1000);
        }

        // Fonction pour arrêter le décompte
        function stopCountdown() {
            if (countdownInterval) {
                clearInterval(countdownInterval);
                countdownInterval = null;
            }
            countdownActive = false;
        }

        // Fonction pour démarrer l'incrémentation
        function startIncrementing() {
            const countdown = document.getElementById('countdown');

            if (incrementing) {
                return; // Empêche de démarrer une nouvelle incrémentation si elle est déjà active
            }

            incrementing = true; // Activer le mode incrémentation

            incrementingInterval = setInterval(() => {
                if (remainingTime < 10) {
                    remainingTime++;

                    // Met à jour le décompte
                    countdown.textContent = remainingTime;
                } else {
                    // Arrêter l'incrémentation si le temps atteint 10
                    stopIncrementing();
                }
            }, 1000);
        }

        // Fonction pour arrêter l'incrémentation
        function stopIncrementing() {
            if (incrementingInterval) {
                clearInterval(incrementingInterval);
                incrementingInterval = null;
            }
            incrementing = false;
        }

        // Initialisation
        fetchLastMessage(); // Appel initial pour récupérer les données
        setInterval(fetchLastMessage, 1000); // Vérifie les données toutes les secondes
    </script>
</body>
</html>