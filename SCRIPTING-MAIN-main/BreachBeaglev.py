import os
import requests
import re
import time

def limpiar_html(texto):
    """Elimina etiquetas HTML de un texto."""
    return re.sub(r'<.*?>', '', texto)

def get_breach_details(breach_name, api_key):
    url = f"https://haveibeenpwned.com/api/v3/breach/{breach_name}"
    headers = {
        'hibp-api-key': api_key,
        'User-Agent': 'BreachBeagle Script'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def check_email_breach(email, api_key, breaches_dict, seen_breaches):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        'hibp-api-key': api_key,
        'User-Agent': 'BreachBeagle Script'
    }
    retries = 3
    for attempt in range(retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            breaches = response.json()
            breaches_dict[email] = []
            
            for breach in breaches:
                breach_name = breach.get('Name', 'No especificado')

                if breach_name not in seen_breaches:
                    detailed_breach = get_breach_details(breach_name, api_key)
                    if detailed_breach:
                        seen_breaches[breach_name] = {
                            'Nombre': breach_name,
                            'Fecha': detailed_breach.get('BreachDate', 'Fecha no disponible'),
                            'Descripción': limpiar_html(detailed_breach.get('Description', 'Descripción no disponible')),
                            'Datos comprometidos': ', '.join(detailed_breach.get('DataClasses', ['Datos no disponibles']))
                        }

                if breach_name in seen_breaches:
                    breaches_dict[email].append(breach_name)
            return
        elif response.status_code == 404:
            return  # No hay brechas para este correo
        elif response.status_code == 429:
            time.sleep(30)  # Espera antes de reintentar
        else:
            breaches_dict[email] = f"[ERROR] Status Code: {response.status_code} - {response.text}"
            return

def check_emails_from_file(file_path, api_key):
    breaches_dict = {}
    seen_breaches = {}  # Guardará detalles de filtraciones únicas

    try:
        with open(file_path, 'r') as file:
            emails = [line.strip() for line in file if line.strip()]
            for email in emails:
                check_email_breach(email, api_key, breaches_dict, seen_breaches)
                time.sleep(5)  # Espera 5 segundos entre cada solicitud

        output_path = "reporte_brechas.txt"
        with open(output_path, 'w') as output_file:
            # Mapeo de filtraciones a números únicos
            breach_number_map = {breach: i + 1 for i, breach in enumerate(seen_breaches.keys())}

            # Primera sección: lista de correos con números correctos
            output_file.write("### Correos afectados:\n\n")
            for email, breaches in breaches_dict.items():
                if isinstance(breaches, list) and breaches:
                    numbers = [str(breach_number_map[breach]) for breach in breaches]
                    output_file.write(f"{email} [{', '.join(numbers)}]\n")

            # Segunda sección: descripción de filtraciones únicas
            output_file.write("\n### Detalle de filtraciones:\n\n")
            for breach, number in breach_number_map.items():
                details = seen_breaches[breach]
                output_file.write(f"{number}. {details['Nombre']} ({details['Fecha']}):\n")
                output_file.write(f"{details['Descripción']}\n")
                output_file.write(f"Datos comprometidos: {details['Datos comprometidos']}\n\n")

        print(f"[OK] Reporte generado exitosamente en: {output_path}")
    except FileNotFoundError:
        print(f"[ERROR] El archivo '{file_path}' no fue encontrado.")

# Ejemplo de uso
api_key = "989eac5873a34ad2b55eb788a4d0e655"
file_path = "SCRIPTING-MAIN-main/correos.txt"
check_emails_from_file(file_path, api_key)