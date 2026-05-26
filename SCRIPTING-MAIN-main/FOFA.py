import requests
import json

# Configura tu clave API
api_key = 'c31a6dd4f9a60996e60bc38b6a80ef97'  # Sustituye con tu clave API
base_url = 'https://fofa.info/api/v1/search/all'  # URL correcta

# Función para hacer la consulta a la API
def consulta_fofa(query, size=10):
    headers = {
        'Authorization': f'Bearer {api_key}'  # Usa tu clave API aquí
    }
    
    # Parámetros de búsqueda
    params = {
        'q': query,  # Consulta que quieres hacer
        'size': size  # Número de resultados que quieres obtener
    }
    
    try:
        # Hacer la solicitud GET a la API
        response = requests.get(base_url, headers=headers, params=params)
        
        # Verificar si la respuesta fue exitosa (200 OK)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                return data
            else:
                print("No se encontraron resultados. Revisa tu consulta.")
                return None
        else:
            print(f"Error: {response.status_code} - {response.text}")  # Mostramos el error detallado
            return None
    
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        return None

# Función principal
def main():
    # Pedir al usuario un dominio o IP
    sitio = input("Introduce el dominio o IP que deseas buscar en FOFA: ")
    
    # Asegurémonos de que la consulta esté correctamente formulada
    query = f'host="{sitio}"'  # Construimos la consulta para buscar ese sitio
    print(f"Realizando consulta con: {query}")  # Mostramos la consulta para depurar
    
    # Realiza la consulta a FOFA con el dominio o IP proporcionado
    resultados = consulta_fofa(query, size=5)
    
    # Mostrar los resultados
    if resultados:
        if 'results' in resultados:
            if len(resultados['results']) > 0:
                print(f"\nResultados para '{sitio}':\n")
                for i, resultado in enumerate(resultados['results'], start=1):
                    print(f"Resultado {i}:")
                    print(json.dumps(resultado, indent=2))  # Muestra los resultados en formato JSON bonito
            else:
                print(f"No se encontraron resultados para el sitio: {sitio}")
        else:
            print("No se obtuvieron resultados en el formato esperado.")
    else:
        print("Hubo un error o no se encontraron resultados.")

if __name__ == '__main__':
    main()
