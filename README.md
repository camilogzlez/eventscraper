# Scraped Activities Project
![image](https://github.com/user-attachments/assets/dd802ed0-3adc-400f-ae1a-2f1ceedaaaf3)


## Overview

This project is designed to scrape activities from Eventbrite, TripAdvisor, and Facebook, providing users with a centralized platform to explore and interact with various events. The application integrates:

- **Backend**: Python with Flask (using a virtual environment `venv`).
- **Frontend**: Vue.js with Vuetify and Tailwind CSS for styling.
- **Map Service**: OpenStreetMap for displaying event locations.
- **AI Integration**: Google Dialogflow for intelligent user interactions.

---

## Features

- Scrape and aggregate activities from multiple platforms.
- Interactive map with event markers using OpenStreetMap.
- User-friendly interface with Vuetify and Tailwind.
- AI-powered queries for activities using Dialogflow.

---

## Installation and Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- Virtual environment for Python (`venv`)

---

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/camilogzlez/eventscraper

   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add your credentials in a `.env` file:

   ```env
   FB_EMAIL=your-facebook-email
   FB_PASSWORD=your-facebook-password
   GOOGLE_APPLICATION_CREDENTIALS=path-to-your-google-credentials.json
   GOOGLE_PROJECT_ID=your-google-project-id
   ```

5. Run the backend server:

   ```bash
   flask run
   ```

   The backend will be available at `http://127.0.0.1:5000`.

---

### Frontend Setup

1. Navigate to the frontend folder:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the development server:

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:4173`.

4. Use ngrok to expose the backend:

   ```bash
   ngrok http 5000
   ```

   Copy the ngrok URL and replace the backend URL in the frontend configuration.

---

## Future Improvements

- **Performance Optimization**: Enhance scraping efficiency with asynchronous processing.
- **Additional Platforms**: Integrate more event platforms (e.g., Meetup, Ticketmaster).
- **Advanced Filtering**: Add more granular filters (e.g., price range, event type).
- **User Accounts**: Implement authentication for personalized event recommendations.
- **Map Features**: Add clustering for nearby events on the map.
- **AI Improvements**: Enhance Dialogflow integration with more conversational scenarios.

---

Français

Ce projet est conçu pour récupérer des activités depuis Eventbrite, TripAdvisor et Facebook, offrant aux utilisateurs une plateforme centralisée pour explorer et interagir avec divers événements. L'application intègre :

- **Backend** : Python avec Flask (utilisant un environnement virtuel `venv`).
- **Frontend** : Vue.js avec Vuetify et Tailwind CSS pour le style.
- **Service de Carte** : OpenStreetMap pour afficher les localisations des événements.
- **Intégration IA** : Google Dialogflow pour des interactions intelligentes.

---

### Fonctionnalités

- Récupération et agrégation des activités de plusieurs plateformes.
- Carte interactive avec des marqueurs d’événements via OpenStreetMap.
- Interface conviviale avec Vuetify et Tailwind.
- Requêtes intelligentes pour les activités via Dialogflow.

---

### Installation et Configuration

#### Prérequis

- Python 3.9+
- Node.js 16+
- npm ou yarn
- Environnement virtuel pour Python (`venv`)

---

#### Configuration du Backend

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/camilogzlez/eventscraper
   ```

2. Créez et activez un environnement virtuel :

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Ajoutez vos informations d'identification dans un fichier `.env` :

   ```env
   FB_EMAIL=votre-email-facebook
   FB_PASSWORD=votre-mot-de-passe-facebook
   GOOGLE_APPLICATION_CREDENTIALS=chemin-vers-vos-credentials-google.json
   GOOGLE_PROJECT_ID=your-google-project-id
   ```

5. Lancez le serveur backend :

   ```bash
   flask run
   ```

   Le backend sera accessible à `http://127.0.0.1:5000`.

---

#### Configuration du Frontend

1. Naviguez vers le dossier frontend :

   ```bash
   cd ../frontend
   ```

2. Installez les dépendances :

   ```bash
   npm install
   ```

3. Lancez le serveur de développement :

   ```bash
   npm run dev
   ```

   Le frontend sera accessible à `http://localhost:4173`.

4. Utilisez ngrok pour exposer le backend :

   ```bash
   ngrok http 5000
   ```

   Copiez l'URL ngrok et remplacez l'URL du backend dans la configuration frontend.

---

### Améliorations

- **Optimisation des performances** : Améliorer l’efficacité du scraping avec un traitement asynchrone.
- **Nouvelles plateformes** : Intégrer davantage de plateformes d’événements (par ex., Meetup, Ticketmaster).
- **Filtrage avancé** : Ajouter des filtres plus granulaires (par ex., gamme de prix, type d’événement).
- **Comptes utilisateur** : Implémenter l’authentification pour des recommandations personnalisées.
- **Fonctionnalités cartographiques** : Ajouter un regroupement pour les événements proches sur la carte.
- **Améliorations IA** : Améliorer l’intégration de Dialogflow avec des scénarios conversationnels plus riches.

---

