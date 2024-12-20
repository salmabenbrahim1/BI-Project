import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
per_game_df = pd.read_csv("per_game_data.csv")
eastern_df = pd.read_csv("eastern_conference_data.csv")
western_df = pd.read_csv("western_conference_data.csv")

# Titre du Dashboard
st.title("🏀 Saison NBA 2024-2025 Dashboard")

# --- Dernières statistiques des joueurs ---
st.write("### 📋 Dernières statistiques des joueurs")
st.dataframe(per_game_df.head(20))

# --- Visualisation des meilleurs leaders ---
st.write("### 📊 Les meilleurs leaders de la saison NBA 2024-2025")
donnees_leaders = {
    "Leader WS": {"Joueur": "Shai Gilgeous-Alexander", "Points": 5.2},
    "Leader APG": {"Joueur": "Trae Young", "Points": 12.1},
    "Leader RPG": {"Joueur": "Karl-Anthony Towns", "Points": 13.9},
    "Leader PPG": {"Joueur": "Giannis Antetokounmpo", "Points": 32.7},
}
leaders_df = pd.DataFrame(donnees_leaders).T

# Graphique en barres des leaders
fig, ax = plt.subplots(figsize=(6, 4))
leaders_df["Points"].plot(kind="barh", color=["blue", "orange", "green", "red"], ax=ax)
ax.set_xlabel("Points")
ax.set_title("Les 4 meilleurs leaders NBA de la saison 2024-2025")
ax.set_yticks(range(len(leaders_df)))
ax.set_yticklabels(leaders_df["Joueur"])
st.pyplot(fig)

# --- Graphique des meilleurs joueurs par points ---
st.write("### 🔥 Points moyens des meilleurs joueurs")
top_joueurs = per_game_df.groupby("Player")["Points"].mean().sort_values(ascending=False).head(10)

fig, ax = plt.subplots()
top_joueurs.plot(kind="barh", color="orange", ax=ax)
ax.set_title("Top 10 des joueurs avec la meilleure moyenne de points")
ax.set_xlabel("Points Moyens")
ax.set_ylabel("Joueurs")
st.pyplot(fig)

# --- Moyennes des points par équipe ---
st.write("### 🏀 Moyenne des points par équipe")
moyenne_points_equipe = per_game_df.groupby("Team")["Points"].mean().sort_values(ascending=False)
st.bar_chart(moyenne_points_equipe)

# --- Total des matchs joués par équipe ---
st.write("### 📈 Nombre total de matchs joués par équipe")
total_matchs = per_game_df.groupby("Team")["Games"].sum().sort_values(ascending=False)
st.line_chart(total_matchs)

# --- Filtrer les statistiques d'une équipe ---
equipe_selectionnee = st.selectbox("🔍 Sélectionnez une équipe", per_game_df["Team"].unique())
donnees_equipe = per_game_df[per_game_df["Team"] == equipe_selectionnee]

moyenne_steals = donnees_equipe["Steals"].mean()
moyenne_blocks = donnees_equipe["Blocks"].mean()
moyenne_turnovers = donnees_equipe["Turnovers"].mean()

# Diagramme circulaire des statistiques de l'équipe
stats_equipe = {
    "Vols (Steals)": moyenne_steals,
    "Contres (Blocks)": moyenne_blocks,
    "Pertes de balle (Turnovers)": moyenne_turnovers,
}

st.write(f" Statistiques clés de l'équipe {equipe_selectionnee}")
fig, ax = plt.subplots(figsize=(8, 5))
ax.pie(stats_equipe.values(), labels=stats_equipe.keys(), autopct="%1.1f%%", startangle=140)
ax.set_title(f"Statistiques de l'équipe {equipe_selectionnee}")
st.pyplot(fig)

# --- Classements des conférences ---
conference = st.selectbox("🎯 Sélectionnez une conférence", ["Conférence Est", "Conférence Ouest"])
if conference == "Conférence Est":
    standings_df = eastern_df
else:
    standings_df = western_df

# Affichage des classements
st.write(f"### 🏆 Classement de la {conference}")
st.dataframe(standings_df)

# --- Répartition Victoires/Défaites ---
standings_df["Défaites"] = per_game_df["Games"] - standings_df["Wins"]
victoires = standings_df["Wins"].sum()
defaites = standings_df["Défaites"].sum()

st.write(f"### ⚖️ Répartition des victoires et défaites dans la {conference}")
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie([victoires, defaites], labels=["Victoires", "Défaites"], autopct="%1.1f%%", startangle=90, colors=["green", "red"])
ax.set_title(f"Répartition des victoires et défaites - {conference}")
st.pyplot(fig)

