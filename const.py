from homeassistant.const import Platform

DOMAIN = "titan_izypower"  # Met le même nom que ton dossier d'intégration
DEFAULT_PORT = 8899        # Mets le port par défaut de la Titan si besoin
DEFAULT_SCAN_INTERVAL = 30
PLATFORMS = [
    Platform.SENSOR
]

SUPPORTED_MODELS = [
    "Titan 2400",
    "Titan 3200",
    "Titan PRO",
    # Ajoute ici tous les modèles Titan IzyPower à supporter
]
