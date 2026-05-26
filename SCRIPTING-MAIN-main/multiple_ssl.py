import webbrowser
import time

# Recibir los dominios desde el input del usuario separados por espacios
dominios_input = input("Introduce los dominios separados por espacios: ")

# Dividir el input en una lista de dominios
dominios = dominios_input.split()

# URL base de SSL Labs
base_url = "https://www.ssllabs.com/ssltest/analyze.html?d="

# Abrir cada dominio en el navegador
for dominio in dominios:
    full_url = base_url + dominio
    print(f"Abriendo: {full_url}")
    webbrowser.open_new_tab(full_url)
    time.sleep(2)  # Pausa de 2 segundos entre cada ventana
