import os
import requests

# Ruta absoluta del archivo ips.txt
file_path = r"C:\Users\flipp\Downloads\SCRIPTING-MAIN-main\SCRIPTING-MAIN-main\ips.txt"

# Verificar si el archivo existe antes de abrirlo
if not os.path.exists(file_path):
    print(f"❌ Error: No se encontró el archivo en {file_path}")
    exit()

# Leer las IPs desde el archivo
with open(file_path, "r") as file:
    listado_ip = [line.strip() for line in file.readlines()]

url = "https://api.abuseipdb.com/api/v2/check"
api_key = "9df592de979ceee798dac428f7a437e7a3797c0189bf26d2195aa7673ec9919c625e0e9e81b22cbc"

for cada_ip in listado_ip:
    informacion = {
        "ipAddress": cada_ip,
        "maxAgeInDays": "90"
    }
    api = {
        "Key": api_key,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=api, params=informacion)

    if response.status_code == 200:
        respuesta = response.json()

        # Extraer la IP, total de reportes y el porcentaje de abuso
        ip = respuesta['data']['ipAddress']
        reportes = respuesta['data']['totalReports']
        confianza_abuso = respuesta['data']['abuseConfidenceScore']

        #print(f"Para la IP {ip}, tiene {reportes} reportes con un {confianza_abuso}% de confianza de abuso.")
        #print(f"{reportes}")
        print(f"{confianza_abuso}%")
    else:
        print(f"❌ Error al consultar la IP {cada_ip}: {response.status_code} - {response.text}")
