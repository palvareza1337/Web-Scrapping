import whois
import dns.resolver
from ipwhois import IPWhois


# Consulta WHOIS de dominio
def consulta_whois(dominio):
    try:
        info = whois.whois(dominio)
        return info
    except Exception as e:
        return f"Error en WHOIS: {e}"


# Consulta DNS
def consulta_dns(dominio, tipo='A'):
    resultados = []
    try:
        respuestas = dns.resolver.resolve(dominio, tipo)
        for rdata in respuestas:
            resultados.append(str(rdata).strip())
    except Exception:
        pass
    return resultados


# Consulta DNS y resuelve IPs
def consulta_dns_resuelta(dominio, tipo='A'):
    registros = consulta_dns(dominio, tipo)
    registros_resueltos = {}

    if tipo == 'A':
        registros_resueltos[dominio] = registros
    else:
        for registro in registros:
            try:
                ips = consulta_dns(registro, 'A')
                registros_resueltos[registro] = ips
            except:
                registros_resueltos[registro] = []

    return registros_resueltos


# Consulta WHOIS de IP
def consulta_whois_ip(ip):
    try:
        obj = IPWhois(ip)
        result = obj.lookup_rdap()
        return result
    except Exception as e:
        return f"Error en WHOIS IP: {e}"


if __name__ == "__main__":

    dominio = input("Por favor, ingrese el dominio: ")

    info_whois = consulta_whois(dominio)
    info_dns_NS = consulta_dns_resuelta(dominio, 'NS')
    info_dns_A = consulta_dns_resuelta(dominio, 'A')
    info_dns_MX = consulta_dns_resuelta(dominio, 'MX')
    info_dns_TXT = consulta_dns(dominio, 'TXT')

    info_whois_ip = None
    if info_dns_A and info_dns_A[dominio]:
        primera_ip = info_dns_A[dominio][0]
        if primera_ip:
            info_whois_ip = consulta_whois_ip(primera_ip)

    print("\nInformación WHOIS del Dominio:")
    print(info_whois)

    print("\nRegistros NS y sus IPs:")
    for registro, ips in info_dns_NS.items():
        print(f"{registro}: {', '.join(ips)}")

    print("\nRegistros A y sus IPs:")
    print(f"{dominio}: {', '.join(info_dns_A[dominio])}")

    print("\nRegistros MX y sus IPs:")
    for registro, ips in info_dns_MX.items():
        print(f"{registro}: {', '.join(ips)}")

    print("\nRegistros TXT:")
    for registro in info_dns_TXT:
        print(registro)

    if info_whois_ip:
        print("\nInformación WHOIS de la IP:")
        print(info_whois_ip)