import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_data import fetch_nba_data
from clean_data import clean_per_game_data, clean_conference_standings_data
from io import StringIO
from bs4 import BeautifulSoup
from config import *

# Function to extract per game stats
def extract_per_game_table(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    per_game_table = soup.find("table", {"id": "per_game_stats"})
    if per_game_table:
        return pd.read_html(StringIO(str(per_game_table)))[0]
    else:
        print("La table des statistiques par match n'a pas été trouvée !")
        return None

# Function to extract conference standings
def extract_conference_standings(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    division_standings = {}

    # Conference East
    E = soup.find("table", {"id": "confs_standings_E"})
    if E:
        division_standings["Eastern Conference"] = pd.read_html(StringIO(str(E)))[0]

    # Conference West
    W = soup.find("table", {"id": "confs_standings_W"})
    if W:
        division_standings["Western Conference"] = pd.read_html(StringIO(str(W)))[0]

    return division_standings

# Main function for processing data and rendering the dashboard
def main():
    # Fetch data
    standings_html_content = fetch_nba_data(NBA_2025_STANDINGS_URL)
    per_game_html_content = fetch_nba_data(NBA_2025_PER_GAME_URL)

    if standings_html_content and per_game_html_content:
        # Extract data
        division_standings = extract_conference_standings(standings_html_content)
        per_game_df = extract_per_game_table(per_game_html_content)

        # Clean the data
        cleaned_per_game_df = clean_per_game_data(per_game_df)
        eastern_df = clean_conference_standings_data(division_standings.get("Eastern Conference"), "Eastern Conference")
        western_df = clean_conference_standings_data(division_standings.get("Western Conference"), "Western Conference")

        # Pass the cleaned data directly to the dashboard
        render_dashboard(cleaned_per_game_df, eastern_df, western_df)

# Function to render the Streamlit dashboard
def render_dashboard(per_game_df, eastern_df, western_df):
    # Title
    st.title("🏀 Saison NBA 2024-2025 Dashboard")

    # Display player stats
    st.write("### 📋 Dernières statistiques des joueurs")
    st.dataframe(per_game_df.head(20))

    # Best leaders
    st.write("### 📊 Les meilleurs leaders de la saison NBA 2024-2025")
    leaders_data = {
        "Leader WS": {"Joueur": "Shai Gilgeous-Alexander", "Points": 5.2},
        "Leader APG": {"Joueur": "Trae Young", "Points": 12.1},
        "Leader RPG": {"Joueur": "Karl-Anthony Towns", "Points": 13.9},
        "Leader PPG": {"Joueur": "Giannis Antetokounmpo", "Points": 32.7},
    }
    leaders_df = pd.DataFrame(leaders_data).T

    # Bar chart for best leaders
    fig, ax = plt.subplots(figsize=(6, 4))
    leaders_df["Points"].plot(kind="barh", color=["blue", "orange", "green", "red"], ax=ax)
    ax.set_xlabel("Points")
    ax.set_title("Les 4 meilleurs leaders NBA de la saison 2024-2025")
    ax.set_yticks(range(len(leaders_df)))
    ax.set_yticklabels(leaders_df["Joueur"])
    st.pyplot(fig)

    # Top players by points
    st.write("### 🔥 Points moyens des meilleurs joueurs")
    top_players = per_game_df.groupby("Player")["Points"].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots()
    top_players.plot(kind="barh", color="orange", ax=ax)
    ax.set_title("Top 10 des joueurs avec la meilleure moyenne de points")
    ax.set_xlabel("Points Moyens")
    ax.set_ylabel("Joueurs")
    st.pyplot(fig)

    # Points by team
    st.write("### 🏀 Moyenne des points par équipe")
    team_avg_points = per_game_df.groupby("Team")["Points"].mean().sort_values(ascending=False)
    st.bar_chart(team_avg_points)

    # Total games played by team
    st.write("### 📈 Nombre total de matchs joués par équipe")
    total_games = per_game_df.groupby("Team")["Games"].sum().sort_values(ascending=False)
    st.line_chart(total_games)

    # Filter by selected team
    selected_team = st.selectbox("🔍 Sélectionnez une équipe", per_game_df["Team"].unique())
    team_data = per_game_df[per_game_df["Team"] == selected_team]

    steals_avg = team_data["Steals"].mean()
    blocks_avg = team_data["Blocks"].mean()
    turnovers_avg = team_data["Turnovers"].mean()

    # Pie chart for team stats
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

    # Conference standings selection
    conference = st.selectbox("🎯 Sélectionnez une conférence", ["Conférence Est", "Conférence Ouest"])
    standings_df = eastern_df if conference == "Conférence Est" else western_df
    st.write(f"### 🏆 Classement de la {conference}")
    st.dataframe(standings_df)

    # Victory/Defeat distribution
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
