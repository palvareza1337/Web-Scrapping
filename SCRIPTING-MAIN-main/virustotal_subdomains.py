import requests
import dns.resolver
import pandas as pd
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import subprocess
import os
from docx.shared import RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def fetch_data(domain):

        # URL base de la API de VirusTotal para obtener subdominios
        url_base = f'https://www.virustotal.com/api/v3/domains/{domain}/subdomains'

        # Lista para almacenar los resultados
        results = []

        # Obtener la primera página de resultados
        data = get_subdomains(url_base)

        # Procesar todas las páginas
        while data:
            if 'data' in data:
                for item in data['data']:
                    subdomain = item.get('id', 'N/A')
                    ips = []
                    try:
                        answers = dns.resolver.resolve(subdomain, 'A')
                        ips = [str(ip) for ip in answers]
                    except dns.resolver.NXDOMAIN:
                        ips = []
                    except dns.resolver.NoAnswer:
                        ips = []
                    except dns.resolver.Timeout:
                        ips = ["La solicitud DNS agotó el tiempo"]
                    except Exception as e:
                        ips = [f"Error: {e}"]
                    
                    # Verificar accesibilidad
                    access = check_accessibility(subdomain)
                    
                    # Almacenar resultados
                    results.append([subdomain, '\n'.join(ips) if ips else '', access])
            else:
                print("No se encontraron subdominios.")

            # Verificar si hay más páginas de resultados
            next_link = data['links'].get('next')
            if next_link:
                data = get_subdomains(next_link)
            else:
                break
        
        return pd.DataFrame(results, columns=['Subdominio', 'IP', 'Accede http(s)'])

# Función para obtener subdominios con manejo de paginación
def get_subdomains(url):
    
    # Tu clave API de VirusTotal
    api_key = '063486c670095019fe40b6a93d69aeb3e189ab41707bfba038c0443889280014'

    headers = {
            'x-apikey': api_key
        }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error en la solicitud a la API: {response.status_code} - {response.text}")
        return None ,

# Función para verificar accesibilidad HTTP/HTTPS
def check_accessibility(subdomain):
    try:
        http_response = requests.get(f'http://{subdomain}', timeout=5)
        return http_response.status_code
        
    except requests.RequestException:
        pass

    try:
        https_response = requests.get(f'https://{subdomain}', timeout=5)
        return https_response.status_code
    
    except requests.RequestException:
        pass

    return 'No'


def set_cell_background(cell, color):
    """
    Aplica un color de fondo (en hexadecimal, sin el símbolo #) a la celda.
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    tcPr.append(shd)


def super_Tabla1(domain, df, doc):
    # Configuración de fuente y tamaño
    fuente = "Calibri (Cuerpo)"
    tamano = Pt(9)

    table = doc.add_table(rows=9, cols=2)
    table.style = 'Table Grid'

    # --- Fila 0: Vacía con fondo #0070C0 en ambas celdas, fusionadas en una sola celda ---
    merged_cell = table.rows[0].cells[0].merge(table.rows[0].cells[1])
    merged_cell.text = ""
    set_cell_background(merged_cell, "0070C0")

    # --- Datos de cabecera para las filas 1 a 6 ---
    header_data = [
        ("NOMBRE", "Análisis de subdominios"),
        ("SEVERIDAD", ""),
        ("CVSS BASE", ""),
        ("CVE", ""),
        ("ACCESO", ""),
        ("RIESGO", "")
    ]

    # Fondo para la primera columna de cabecera (Gris Claro, Fondo 2, Oscuro 50% → D9D9D9)
    header_bg = "D9D9D9"
    for i, (campo, valor) in enumerate(header_data, start=1):
        # Celda izquierda: texto en fuente Calibri (Cuerpo) 9 y fondo header_bg (sin negrita)
        cell_left = table.rows[i].cells[0]
        para_left = cell_left.paragraphs[0]
        run_left = para_left.add_run(campo)
        run_left.bold = False  # Se elimina la negrita
        run_left.font.size = tamano
        run_left.font.name = fuente
        set_cell_background(cell_left, header_bg)
        
        # Celda derecha: texto normal (si existe)
        cell_right = table.rows[i].cells[1]
        if valor:
            para_right = cell_right.paragraphs[0]
            run_right = para_right.add_run(valor)
            run_right.font.size = tamano
            run_right.font.name = fuente

    # --- Fila 7: Encabezados de DESCRIPCIÓN e IMPACTO ---
    # Se aplica fondo "666666" (gris) y color de letra blanco
    header_oscuro = "666666"

    # Encabezado DESCRIPCIÓN
    cell_desc_header = table.rows[7].cells[0]
    para_desc_header = cell_desc_header.paragraphs[0]
    run_desc_header = para_desc_header.add_run("DESCRIPCIÓN")
    run_desc_header.bold = True
    run_desc_header.font.size = tamano
    run_desc_header.font.name = fuente
    run_desc_header.font.color.rgb = RGBColor(255, 255, 255)
    set_cell_background(cell_desc_header, header_oscuro)

    # Encabezado IMPACTO
    cell_impact_header = table.rows[7].cells[1]
    para_impact_header = cell_impact_header.paragraphs[0]
    run_impact_header = para_impact_header.add_run("IMPACTO")
    run_impact_header.bold = True
    run_impact_header.font.size = tamano
    run_impact_header.font.name = fuente
    run_impact_header.font.color.rgb = RGBColor(255, 255, 255)
    set_cell_background(cell_impact_header, header_oscuro)

    # --- Fila 8: Contenidos de DESCRIPCIÓN e IMPACTO ---
    # En la celda de DESCRIPCIÓN se separa el texto en dos runs, para que
    # el fragmento "*  El certificado vence en 2 meses." se muestre en rojo.
    cell_desc = table.rows[8].cells[0]
    cell_desc.text = ""  # Limpiar contenido previo
    p_desc = cell_desc.paragraphs[0]
    # Primer segmento de texto (normal)
    run_normal = p_desc.add_run("Se analiza el listado de subdominios descubiertos. \n"
                                "Además, algunos de estos subdominios no cuentan con \n"
                                "direcciones IP activas.  Sin embargo, otros se \n"
                                "encuentran activos y pueden. ser accedidos desde \n"
                                "internet a través de http y/o https.\n\n"
                                "Los subdominios sin acceso podrían corresponden a\n"
                                "subdominios publicados a nivel interno, es decir, \n"
                                "accesibles desde una red local."
                                )
    run_normal.font.size = tamano
    run_normal.font.name = fuente


    # Celda IMPACTO (texto normal)
    cell_impact = table.rows[8].cells[1]
    cell_impact.text = (
        "Un subdominio no identificado por la organización \n" 
        "puede contener versions de software desactualizadas o \n" 
        "con vulnerabilidades. Así como instalaciones por \n"
        "defecto."
    )
    for paragraph in cell_impact.paragraphs:
        for run in paragraph.runs:
            run.font.size = tamano
            run.font.name = fuente

    # ===============================================================
    # TABLA DE MITIGACIÓN (2 filas, 1 columna) - Colocada justo debajo
    # ===============================================================
    table_mitigacion = doc.add_table(rows=2, cols=1)
    table_mitigacion.style = 'Table Grid'
    # Encabezado MITIGACIÓN con fondo "666666" y texto blanco
    cell_mitigacion_header = table_mitigacion.rows[0].cells[0]
    para_mitigacion_header = cell_mitigacion_header.paragraphs[0]
    run_mitigacion_header = para_mitigacion_header.add_run("MITIGACIÓN")
    run_mitigacion_header.bold = True
    run_mitigacion_header.font.size = tamano
    run_mitigacion_header.font.name = fuente
    run_mitigacion_header.font.color.rgb = RGBColor(255, 255, 255)
    set_cell_background(cell_mitigacion_header, header_oscuro)
    # Contenido de MITIGACIÓN
    mitigacion_text = (
        "Se recomienda revisar la lista de subdominios identificados y de evaluar dar de bajas los servicios que no estén \n"
        "siendo utilizados."
    )
    table_mitigacion.rows[1].cells[0].text = mitigacion_text
    for paragraph in table_mitigacion.rows[1].cells[0].paragraphs:
        for run in paragraph.runs:
            run.font.size = tamano
            run.font.name = fuente

    # ===============================================================
    # TABLA DE EVIDENCIA (2 filas, 1 columna) - Inmediatamente después
    # ===============================================================
    table_evidencia = doc.add_table(rows=2, cols=1)
    table_evidencia.style = 'Table Grid'
    # Encabezado EVIDENCIA con fondo "666666" y texto blanco
    cell_evidencia_header = table_evidencia.rows[0].cells[0]
    para_evidencia_header = cell_evidencia_header.paragraphs[0]
    run_evidencia_header = para_evidencia_header.add_run("EVIDENCIA")
    run_evidencia_header.bold = True
    run_evidencia_header.font.size = tamano
    run_evidencia_header.font.name = fuente
    run_evidencia_header.font.color.rgb = RGBColor(255, 255, 255)
    set_cell_background(cell_evidencia_header, header_oscuro)
    # Contenido de EVIDENCIA
    table_evidencia.rows[1].cells[0].text = "A continuación, se detalla los subdominios identificados:"
    
    create_doc(domain, df, table_evidencia.rows[1].cells[0])

    table_evidencia.rows[1].cells[0].add_paragraph()

    for paragraph in table_evidencia.rows[1].cells[0].paragraphs:
        for run in paragraph.runs:
            run.font.size = tamano
            run.font.name = fuente

    doc.add_paragraph()
# Crear un documento de Word
def create_doc(domain, df, doc):

   

    # Agregar título al documento
    # doc.add_heading(f'Subdominios y IPs para {domain}', level=1)

    # Agregar tabla al documento
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    # Aplicar estilo a la cabecera de la tabla
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Subdominio'
    hdr_cells[1].text = 'IP'
    hdr_cells[2].text = 'Accede http(s)'

    # Aplicar estilos a la cabecera
    for cell in hdr_cells:
        cell_paragraph = cell.paragraphs[0]
        cell_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell_font = cell_paragraph.runs[0].font
        cell_font.bold = True
        cell_font.color.rgb = RGBColor(0, 0, 0)  # Color del texto: Negro
        cell_font.size = Pt(9)

        # Establecer fondo de la celda
        cell_shading = OxmlElement('w:shd')
        cell_shading.set(qn('w:val'), 'clear')
        cell_shading.set(qn('w:color'), 'auto')
        cell_shading.set(qn('w:fill'), 'D9D9D9')  # Fondo: Blanco, Fondo 1, Oscuro 15%
        cell._element.get_or_add_tcPr().append(cell_shading)

    # Agregar datos a la tabla
    for index, row in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = row['Subdominio']
        row_cells[1].text = row['IP']
        row_cells[2].text = str(row['Accede http(s)'])

    # Guardar el documento de Word
    # output_filename = f'subdominios_{domain}.docx'
    # doc.save(output_filename)

    # print(f"Documento guardado como {output_filename}")

   # Agregar una nueva tabla con una sola columna
    fuentes_table = doc.add_table(rows=2, cols=1)
    fuentes_table.style = 'Table Grid'  # Aplicar estilo de tabla con bordes

    # Primera fila: "FUENTES" en negrita, centrado y con fondo gris #D9D9D9
    fuentes_cell = fuentes_table.cell(0, 0)
    fuentes_cell.text = "FUENTES"

    # Centrar el texto y poner en negrita
    fuentes_paragraph = fuentes_cell.paragraphs[0]
    fuentes_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    fuentes_paragraph.runs[0].bold = True

    # Aplicar fondo gris #D9D9D9 (RGB: 217, 217, 217)
    shading_elm = parse_xml(r'<w:shd {} w:fill="D9D9D9"/>'.format(nsdecls('w')))
    fuentes_cell._element.get_or_add_tcPr().append(shading_elm)

    # Segunda fila: Lista de fuentes con saltos de línea
    fuentes_text = "- Sublist3r\n- subfinder\n- Virustotal\n- Google, Bing, DuckDuckGo\n- dnsdumpster.com"
    fuentes_table.cell(1, 0).text = fuentes_text


if __name__ == "__main__":

    # Solicitar al usuario que ingrese el dominio principal
    domain = input("Ingresa el dominio principal: ")

    

    # Crear un DataFrame de pandas
    df = fetch_data(domain)

    create_doc(domain, df)