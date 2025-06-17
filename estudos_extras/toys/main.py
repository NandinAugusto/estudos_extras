from modules.tech_fingerprint import fingerprint_techs
from modules.vuln_lookup import buscar_vulnerabilidades

def main():
    alvo = input("Informe a URL do site (ex: https://example.com): ")
    print(f"\n🔍 Coletando tecnologias usadas em {alvo}...\n")
    techs = fingerprint_techs(alvo)

    if not techs:
        print("Nenhuma tecnologia identificada.")
        return

    for tech in techs:
        print(f"\n🧩 Tecnologia: {tech}")
        cves = buscar_vulnerabilidades(tech)
        if not cves:
            print("Nenhuma CVE relevante encontrada.")
        else:
            for cve_id, desc in cves:
                print(f" - {cve_id}: {desc[:100]}...")

if __name__ == "__main__":
    main()