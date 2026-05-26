from censys.search import CensysHosts
import getpass

# Solicitar credenciales de la API
UID = input("Ingrese su API UID de Censys: ")
SECRET = getpass.getpass("Ingrese su API SECRET de Censys: ")

# Crear cliente de Censys
censys_client = CensysHosts(api_id=UID, api_secret=SECRET)

# Solicitar dominio al usuario
domain = input("Ingrese el dominio a buscar: ")

# Consultar la API de Censys
try:
    results = censys_client.search(domain, per_page=5)  # Limita la búsqueda a 5 resultados

    print("\n🔍 Resultados encontrados:")
    for result in results:
        ip = result.get("ip", "No disponible")
        subdomains = result.get("dns.names", ["No disponible"])
        print(f"\n➡ IP: {ip}")
        print(f"📌 Subdominios: {', '.join(subdomains)}")

except Exception as e:
    print(f"❌ Error al consultar Censys: {e}")
