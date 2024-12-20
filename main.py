from fetch_data import fetch_nba_data
from clean_data import clean_per_game_data, clean_conference_standings_data
from save_data import save_to_csv
from config import NBA_2025_STANDINGS_URL, NBA_2025_PER_GAME_URL
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup

def extract_per_game_table(html_content):
    # Utiliser BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(html_content, "html.parser")
    per_game_table = soup.find("table", {"id": "per_game_stats"})

    # Vérifier si la table des statistiques par match est présente
    if per_game_table:
        return pd.read_html(StringIO(str(per_game_table)))[0]
    else:
        print("La table des statistiques par match n'a pas été trouvée !")
        return None

def extract_conference_standings(html_content):
    # Utiliser BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(html_content, "html.parser")
    division_standings = {}

    # Essayer de trouver la table des classements de la Conférence Est
    E = soup.find("table", {"id": "confs_standings_E"})
    if E:
        print("Classement de la Conférence Est trouvé !")
        division_standings["Eastern Conference"] = pd.read_html(StringIO(str(E)))[0]
    else:
        print("La table des classements de la Conférence Est n'a pas été trouvée !")

    # Essayer de trouver la table des classements de la Conférence Ouest
    W = soup.find("table", {"id": "confs_standings_W"})
    if W:
        print("Classement de la Conférence Ouest trouvé !")
        division_standings["Western Conference"] = pd.read_html(StringIO(str(W)))[0]
    else:
        print("La table des classements de la Conférence Ouest n'a pas été trouvée !")

    return division_standings

def main():
    # Récupérer les données de la page des classements
    standings_html_content = fetch_nba_data(NBA_2025_STANDINGS_URL)
    if standings_html_content:
        division_standings = extract_conference_standings(standings_html_content)

        # Extraire les DataFrames pour les conférences Est et Ouest
        eastern_df = division_standings.get("Eastern Conference")
        western_df = division_standings.get("Western Conference")

    # Récupérer les données de la page des statistiques par match
    per_game_html_content = fetch_nba_data(NBA_2025_PER_GAME_URL)
    if per_game_html_content:
        per_game_df = extract_per_game_table(per_game_html_content)
        if per_game_df is not None:
            # Nettoyer les données des statistiques par match
            cleaned_per_game_df = clean_per_game_data(per_game_df)

            # Nettoyer les données des classements des conférences
            cleaned_eastern_df = clean_conference_standings_data(eastern_df, "Eastern Conference") if eastern_df is not None else None
            cleaned_western_df = clean_conference_standings_data(western_df, "Western Conference") if western_df is not None else None

            # Sauvegarder les données nettoyées au format CSV en utilisant les chemins définis dans config.py
            save_to_csv(cleaned_per_game_df, cleaned_eastern_df, cleaned_western_df)

if __name__ == "__main__":
    main()
