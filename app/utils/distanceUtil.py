import requests
from app.config import TOKEN_API_MAP
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float]:
  origen = (lat1, lon1)
  destino = (lat2, lon2)
  coords = f"{origen[1]},{origen[0]};{destino[1]},{destino[0]}"
  url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={TOKEN_API_MAP}&start={coords.split(';')[0]}&end={coords.split(';')[1]}"
  response = requests.get(url).json()
  distancia_ruta = response["features"][0]["properties"]["summary"]["distance"] / 1000  # km
  duracion = response["features"][0]["properties"]["summary"]["duration"] / 60 # min
  return distancia_ruta, duracion
  