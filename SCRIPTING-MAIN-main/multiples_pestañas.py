from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Lista de URLs actualizadas
urls = [
    "https://lyncdiscover.cl.kghm.com",
    "https://meet.cl.kghm.com",
    "https://sdsip.cl.kghm.com",
    "https://sip.cl.kghm.com",
    "https://frvpn.cl.kghm.com",
    "https://autodiscover.cl.kghm.com",
    "https://scvpn.cl.kghm.com",
    "https://ucrania.sgscm.cl",
    "https://exponor.sgscm.cl",
    "https://app.sgscm.cl",
    "https://sistemas.sgscm.cl",
    "https://academia.sgscm.cl",
    "https://vpnsgsecundaria.sgscm.cl",
    "https://vpnmina.sgscm.cl",
    "https://catabela.sgscm.cl",
    "https://vcse.sgscm.cl",
    "https://vpnsg.sgscm.cl",
    "https://sdsip.sgscm.cl",
    "https://vpn.sgscm.cl",
    "https://ftp.sgscm.cl",
    "https://induccionvisitas.sgscm.cl",
    "https://mail1.sgscm.cl",
    "https://meet.sgscm.cl",
    "https://mx.sgscm.cl",
    "https://mx1.sgscm.cl",
    "https://sconnector.sgscm.cl",
    "https://sip.sgscm.cl",
    "https://sisense.sgscm.cl",
    "https://lyncdiscover.sgscm.cl",
    "https://lyncws.sgscm.cl",
    "https://autodiscover.sgscm.cl",
    "https://mail.sgscm.cl",
    "https://pivision.sgscm.cl",
    "https://sisensebi.sgscm.cl",
    "https://www.sgscm.cl"
]





def open_tabs(urls):
    # Configuración del WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()  # Maximizar la ventana para ver todas las pestañas

    # Abrir cada URL en una nueva pestaña
    for url in urls:
        driver.execute_script(f"window.open('{url}', '_blank');")
    print("Todas las pestañas han sido abiertas.")

    # Mantener el navegador abierto
    try:
        print("Presiona Ctrl+C para cerrar el navegador.")
        while True:
            time.sleep(1)  # Mantener el script en ejecución
    except KeyboardInterrupt:
        print("Cerrando el navegador...")
        driver.quit()

# Ejecutar el script
if __name__ == "__main__":
    open_tabs(urls)
