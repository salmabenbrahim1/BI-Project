import pandas as pd

def clean_per_game_data(df):
    # Supprimer les colonnes inutiles
    if 'Rk' in df.columns:
        df.drop(columns=['Rk'], inplace=True)
    if 'Awards' in df.columns:
        df.drop(columns=['Awards'], inplace=True)

    # Renommer les colonnes pour assurer la cohérence
    df.rename(columns={
        'Pos': 'Position',
        'Tm': 'Team',
        'G': 'Games',
        'GS': 'Games Started',
        'MP': 'Minutes Played',
        'FG': 'Field Goals',
        'FGA': 'Field Goals Attempts',
        '3P': '3-Point FG',
        '3PA': '3-Point FG Attempts',
        '2P': '2-Point FG',
        '2PA': '2-Point FG Attempts',
        'eFG%': 'Effective FG%',
        'FT%': 'Free Throw%',
        'FT': 'Free Throws',
        'FTA': 'Free Throws Attempts',
        'PTS': 'Points',
        'AST': 'Assists',
        'DRB': 'Defensive Rebounds',
        'ORB': 'Offensive Rebounds',
        'REB': 'Rebounds',
        'STL': 'Steals',
        'BLK': 'Blocks',
        'TOV': 'Turnovers',
        'PF': 'Personal Fouls'
    }, inplace=True)

    # Remplir les valeurs manquantes pour les données numériques avec la médiane
    for column in ['Age', 'FG%', '3P%', '2P%', 'Effective FG%', 'Free Throw%']:
        if column in df.columns:
            df[column] = df[column].fillna(df[column].median())

    # Remplir les valeurs manquantes pour les données catégoriques
    for column in ['Team', 'Position']:
        if column in df.columns:
            df[column] = df[column].fillna('Unknown')

    return df


def clean_conference_standings_data(df, conference_name):
    if df is None:
        return None

    # Renommer les colonnes pour assurer la cohérence
    df.rename(columns={
        'W': 'Wins',
        'L': 'Losses',
        'W/L%': 'Win/Loss Percentage',
        'GB': 'Games Behind',
        'PS/G': 'Points Scored per Game',
        'PA/G': 'Points Allowed per Game',
        'SRS': 'Simple Rating System'
    }, inplace=True)

    # Ajouter une nouvelle colonne pour le nom de la conférence
    df['Conference'] = conference_name

    # Remplir les données manquantes dans 'Win/Loss Percentage' avec 0.0
    if 'Win/Loss Percentage' in df.columns:
        df['Win/Loss Percentage'] = df['Win/Loss Percentage'].fillna(0.0)

    return df
