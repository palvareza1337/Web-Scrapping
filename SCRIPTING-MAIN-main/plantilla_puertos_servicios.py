from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, color):
    """
    Aplica un color de fondo (en hexadecimal, sin el símbolo #) a la celda.
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    tcPr.append(shd)

# Crear el documento
doc = Document()

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
for paragraph in table_evidencia.rows[1].cells[0].paragraphs:
    for run in paragraph.runs:
        run.font.size = tamano
        run.font.name = fuente

# Guardar el documento resultante
doc.save("puertos_servicios_generado.docx")
print("Documento generado: puertos_servicios_generado.docx")
