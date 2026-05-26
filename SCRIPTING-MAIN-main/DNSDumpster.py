import requests
import csv

API_KEY = "fedf5520faefa927c830e112237f6fdc895148d9f028d27d361d0822470d0f30"
DOMAIN = "cl.kghm.com"

# URL de la API
url = f"https://api.dnsdumpster.com/domain/{DOMAIN}"

# Encabezados con la API Key
headers = {"X-API-Key": API_KEY}

# Hacer la petición GET
response = requests.get(url, headers=headers)

# Verificar si la respuesta es válida
if response.status_code == 200:
    data = response.json()

    # Nombre del archivo CSV
    filename = f"subdominios_{DOMAIN}.csv"

    # Abrir archivo CSV en modo escritura
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Subdominio", "IP", "ASN Name"])  # Encabezados

        # Extraer subdominios, IPs y ASN Name
        for entry in data.get("a", []):
            subdomain = entry.get("host", "N/A")
            for ip_info in entry.get("ips", []):
                ip = ip_info.get("ip", "Sin IP")
                asn_name = ip_info.get("asn_name", "Sin ASN")
                writer.writerow([subdomain, ip, asn_name])
                print(f"{subdomain} - {ip} - {asn_name}")

    print(f"\n📁 Archivo guardado: {filename}")

else:
    print(f"❌ Error: {response.status_code} - {response.text}")
