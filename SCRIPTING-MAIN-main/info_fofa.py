from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración de WebDriver con User-Agent personalizado
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# Descomenta la siguiente línea para ver la ventana del navegador
# options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    # 1. Abrir FOFA
    driver.get("https://fofa.info/result?qbase64=Y2wua2dobS5jb20%3D")
    print("[+] Accediendo a FOFA...")
    time.sleep(3)  # Pausa para asegurar la carga completa de la página

    # 2. Iniciar sesión
    try:
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        print("[+] Campo de email encontrado. Iniciando sesión...")
        email_input.clear()
        email_input.send_keys("pabloalvarezaraya4@dominio.com")

        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.clear()
        password_input.send_keys("!@SwYGV2AzwWHhm")
        password_input.send_keys(Keys.RETURN)

        # Esperar a que se muestre algún elemento que confirme el inicio de sesión.
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info"))
        )
        print("[+] Inicio de sesión exitoso.")
    except Exception as login_error:
        print("[!] No se encontró el campo de email o ya estás logueado:", login_error)

    # Agrega un retraso adicional para evitar que el sitio interprete la actividad como de un bot
    time.sleep(5)

    # 3. Realizar la búsqueda o continuar con otras interacciones
    # ...

except Exception as e:
    print("[-] Se produjo un error:", e)
finally:
    driver.quit()
