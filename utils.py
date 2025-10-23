def get_device_gen(device_model: str) -> int:
    """Retourne la génération de l'appareil selon son modèle."""

    titan_gen1_models = ["Titan 2400", "Titan 3200", "Titan PRO"]  # Modèles Gen 1 Titan (exemples)
    if device_model in titan_gen1_models:
        return 1
    else:
        return 2

