#!/usr/bin/env python3
"""
Crawl limitado (mismo host, hasta 2 niveles) y listar formularios.
Uso: python3 crawl_forms.py https://example.local
Advertencia: ejecutar solo en entornos de pruebas o con permiso.
"""

import sys
import time
import requests
from urllib.parse import urlparse, urljoin #normalizarURL
from urllib.robotparser import RobotFileParser #leer el robots.txt
from bs4 import BeautifulSoup 
from collections import deque #para el algoritmo BFS 

# Config
USER_AGENT = "SimpleFormCrawler/1.0 (+https://example.local)" #Identificar el crawler,
TIMEOUT = 8 # evita que una petición quede bloqueada demasiado tiempo 
RATE_DELAY = 0.5  # segundos entre peticiones
MAX_DEPTH = 2 #profundidad máxima

session = requests.Session() #realiza la conexión TCP y comparte headers
session.headers.update({"User-Agent": USER_AGENT})


def allowed_by_robots(base_url, target_url):
    rp = RobotFileParser() #parsear el robots
    parsed = urlparse(base_url) #parsear la url 
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt" #url del robot
    try:
        rp.set_url(robots_url) #setear la URL 
        rp.read() #leer el robots
    except Exception:
        # Si no hay robots.txt o no se puede leer, asumir permitimos (pero cuidado)
        return True
    return rp.can_fetch(USER_AGENT, target_url) #podemos hacerle fetch a la url


def same_host(u1, u2):
    p1 = urlparse(u1)
    p2 = urlparse(u2)
    return p1.netloc == p2.netloc #compara que las dos url pertenezcan al mismo host


def normalize_url(base, link):
    if not link:
        return None #verificar si no es un link
    parsed_link = urlparse(link) #paresar el link 
    if parsed_link.scheme and parsed_link.netloc:
        return link.split("#")[0]  # quitar fragmentos
    # href puede ser relativo
    joined = urljoin(base, link) #hacer el join the la url base y el link
    return joined.split("#")[0] #quitar los #


def extract_forms(html, page_url):
    #extraer los formularios
    soup = BeautifulSoup(html, "html.parser")
    forms = []
    for form in soup.find_all("form"):
        action = form.get("action") or ""
        method = form.get("method", "GET").upper()
        inputs = []
        # inputs
        for i in form.find_all(["input", "select", "textarea"]):
            name = i.get("name")
            typ = i.get("type") if i.name == "input" else i.name
            value = i.get("value", "")
            inputs.append({"name": name, "type": typ, "value": value})
        forms.append({"page": page_url, "action": action, "method": method, "inputs": inputs})
    return forms


def crawl(start_url):
    visited = set()
    results = []
    q = deque()
    q.append((start_url, 0))

    while q:
        url, depth = q.popleft()
        if url in visited:
            continue
        visited.add(url)

        if not allowed_by_robots(start_url, url):
            print(f"[robots] SKIP {url}")
            continue

        try:
            resp = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        except Exception as e:
            print(f"[error] {url} -> {e}")
            continue

        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            # no es HTML, saltar
            # print(f"[skip] no-html {url} ({content_type})")
            continue

        html = resp.text
        forms = extract_forms(html, url)
        if forms:
            results.extend(forms)
            print(f"[forms] {len(forms)} form(s) on {url}")

        # si podemos profundizar, extraemos enlaces
        if depth < MAX_DEPTH:
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                norm = normalize_url(url, href)
                if not norm:
                    continue
                # solo mismo host
                if not same_host(start_url, norm):
                    continue
                if norm not in visited:
                    q.append((norm, depth + 1))

        time.sleep(RATE_DELAY)

    return results


def main():
    if len(sys.argv) < 2:
        print("Uso: python crawl_forms.py https://target.local")
        sys.exit(1)
    start = sys.argv[1].rstrip("/")
    print(f"Starting crawl at {start} (max depth {MAX_DEPTH})")
    forms = crawl(start)
    print("\n==== FORMS FOUND ====\n")
    for i, f in enumerate(forms, 1):
        print(f"Form #{i}")
        print(" Page : ", f["page"])
        print(" Action: ", f["action"])
        print(" Method: ", f["method"])
        print(" Inputs:")
        for inp in f["inputs"]:
            print("   -", inp)
        print("-" * 40)


if __name__ == "__main__":
    main()
