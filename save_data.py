import pandas as pd
from config import PER_GAME_OUTPUT_FILE, EASTERN_CONFERENCE_OUTPUT_FILE, WESTERN_CONFERENCE_OUTPUT_FILE

def save_to_csv(per_game_df, eastern_df, western_df):
    # Sauvegarder les données des statistiques par match dans un fichier CSV
    per_game_output = PER_GAME_OUTPUT_FILE  # Référence directe à la constante définie dans config.py
    per_game_df.to_csv(per_game_output, index=False)
    print(f"Données par match sauvegardées dans {per_game_output}")

    # Sauvegarder les données nettoyées des classements des conférences dans des fichiers CSV
    eastern_output = EASTERN_CONFERENCE_OUTPUT_FILE  # Référence directe à la constante définie dans config.py
    western_output = WESTERN_CONFERENCE_OUTPUT_FILE  # Référence directe à la constante définie dans config.py

    if eastern_df is not None:
        eastern_df.to_csv(eastern_output, index=False)
        print(f"Données de la Conférence Est sauvegardées dans {eastern_output}")

    if western_df is not None:
        western_df.to_csv(western_output, index=False)
        print(f"Données de la Conférence Ouest sauvegardées dans {western_output}")
