# Home Assistant Titan IzyPower Integration (avec services de contrôle)

Ceci est une version modifiée d'une intégration personnalisée pour Titan IzyPower.  
Cette version ajoute des services essentiels permettant aux utilisateurs de gérer activement leur batterie Titan IzyPower (ex : Titan 2400, Titan PRO) directement depuis Home Assistant.

L’intégration originale se focalise sur les données de monitoring, tandis que ce fork comble le manque en fournissant des services pour démarrer la charge, la décharge et stopper la batterie, ouvrant la voie à des automatisations avancées telles que le contrôle zéro export.

---

## Modèles supportés

Cette intégration a été testée et fonctionne avec les modèles suivants :

- **Gen 1 :** Titan 2400, Titan 3200
- **Gen 2 :** Titan PRO  

L’intégration fournira automatiquement les bons capteurs selon le modèle choisi lors de la configuration.

---

## Fonctionnalités & Services

Ce fork ajoute les services personnalisés suivants au domaine `titan_izypower`, utilisables dans vos automatisations et scripts :

### `titan_izypower.set_realtime_mode`  
> Mets le dispositif en mode acceptant les commandes de contrôle en temps réel.  
> Ce service doit être appelé une fois après le démarrage de Home Assistant pour assurer un contrôle fiable.

| Paramètre | Obligatoire | Description                |
|-----------|-------------|----------------------------|
| (aucun)   | –           | Active le mode temps réel  |

---

### `titan_izypower.charge`  
> Demande à la batterie de commencer à charger depuis le réseau ou un surplus solaire.

| Paramètre | Obligatoire | Description             | Exemple |
|-----------|-------------|-------------------------|---------|
| power     | Oui         | Puissance de charge (W) | 500     |

---

### `titan_izypower.discharge`  
> Demande à la batterie de commencer à décharger pour alimenter le domicile.

| Paramètre | Obligatoire | Description                  | Exemple  |
|-----------|-------------|------------------------------|----------|
| power     | Oui         | Puissance de décharge (W)    | 300      |

---

### `titan_izypower.stop`  
> Met la batterie en mode veille, stoppant toute charge ou décharge active.

| Paramètre | Obligatoire | Description            |
|-----------|-------------|------------------------|
| (aucun)   | –           | Stoppe la charge/décharge |

---

## Capteurs disponibles

L’intégration crée un ensemble complet de capteurs pour surveiller tous les aspects de votre batterie Titan, incluant :

- **Capteurs de puissance:** puissance entrée DC (par chaîne), puissance totale AC en sortie, puissance batterie, puissance du compteur.
- **Capteurs d’énergie:** production journalière, production cumulée, énergie charge/décharge journalière et totale.
- **Capteurs batterie:** état de charge (SOC), état charge/décharge.
- **Capteurs statut:** mode de fonctionnement, état de la connexion compteur.

---

## Configuration

1. Téléchargez et installez ce composant personnalisé en plaçant les fichiers dans `/homeassistant/custom_components/titan_izypower/`.
2. Dans Home Assistant, allez dans **Paramètres > Appareils & Services**.  
3. Cliquez sur **Ajouter une intégration** et recherchez `TITAN IZYPOWER`.
4. Remplissez les informations demandées :  
    - **Host :** adresse IP de votre appareil Titan.  
    - **Port :** port API (par défaut : `8899`).  
    - **Intervalle de scan :** fréquence d'interrogation en secondes (par défaut : `30`).  
    - **Modèle :** sélectionnez votre modèle Titan dans la liste déroulante.  

---

## Exemples d’automatisations

### 1. Activer le mode temps réel au démarrage

Cette automatisation garantit que l’appareil est prêt à recevoir des commandes en temps réel dès que Home Assistant démarre.

