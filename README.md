# 🚀 Détection de Son avec Arduino : Activation d’un Moteur et LEDS

## 📖 Description  
Ce projet utilise un **capteur de son**, un **moteur pas à pas** et des **LEDs** pour réagir aux bruits détectés.  
- **Si un son est détecté** → La **LED verte s'allume**, le **moteur tourne** et un **buzzer émet un son**.  
- **Si aucun son n'est détecté** → La **LED rouge s'allume**, et le **moteur s’arrête**.  

## 🔧 Matériel Requis  
- 🎛 **Arduino UNO**  
- 🎤 **Capteur de son (KY-038 ou MAX9814)**  
- 🔴 **LED Rouge** (indique silence)  
- 🟢 **LED Verte** (indique son détecté)  
- 🔊 **Buzzer**  
- 🔄 **Moteur pas à pas 28BYJ-48 + Driver ULN2003**  
- 🛠 **Câbles et Breadboard**  

## ⚡ Schéma de câblage  
<img width="752" alt="image" src="https://github.com/user-attachments/assets/d27069f9-bf85-4836-8a5e-d717b482ae68" />

| **Composant** | **Broche Arduino** |
|--------------|----------------|
| LED Rouge    | 2              |
| LED Verte    | 3              |
| Buzzer       | 4              |
| Capteur Son (OUT) | 6         |
| Capteur Son (Analogique) | A0 |
| Moteur Stepper IN1 | 8 |
| Moteur Stepper IN2 | 10 |
| Moteur Stepper IN3 | 9 |
| Moteur Stepper IN4 | 11 |

## 🚀 Installation et Utilisation  
1. **Branchez les composants** selon le schéma.  
2. **Téléversez le code** sur l’Arduino via l’IDE Arduino.  
3. **Ouvrez le Moniteur Série (`Ctrl + Shift + M`)** pour voir les valeurs du capteur.  
4. **Faites du bruit** (clap, sifflement) pour voir les LEDs et le moteur réagir.  

## 💻 Explication du Code  
- `analogRead(A0)` → Lit le niveau sonore.  
- **Seuil défini (`700`)** → Si le son dépasse cette valeur, le moteur tourne.  
- `tone(buzzer, 440);` → Active un son de fréquence **440Hz** si du bruit est détecté.  
- `myStepper.step(stepsPerRevolution / 8);` → Fait tourner le moteur légèrement.  
- `noTone(buzzer);` → Arrête le buzzer en l’absence de son.  

## 🔥 Améliorations Possibles  
✅ Ajouter un écran LCD pour afficher l’intensité du son.  
✅ Enregistrer les sons détectés et afficher un historique.  
✅ Ajuster automatiquement la sensibilité du capteur.  

## 🏆 Auteur  
Projet réalisé par Les Suceurs de Bits 🚀  
