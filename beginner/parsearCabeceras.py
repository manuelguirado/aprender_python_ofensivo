import requests
def parsearCabeceras(url):
    filtrar_cabceras = {"Status", "Content-Type", "Server", "Set-Cookie"}
    response = requests.get(url)
    cabceras = response.headers
    for clave, valor in cabceras.items():
        if clave in filtrar_cabceras:
            print(f"{clave}: {valor}")

if __name__ == "__main__":
    url = "https://pokeapi.co/api/v2/pokemon"
    parsearCabeceras(url)      