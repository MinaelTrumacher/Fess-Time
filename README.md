🚀 Détection de Pression avec ESP32 : Activation d’un Afficheur 7 segments et d'un Haut-parleur

## 📖 Description  
Ce projet utilise un **capteur de force** et un **afficheur 7 segments**, un **haut-parleur** pour réagir à la force détectés.  
- **Si une pression est détecté** → L'**afficheur 7 segments** affiche XXXX, le **haut-parleur** émet un son.  
- **Si aucune pression n'est détecté** → L'**afficheur 7 segments** affiche 0000, le **haut-parleur** n'émet pas de son.  

## 🔧 Matériel Requis  
- 🔢 **Afficheur 7 segments** (affiche la pression)
- 🗜 **Force Censor Resistence (FCR)**  
- 🔊 **Haut-parleur** (indique une pression)  
- 🔋**Module Batterie**
- ⏸ **x7 Résistance**
- 🎮 **ESP32** (microcontroller)

## ⚡ Schéma de câblage  
![Shéma de cablage](https://github.com/user-attachments/assets/ce21d2d2-3df9-4a91-b573-f3e313986114)

| **Composant** | **Port ESP32** |
|---------------|----------------|
| Afficheur 7 segments | 23      |
| Afficheur 7 segments | 18      |
| Afficheur 7 segments | 19      |
| Afficheur 7 segments | 13      |
| Afficheur 7 segments | 12      |
| Afficheur 7 segments | 5       |
| Afficheur 7 segments | 15      | + resistance
| Afficheur 7 segments | 2       | + resistance
| Afficheur 7 segments | 22      | + resistance
| Afficheur 7 segments | 4       | + resistance
| Afficheur 7 segments | 21      | + resistance
| Afficheur 7 segments | 14      | + resistance
| Force Censor Resistence (FCR) | 3v3             |
| Force Censor Resistence (FCR) | 34              | + resistance -> GND
| Haut-parleur | 25              |
| Haut-parleur | GND             |

## 🚀 Installation et Utilisation  
1. **Branchez les composants** selon le schéma.
2. **Télécharger le projet** via Git
3. **Modifier les information** de connection au wifi dans le code (SSID, Mot de Passe)
4. **Téléversez le code** sur l’ESP32 via l’IDE Thonny.
5. **Lancer le script** (nom du script) sur la Raspberry Pi [indisponible]
6. **Lancer le code** sur l’ESP32 via l’IDE Thonny.
7. **Pressez le FCR** pour voir les valeurs du capteur s'afficher et le haut parleur bipper.  

## 🏆 Auteur  
Projet réalisé par Fess-Time 🚀  
