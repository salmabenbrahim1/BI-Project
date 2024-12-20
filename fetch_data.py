# fetch_data.py
import requests
def fetch_nba_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("La page a été récupérée avec succès")
        return response.content
    else:
        print("Échec de la récupération de la page")
        return None
