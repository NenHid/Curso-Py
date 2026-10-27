"""
demo_00_apis_publicas.py
------------------------
Demostración de APIs REST públicas gratuitas (Sin registro ni clave).
Ideales para mostrar en clase consumo de APIs y automatización con datos en vivo.
"""

import requests

def demo_clima_alertas():
    """1. API de Clima con Open-Meteo (Sin API key)."""
    print("\n--- 1. API DE CLIMA (Open-Meteo) ---")
    url = "https://api.open-meteo.com/v1/forecast"
    # Coordenadas (por ejemplo: Buenos Aires)
    params = {
        "latitude": -34.6037,
        "longitude": -58.3816,
        "current_weather": "true"
    }
    
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()["current_weather"]
        temp = data["temperature"]
        viento = data["windspeed"]
        print(f"Temperatura actual: {temp}°C | Viento: {viento} km/h")
        
        # Regla de automatización didáctica
        if temp > 28:
            print(" Regla activada: Alerta por calor.")
        else:
            print(" Regla activada: Clima agradable.")
    else:
        print("Error al consultar clima:", res.status_code)

def demo_finanzas_divisas():
    """2. API de Divisas con Frankfurter (Sin API key)."""
    print("\n--- 2. API FINANCIERA DE DIVISAS (Frankfurter) ---")
    url = "https://api.frankfurter.app/latest"
    params = {"amount": 100, "from": "USD", "to": "EUR"}
    
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        print(f"100 USD equivalen a: {data['rates']['EUR']} EUR (Fecha: {data['date']})")
    else:
        print("Error al consultar divisas:", res.status_code)

def demo_github_releases():
    """3. API de GitHub para monitoreo de software (Sin token para consultas públicas)."""
    print("\n--- 3. API DE GITHUB (Monitoreo de proyectos) ---")
    url = "https://api.github.com/repos/pallets/flask/releases/latest"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CursoPythonDemo/1.0"
    }
    res = requests.get(url, headers=headers, timeout=10)
    if res.status_code == 200:
        rel = res.json()
        print(f"Proyecto monitoreado: pallets/flask")
        print(f"Última versión oficial: {rel['tag_name']}")
        print(f"Fecha de publicación: {rel['published_at'][:10]}")
        print(f"Notas: {rel.get('name', 'Sin título')}")
    else:
        print("Error al consultar GitHub:", res.status_code)

if __name__ == "__main__":
    print("=== CONSUMO DE APIS PÚBLICAS EN PYTHON ===")
    demo_clima_alertas()
    demo_finanzas_divisas()
    demo_github_releases()
