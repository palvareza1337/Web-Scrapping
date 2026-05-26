from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time

def ssl_test(domain):
    # Configurar ChromeDriver
    options = Options()
    options.headless = True  # Ejecutar Chrome en modo headless (sin interfaz gráfica)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Ajustar el tamaño de la ventana del navegador al tamaño máximo de la pantalla
    driver.maximize_window()

    # Generar la URL dinámicamente con el dominio proporcionado
    url = f'https://www.ssllabs.com/ssltest/analyze.html?d={domain}'
    driver.get(url)

    # Esperar explícitamente a que el elemento esté presente
    wait = WebDriverWait(driver, 120)  # Aumenta el tiempo de espera a 120 segundos
    element = None

    for i in range(10):  # Intentar hasta 10 veces para obtener el elemento
        try:
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'reportSection')))
            break  # Si se encuentra el elemento, salir del bucle
        except StaleElementReferenceException:
            print(f"Elemento no disponible en el intento {i + 1}. Reintentando...")
            time.sleep(10)  # Esperar un poco antes de reintentar
        except Exception as e:
            print(f"Error encontrado: {e}")
            time.sleep(10)  # Esperar un poco antes de reintentar

    if element is None:
        print("No se pudo encontrar el elemento 'reportSection' después de varios intentos.")
    else:
        # Asegurarse de que el elemento esté completamente cargado antes de proceder
        for i in range(10):
            try:
                element = driver.find_element(By.CLASS_NAME, 'reportSection')
                break
            except StaleElementReferenceException:
                print(f"Elemento obsoleto en el intento {i + 1}. Reintentando...")
                time.sleep(5)  # Esperar antes de reintentar
            except Exception as e:
                print(f"Error encontrado: {e}")
                time.sleep(5)

        # Esperar un tiempo adicional para asegurarse de que todo el contenido esté completamente cargado
        time.sleep(10)

        # Obtener la posición y tamaño del elemento
        location = element.location
        size = element.size

        # Tomar una captura de pantalla de toda la página
        driver.save_screenshot('full_screenshot.png')

        # Cargar la captura de pantalla en Pillow
        full_screenshot = Image.open('full_screenshot.png')

        # Aumentar el área de recorte para evitar cortar partes del elemento
        padding = 10  # Puedes ajustar este valor según sea necesario

        # Definir el área para recortar
        left = location['x'] - padding
        top = location['y'] - padding
        right = location['x'] + size['width'] + padding
        bottom = location['y'] + size['height'] + padding

        # Recortar la captura de pantalla
        cropped_screenshot = full_screenshot.crop((left, top, right, bottom))

        # Guardar la imagen recortada
        cropped_screenshot.save(f'{domain}_cropped_screenshot.png')

        print(f"Captura de pantalla guardada como '{domain}_cropped_screenshot.png'")

    # Cerrar el navegador
    driver.quit()
