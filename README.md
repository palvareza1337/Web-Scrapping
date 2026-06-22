# Attack Surface Analyzer

Herramienta desarrollada en Python para automatizar el análisis de superficie de ataque externa mediante la recopilación de información de DNS, subdominios, servicios expuestos y vulnerabilidades asociadas.

El objetivo es centralizar información proveniente de múltiples fuentes y generar reportes ejecutivos que faciliten las actividades de reconocimiento, gestión de vulnerabilidades y evaluación perimetral.

---

## Características

### Enumeración de activos

- Consulta información DNS de dominios.
- Obtención de subdominios desde VirusTotal.
- Obtención de subdominios desde crt.sh.
- Resolución de direcciones IP.

### Identificación de infraestructura

- Detección de hosts protegidos por Cloudflare.
- Identificación de servicios expuestos.
- Enumeración de puertos abiertos.

### Gestión de vulnerabilidades

- Obtención de CVEs asociados a los servicios detectados.
- Consulta de severidad CVSS mediante NVD/NIST.
- Clasificación de vulnerabilidades por criticidad.

### Generación de reportes

- Exportación automática a Microsoft Word (.docx).
- Consolidación de hallazgos técnicos.
- Resumen de activos y vulnerabilidades identificadas.

---

## Arquitectura

```text
Dominio objetivo
        │
        ▼
  DNS / WHOIS
        │
        ▼
 Enumeración de Subdominios
 (VirusTotal + crt.sh)
        │
        ▼
 Resolución DNS
        │
        ▼
 Consulta de Shodan
        │
        ▼
 Obtención de CVEs
        │
        ▼
 Consulta NVD/NIST
        │
        ▼
 Generación de Reporte DOCX
```

---

## Tecnologías utilizadas

- Python 3
- Pandas
- Requests
- dnspython
- python-docx
- BeautifulSoup
- VirusTotal API
- Shodan
- NVD API

---

## Instalación

### Clonar repositorio

```cmd
git clone https://github.com/palvareza1337/Web-Scrapping.git
cd Web-Scrapping
```

### Crear entorno virtual

```cmd
python -m venv venv
```

### Activar entorno virtual

```cmd
venv\Scripts\activate
```

### Instalar dependencias

```cmd
pip install -r requirements.txt
```

---

## Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
VT_API_KEY=YOUR_VIRUSTOTAL_API_KEY
NVD_API_KEY=YOUR_NVD_API_KEY
```

---

## Uso

Ejecutar:

```cmd
python main.py
```

Ingresar el dominio objetivo cuando sea solicitado:

```text
Ingrese el dominio:
empresa.com
```

---

## Ejemplo de flujo

```text
[+] Obteniendo registros DNS
[+] Enumerando subdominios
[+] Resolviendo IPs
[+] Consultando Shodan
[+] Obteniendo CVEs
[+] Generando reporte
```

---

## Casos de uso

- Attack Surface Management (ASM)
- Reconocimiento externo
- Gestión de vulnerabilidades
- Inventario de activos expuestos
- Auditorías de seguridad
- Evaluaciones de riesgo

---

## Roadmap

### v1.0

- [x] Enumeración de subdominios mediante VirusTotal
- [x] Enumeración de subdominios mediante crt.sh
- [x] Resolución DNS
- [x] Identificación de servicios expuestos
- [x] Correlación de CVEs
- [x] Generación de reportes DOCX

### v2.0

- [ ] Variables de entorno para credenciales
- [ ] Concurrencia mediante ThreadPoolExecutor
- [ ] Exportación JSON
- [ ] Exportación HTML
- [ ] Soporte Docker
- [ ] Caché DNS
- [ ] Integración con API oficial de Shodan

---

## Disclaimer

Esta herramienta ha sido desarrollada exclusivamente con fines educativos, de investigación y evaluación de seguridad autorizada.

El uso indebido de esta herramienta es responsabilidad exclusiva del usuario.

---

## Autor

**Pablo Álvarez**

🔗 GitHub: https://github.com/palvareza1337

🔗 LinkedIn: https://www.linkedin.com/in/pabloalvarez1337/
