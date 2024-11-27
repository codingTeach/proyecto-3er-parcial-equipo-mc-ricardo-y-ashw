import requests
import pandas as pd

def fetch_popular_games():
    steamspy_url = "https://steamspy.com/api.php"
    params = {"request": "all"}  # Puedes probar con otros parámetros como 'top200in2weeks'
    
    try:
        # Obtener datos de SteamSpy
        response = requests.get(steamspy_url, params=params)

        response.raise_for_status()  # Lanzar excepción si hay errores HTTP
        games_data = response.json()
        
        # Transformar los datos en una tabla
        games = []
        for appid, details in games_data.items():
            games.append({
                "AppID": appid,
                "Nombre": details.get("name", "N/A"),
                "Desarrollador": details.get("developer", "N/A"),
                "Editor": details.get("publisher", "N/A"),
                "Propietarios": details.get("owners", "N/A"),
                "Número de Reviews": details.get("positive", 0) + details.get("negative", 0),
                "Porcentaje Positivo": details.get("positive", 0) / max(1, (details.get("positive", 0) + details.get("negative", 0))) * 100,
                "Precio (aprox)": float(details.get("price", 0)) / 100.0  # Convertir a flotante y manejar ausencia
            })

        # Crear DataFrame
        df = pd.DataFrame(games)
        return df
    
    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return pd.DataFrame()

# Guardar los datos en un archivo CSV
if __name__ == "__main__":
    popular_games_df = fetch_popular_games()
    if not popular_games_df.empty:
        print(popular_games_df.head())  # Muestra las primeras filas
        popular_games_df.to_csv("steam_top_games.csv", index=False)  # Guardar en CSV
        print("Datos guardados en steam_top_games.csv")
    else:
        print("No se pudo obtener datos.")
