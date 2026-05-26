import webbrowser

def abrir_pestanas(lista_ips):
    url_base = "https://www.shodan.io/host/"
    
    # Abrir una pestaña por cada dirección IP en la lista
    for ip in lista_ips:
        url_completa = url_base + ip.strip()
        webbrowser.open_new_tab(url_completa)

def main():
    # Ingresar listado de direcciones IP (puedes reemplazar esto por una lectura desde un archivo si lo prefieres)
    input_ips = """104.21.34.5
172.67.194.170
172.67.194.170
104.21.34.5
159.60.129.196
159.60.129.196
104.26.10.60
104.26.11.60
172.67.74.96
104.26.10.60
104.26.11.60
172.67.74.96
104.26.10.60
104.26.11.60
172.67.74.96
104.26.10.212
172.67.68.213
104.26.11.212
104.26.10.60
104.26.11.60
172.67.74.96
104.26.10.60
104.26.11.60
172.67.74.96
104.26.10.60
104.26.11.60
172.67.74.96
104.26.10.60
104.26.11.60
172.67.74.96
52.112.65.27
104.26.10.60
104.26.11.60
172.67.74.96
104.21.34.5
172.67.194.170
104.21.34.5
172.67.194.170
200.73.28.8
159.60.129.196
"""

    # Convertir el input a una lista de direcciones IP
    lista_ips = input_ips.splitlines()

    # Llamar a la función para abrir las pestañas
    abrir_pestanas(lista_ips)

if __name__ == "__main__":
    main()
