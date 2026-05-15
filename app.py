import os
import sys
import requests
from requests.exceptions import Timeout, ConnectionError, RequestException

API_KEY = os.getenv("SPORTSDB_API_KEY")
LEAGUE_ID = os.getenv("LEAGUE_ID")
LEAGUE_NAME = os.getenv("LEAGUE_NAME", "Liga desconocida")
SEASON = os.getenv("SEASON", "2023-2024")
TOP_LIMIT = int(os.getenv("TOP_LIMIT", "5"))

if not API_KEY:
    print("ERROR CONFIG: falta variable de entorno SPORTSDB_API_KEY")
    sys.exit(1)

if not LEAGUE_ID:
    print("ERROR CONFIG: falta variable de entorno LEAGUE_ID")
    sys.exit(1)

URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/lookuptable.php"


def get_league_table():
    params = {
        "l": LEAGUE_ID,
        "s": SEASON
    }

    response = requests.get(URL, params=params, timeout=8)

    if response.status_code == 401:
        print("ERROR 401: API key inválida o no autorizada")
        sys.exit(1)

    if response.status_code == 403:
        print("ERROR 403: acceso prohibido a la API")
        sys.exit(1)

    if response.status_code == 404:
        print("ERROR 404: recurso no encontrado")
        sys.exit(1)

    if response.status_code >= 500:
        print(f"ERROR {response.status_code}: error del servidor de la API")
        sys.exit(1)

    data = response.json()

    if not data:
        print("ERROR DATA: la API no devolvió datos")
        sys.exit(1)

    if "table" not in data:
        print("ERROR DATA: la respuesta no contiene el campo 'table'")
        sys.exit(1)

    if not data["table"]:
        print(f"ERROR DATA: no hay tabla disponible para {LEAGUE_NAME} temporada {SEASON}")
        sys.exit(1)

    return data["table"]


def print_results(table):
    champion = table[0]

    print("========================================")
    print(" PREMIER LEAGUE & TOP LEAGUES TRACKER")
    print("========================================")
    print(f"Liga consultada : {LEAGUE_NAME}")
    print(f"Temporada       : {SEASON}")
    print("----------------------------------------")
    print("Campeón / Líder de la temporada:")
    print(f"Equipo          : {champion.get('strTeam', 'N/A')}")
    print(f"Puntos          : {champion.get('intPoints', 'N/A')}")
    print(f"Partidos jugados: {champion.get('intPlayed', 'N/A')}")
    print(f"Victorias       : {champion.get('intWin', 'N/A')}")
    print("----------------------------------------")
    print(f"Top {TOP_LIMIT} de la tabla:")
    print("----------------------------------------")

    for team in table[:TOP_LIMIT]:
        rank = team.get("intRank", "N/A")
        name = team.get("strTeam", "N/A")
        played = team.get("intPlayed", "N/A")
        wins = team.get("intWin", "N/A")
        draws = team.get("intDraw", "N/A")
        losses = team.get("intLoss", "N/A")
        points = team.get("intPoints", "N/A")

        print(f"{rank}. {name} | PJ: {played} | G: {wins} | E: {draws} | P: {losses} | Pts: {points}")

    print("----------------------------------------")
    print("Consulta finalizada correctamente.")


def main():
    try:
        table = get_league_table()
        print_results(table)
        sys.exit(0)

    except Timeout:
        print("ERROR TIMEOUT: la API tardó demasiado en responder")
        sys.exit(1)

    except ConnectionError:
        print("ERROR CONEXION: no se pudo conectar con la API")
        sys.exit(1)

    except ValueError:
        print("ERROR JSON: la API no devolvió un JSON válido")
        sys.exit(1)

    except RequestException as e:
        print(f"ERROR REQUEST: problema en la solicitud HTTP: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
