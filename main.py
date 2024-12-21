import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_data import fetch_nba_data
from clean_data import clean_per_game_data, clean_conference_standings_data
from io import StringIO
from bs4 import BeautifulSoup
from config import *
# extraire les statistiques par match
def extract_per_game_table(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    per_game_table = soup.find("table", {"id": "per_game_stats"})
    if per_game_table:
        return pd.read_html(StringIO(str(per_game_table)))[0]
    else:
        print("La table des statistiques par match n'a pas été trouvée !")
        return None

#  extraire les classements des conférences
def extract_conference_standings(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    division_standings = {}

    # Conférence Est
    E = soup.find("table", {"id": "confs_standings_E"})
    if E:
        division_standings["Eastern Conference"] = pd.read_html(StringIO(str(E)))[0]

    # Conférence Ouest
    W = soup.find("table", {"id": "confs_standings_W"})
    if W:
        division_standings["Western Conference"] = pd.read_html(StringIO(str(W)))[0]

    return division_standings

# Fonction principale pour traiter les données et afficher le tableau de bord
def main():
    # Récupérer les données
    standings_html_content = fetch_nba_data(NBA_2025_STANDINGS_URL)
    per_game_html_content = fetch_nba_data(NBA_2025_PER_GAME_URL)

    if standings_html_content and per_game_html_content:
        # Extraire les données
        division_standings = extract_conference_standings(standings_html_content)
        per_game_df = extract_per_game_table(per_game_html_content)

        # Nettoyer les données
        cleaned_per_game_df = clean_per_game_data(per_game_df)
        eastern_df = clean_conference_standings_data(division_standings.get("Eastern Conference"), "Eastern Conference")
        western_df = clean_conference_standings_data(division_standings.get("Western Conference"), "Western Conference")

        # Passer les données nettoyées directement au tableau de bord
        render_dashboard(cleaned_per_game_df, eastern_df, western_df)

# afficher le tableau de bord Streamlit
def render_dashboard(per_game_df, eastern_df, western_df):
    # Titre
    st.title("🏀 Saison NBA 2024-2025 Dashboard")

    # Afficher les statistiques des joueurs
    st.write("### 📋 Dernières statistiques des joueurs par match")
    st.dataframe(per_game_df)

    # Meilleurs leaders
    st.write("### 📊 Les meilleurs leaders de la saison NBA 2024-2025")
    leaders_data = {
        "Leader WS": {"Joueur": "Shai Gilgeous-Alexander", "Points": 5.2},
        "Leader APG": {"Joueur": "Trae Young", "Points": 12.1},
        "Leader RPG": {"Joueur": "Karl-Anthony Towns", "Points": 13.9},
        "Leader PPG": {"Joueur": "Giannis Antetokounmpo", "Points": 32.7},
    }
    leaders_df = pd.DataFrame(leaders_data).T

    # Diagramme en barres pour les meilleurs leaders
    fig, ax = plt.subplots(figsize=(6, 4))
    leaders_df["Points"].plot(kind="barh", color=["blue", "orange", "green", "red"], ax=ax)
    ax.set_xlabel("Points")
    ax.set_title("Les 4 meilleurs leaders NBA de la saison 2024-2025")
    ax.set_yticks(range(len(leaders_df)))
    ax.set_yticklabels(leaders_df["Joueur"])
    st.pyplot(fig)

    # Joueurs avec le plus de points
    st.write("### 🔥 Points moyens des meilleurs joueurs")
    top_players = per_game_df.groupby("Player")["Points"].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots()
    top_players.plot(kind="barh", color="orange", ax=ax)
    ax.set_title("Top 10 des joueurs avec la meilleure moyenne de points")
    ax.set_xlabel("Points Moyens")
    ax.set_ylabel("Joueurs")
    st.pyplot(fig)

    # Moyenne des points par équipe
    st.write("### 🏀 Moyenne des points par équipe")
    team_avg_points = per_game_df.groupby("Team")["Points"].mean().sort_values(ascending=False)
    st.bar_chart(team_avg_points)

    # Nombre total de matchs joués par équipe
    st.write("### 📈 Nombre total de matchs joués par équipe")
    total_games = per_game_df.groupby("Team")["Games"].sum().sort_values(ascending=False)
    st.line_chart(total_games)

    # Filtrer par équipe sélectionnée
    selected_team = st.selectbox("🔍 Sélectionnez une équipe", per_game_df["Team"].unique())
    team_data = per_game_df[per_game_df["Team"] == selected_team]

    steals_avg = team_data["Steals"].mean()
    blocks_avg = team_data["Blocks"].mean()
    turnovers_avg = team_data["Turnovers"].mean()

    # Diagramme circulaire pour les statistiques d'équipe
    team_stats = {
        "Vols (Steals)": steals_avg,
        "Contres (Blocks)": blocks_avg,
        "Pertes de balle (Turnovers)": turnovers_avg,
    }

    st.write(f"Statistiques clés de l'équipe {selected_team}")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(team_stats.values(), labels=team_stats.keys(), autopct="%1.1f%%", startangle=140)
    ax.set_title(f"Statistiques de l'équipe {selected_team}")
    st.pyplot(fig)

    # Sélection des conférences
    conference = st.selectbox("🎯 Sélectionnez une conférence", ["Conférence Est", "Conférence Ouest"])
    standings_df = eastern_df if conference == "Conférence Est" else western_df
    st.write(f"### 🏆 Classement de la {conference}")
    st.dataframe(standings_df)

    # Répartition victoires/défaites
    standings_df["Défaites"] = per_game_df["Games"] - standings_df["Wins"]
    victories = standings_df["Wins"].sum()
    defeats = standings_df["Défaites"].sum()

    st.write(f"### ⚖️ Répartition des victoires et défaites dans la {conference}")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie([victories, defeats], labels=["Victoires", "Défaites"], autopct="%1.1f%%", startangle=90, colors=["green", "red"])
    ax.set_title(f"Répartition des victoires et défaites - {conference}")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
