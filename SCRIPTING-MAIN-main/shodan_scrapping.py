import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re  # Importar el módulo re para expresiones regulares
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import ipaddress
from docx.shared import RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def is_ip_in_cloduflare(ip: str) -> bool:
    clodflareSubnet= ["173.245.48.0/20",
                    "103.21.244.0/22",
                    "103.22.200.0/22",
                    "103.31.4.0/22",
                    "141.101.64.0/18",
                    "108.162.192.0/18",
                    "190.93.240.0/20",
                    "188.114.96.0/20",
                    "197.234.240.0/22",
                    "198.41.128.0/17",
                    "162.158.0.0/15",
                    "104.16.0.0/13",
                    "104.24.0.0/14",
                    "172.64.0.0/13",
                    "131.0.72.0/22"]
    for subnet in clodflareSubnet:
        try:
            ip_obj = ipaddress.ip_address(ip)
            subnet_obj = ipaddress.ip_network(subnet, strict=False)
            if ip_obj in subnet_obj:
                return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
    return False

# Función para cambiar el color de fondo de la celda
def set_cell_background(cell, color):
    cell_properties = cell._element.get_or_add_tcPr()
    shade = OxmlElement('w:shd')
    shade.set(qn('w:fill'), color)
    cell_properties.append(shade)

# Función para establecer la fuente y el tamaño del texto
def set_cell_font(cell, font_name='Calibri', font_size=9, bold=False, color=RGBColor(0, 0, 0), align='center'):
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.color.rgb = color
        if align:
            paragraph.alignment = 1  # 1: Center, 0: Left, 2: Right

# Obtener direcciones IP del DataFrame
def get_ips(df):
    ip_addresses = set()
    for x in df['IP']:
        if len(x) == 0:
            continue
        for y in x.split('\n'):
            ip_addresses.add(y)
    return ip_addresses

# Función principal de scraping de Shodan
def sh_scrapping(ip_list):
    http_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    allports = []
    allcve = {}

    for ip_address in ip_list:
        if (is_ip_in_cloduflare(ip_address)):
            print('Cloudflare IP Found')
            continue
        
        url = f"https://www.shodan.io/host/{ip_address}"
        time.sleep(15)
        response = requests.get(url, headers=http_headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            x = re.search(r"const VULNS .*;\n", response.text)
            if x:
                to_json = x.group(0).replace("const VULNS = ", "")[:-2]
                parsed_json = json.loads(to_json)
                allcve[ip_address] = parsed_json.keys()
            
            ports_section = soup.find('div', id="ports")
            if ports_section:
                ports = ports_section.find_all('a', class_="bg-primary")
                seen_ports = set()
                for port in ports:
                    port_number = port.text.strip()
                    if port_number in seen_ports:
                        continue
                    seen_ports.add(port_number)
                    observation = ''
                    protocol_info = port_number.replace('\n', ' / ').replace(' / / ', ' / ')
                    
                    port_detail_heading = soup.find('h6', id=port_number)
                    if port_detail_heading:
                        span = port_detail_heading.find_next('span')
                        if span:
                            protocol_info = span.text.strip().replace('\n', ' / ').replace(' / / ', ' / ')
                        
                        # Buscar el div con clase "card card-padding banner"
                        banner_div = port_detail_heading.find_next('div', class_="card card-padding banner")
                        if banner_div:
                            banner_title = banner_div.find('h1', class_="banner-title")
                            http_title_div = banner_div.find('div', class_="http-title")
                            
                            if banner_title:
                                observation = banner_title.text.strip()
                            
                            if http_title_div:
                                observation = http_title_div.text.strip()
                            
                            if not observation:
                                pre = banner_div.find_next('pre')
                                if pre:
                                    observation = pre.text.strip().split('\n')[0]
                        
                    print(f"IP: {ip_address}, Port: {port_number}, Observation: {observation}")  # Agregar impresión de depuración
                    allports.append([ip_address, protocol_info, observation])
        else:
            print(f"Error al cargar la web para la IP {ip_address}, Código: {response.status_code}")
            if response.status_code == 403:
                print("Acceso prohibido. Es posible que necesite autenticarse o que su IP esté bloqueada.")

    # Generar el archivo shodan_ports_table.docx
    # generate_ports_report(allports)
    
    return pd.DataFrame(allports, columns=['IP', 'PROTOCOL INFO', 'OBSERVACIÓN']), allcve


def super_Tabla2(data, doc):
    # Configuración de fuente y tamaño
    fuente = "Calibri (Cuerpo)"
    tamano = Pt(9)

    # ===============================================================
    # TABLA ÚNICA: CABECERA + DESCRIPCIÓN / IMPACTO (9 filas, 2 columnas)
    # ===============================================================
    # Fila 0: Fila vacía con fondo #0070C0, fusionada en una sola celda
    # Filas 1 a 6: Cabecera (NOMBRE, SEVERIDAD, CVSS BASE, CVE, ACCESO, RIESGO) con fondo gris claro (D9D9D9)
    # Fila 7: Encabezados "DESCRIPCIÓN" e "IMPACTO" con fondo gris (666666) y letra blanca
    # Fila 8: Contenidos de DESCRIPCIÓN e IMPACTO
    table = doc.add_table(rows=9, cols=2)
    table.style = 'Table Grid'

    # --- Fila 0: Vacía con fondo #0070C0 en ambas celdas, fusionadas en una sola celda ---
    merged_cell = table.rows[0].cells[0].merge(table.rows[0].cells[1])
    merged_cell.text = ""
    set_cell_background(merged_cell, "0070C0")

    # --- Datos de cabecera para las filas 1 a 6 ---
    header_data = [
        ("NOMBRE", "Escaneo por IP’s asociadas a servicios expuestos"),
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
    run_normal = p_desc.add_run("Dentro de los activos analizados se observan puertos y \n"
                                "servicios con las siguientes IP’s asociadas, las IP’s no \n"
                                "apuntadas en el siguiente reporte quiere decir que no fue posible detectar mayores detalles."
                                )
    run_normal.font.size = tamano
    run_normal.font.name = fuente


    # Celda IMPACTO (texto normal)
    cell_impact = table.rows[8].cells[1]
    cell_impact.text = (
        "La exposición de puertos y servicios en los dominios de  \n"
        "<DOMINIO> puede aumentar el riesgo de ataques cibernéticos,  \n"
        "comprometer la seguridad de la información, causar  \n"
        "interrupciones en los servicios y afectar negativamente la reputación de la  \n"
        "empresa. Esto podría resultar en pérdidas \n"
        "financieras significativas debido a costos de mitigación y \n"
        "posibles multas regulatorias."
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
        "Para reducir el riesgo de exposición de estos servicios, se recomienda: \n"
        "•	Revisar y limitar la exposición de puertos y servicios no esenciales. \n"
        "•	Implementar reglas de firewall adecuadas para restringir el acceso no autorizado. \n"
        "•	Asegurarse de que todos los servicios y certificados SSL estén actualizados y configurados correctamente. \n"
        "•	Realizar auditorías regulares de seguridad y escaneos de vulnerabilidad para identificar y corregir posibles \n" 
        "   fallos de seguridad."
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
    table_evidencia.rows[1].cells[0].text = "A continuación, se identificaron los siguientes servicios y puertos disponibles:"
    
    generate_ports_report(data, table_evidencia.rows[1].cells[0])
    table_evidencia.rows[1].cells[0].add_paragraph()

    for paragraph in table_evidencia.rows[1].cells[0].paragraphs:
        for run in paragraph.runs:
            run.font.size = tamano
            run.font.name = fuente

    doc.add_paragraph()

    

# Función para generar el reporte de puertos en un archivo .docx
def generate_ports_report(data, doc):
    
    # Agrupar los datos por IP
    grouped_data = {}
    for item in data.values.tolist():
        ip_address, protocol_info, observation = item
        if len(observation)>300:
            observation = observation[:300]
            temp = list(observation)
            temp.insert(49,'\n')
            temp.insert(99,'\n')
            temp.insert(149,'\n')
            temp.insert(199,'\n')
            temp.insert(249,'\n')
            temp.append('...')
            observation = ''.join(temp)

        if ip_address not in grouped_data:
            grouped_data[ip_address] = []
        grouped_data[ip_address].append((protocol_info, observation))
    
    # Procesar cada dirección IP y crear una tabla por IP
    for ip_address, ports in grouped_data.items():
        
        # Añadir un párrafo vacío para separar las tablas
        doc.add_paragraph()

        # Añadir la tabla sin filas iniciales
        table = doc.add_table(rows=0, cols=3)
        
        # Agregar la fila de la IP
        ip_row = table.add_row().cells
        ip_cell = ip_row[0]
        ip_cell.text = f'IP / HOST: {ip_address}'
        ip_cell.merge(ip_row[1])
        ip_cell.merge(ip_row[2])
        set_cell_font(ip_cell, bold=True, align='center')
        set_cell_background(ip_cell, 'D9D9D9')  # color: (blanco, Fondo 1, Oscuro 15%)
        
        # Añadir la fila de encabezados de la tabla
        hdr_cells = table.add_row().cells
        table_headers = ['IP / Host', 'Puerto', 'Observación']
        for i, column in enumerate(table_headers):
            hdr_cells[i].text = column
            set_cell_font(hdr_cells[i], bold=True)  # Texto en negrita para la cabecera
            set_cell_background(hdr_cells[i], 'D9D9D9')  # color: (blanco, Fondo 1, Oscuro 15%)
        
        # Añadir los datos de los puertos a la tabla para la IP actual
        for protocol_info, observation in ports:
            row_cells = table.add_row().cells
            row_cells[0].text = str(ip_address)
            row_cells[1].text = str(protocol_info)
            row_cells[2].text = str(observation)
            for cell in row_cells:
                set_cell_font(cell)  # Establecer fuente y tamaño para celdas

        # Agregar bordes a la tabla
        for row in table.rows:
            for cell in row.cells:
                tc_pr = cell._element.get_or_add_tcPr()
                tc_borders = OxmlElement('w:tcBorders')
                for border_name in ["top", "left", "bottom", "right"]:
                    border = OxmlElement(f'w:{border_name}')
                    border.set(qn('w:val'), 'single')
                    border.set(qn('w:sz'), '4')
                    border.set(qn('w:space'), '0')
                    border.set(qn('w:color'), '000000')
                    tc_borders.append(border)
                tc_pr.append(tc_borders)
    
    # Guardar el documento
    # doc.save('shodan_ports_table.docx')

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
    fuentes_text = "- Virustotal, Google, Bing, DuckDuckGo, Shodan, Cencys, Zoomeye."
    fuentes_table.cell(1, 0).text = fuentes_text

# Ejemplo de uso
if __name__ == "__main__":
    # Para pruebas, usa esta lista de IPs
    ip_list = ['8.8.8.8', '1.1.1.1']
    _, _ = sh_scrapping(ip_list)

