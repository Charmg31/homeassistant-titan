Intégration Home Assistant Titan IzyPower (avec commandes de contrôle)
Ce projet propose une adaptation personnalisée de l’intégration Indevolt disponible ici : https://github.com/solarmanpv/homeassistant-indevolt
Grâce à cette version, il est désormais possible de piloter directement la batterie Titan IzyPower (modèles Titan 2400, ou futur Titan PRO) via Home Assistant, en ajoutant des services dédiés pour automatiser la gestion de la charge, de la décharge, ou l’arrêt de la batterie.

L’intégration d’origine se concentre sur la supervision ; ce fork vient compléter la solution avec des fonctionnalités de pilotage essentielles, idéales pour des automatisations avancées – comme l’activation du mode zéro export.

Modèles compatibles
Cette intégration a été prévue pour fonctionner sur les modèles suivants :

Génération 1 : Titan 2400, Titan 3200

Génération future : Titan PRO

En fonction du modèle sélectionné lors de l’installation, les bons capteurs seront automatiquement configurés.

Fonctions & services personnalisés
Ce fork enrichit le domaine titan_izypower de nouveaux services, à intégrer dans vos scripts ou automatisations :

titan_izypower.set_realtime_mode
Permet au dispositif de recevoir des commandes en temps réel.
À appeler une fois après chaque redémarrage de Home Assistant pour garantir la réactivité.

Paramètre	Requis	Description
(aucun)	–	Active le mode temps réel
titan_izypower.charge
Lance la charge de la batterie depuis le réseau ou via un surplus solaire.

Paramètre	Requis	Description	Exemple
power	Oui	Intensité de charge (W)	500
titan_izypower.discharge
Lance la décharge de la batterie pour alimenter le logement.

Paramètre	Requis	Description	Exemple
power	Oui	Intensité de décharge (W)	300
titan_izypower.stop
Met le système en veille et interrompt toute opération de charge/décharge en cours.

Paramètre	Requis	Description
(aucun)	–	Arrête la charge/décharge
Suivi et capteurs intégrés
Une gamme complète de capteurs permet de suivre précisément l’activité de votre batterie, notamment :

Capteurs de puissance : puissance DC d’entrée (par string), puissance totale AC délivrée, puissance batterie, relevé compteur.

Capteurs d’énergie : suivi production quotidienne et cumulative, énergie totale de charge/décharge (jour et cumulé).

Capteurs batterie : indication du SOC et activité (charge/décharge).

Capteurs de statut : mode actuel et état de connexion au compteur.

Installation et configuration
Placez les fichiers de ce composant dans le dossier /homeassistant/custom_components/titan_izypower/.

Accédez à Paramètres > Appareils & Services dans Home Assistant.

Appuyez sur Ajouter une intégration et cherchez TITAN IZYPOWER.

Entrez les informations requises :

Host : IP de l’onduleur Titan

Port : port API, généralement 8899

Intervalle de scan : fréquence d’interrogation (défaut : 30 s)

Modèle : choisissez le modèle dans la liste proposée
