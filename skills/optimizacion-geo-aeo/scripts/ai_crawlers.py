#!/usr/bin/env python3
"""
ai_crawlers.py: revisa que rastreadores de IA permite o bloquea el robots.txt de un sitio
y si existe /llms.txt (opcional).

Complemento externo adaptado de claude-seo (MIT, agricidaniel), reescrito con solo stdlib.
Lee robots.txt como lo haria un rastreador: elige el grupo de User-agent mas especifico y
aplica la regla Allow/Disallow de ruta mas larga sobre "/".

Uso:
    python3 ai_crawlers.py ejemplo.com
    python3 ai_crawlers.py https://ejemplo.com --out .seo-audit/ejemplo.com/data/ai-features.json
    python3 ai_crawlers.py --robots-file robots.txt

Salida (stdout, JSON):
    {"ok": true, "site": "...", "robots_status": 200, "crawlers": [{"agent","owner","purpose",
     "kind","status":"permitido|bloqueado|sin-regla-especifica","obeys_robots":bool}],
     "llms_txt": {"present": bool, "note": "..."}, "advice": [...]}
Con --out se FUSIONA la clave "crawlers" dentro del JSON existente (p. ej. ai-features.json)
sin tocar el resto. Si falla: {"ok": false, "reason": "...", "fallback": "..."} (exit 0).

Deps: solo stdlib. User-Agent de navegador; detecta WAF basico. Una sola peticion por archivo.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# agent, owner, purpose, kind (busqueda | entrenamiento | usuario), obeys_robots
CRAWLERS = [
    ("GPTBot", "OpenAI", "Entrenamiento y rastreo de OpenAI", "entrenamiento", True),
    ("OAI-SearchBot", "OpenAI", "Busqueda de ChatGPT", "busqueda", True),
    ("ChatGPT-User", "OpenAI", "Navegacion pedida por un usuario", "usuario", False),
    ("ClaudeBot", "Anthropic", "Rastreo de Anthropic", "entrenamiento", True),
    ("anthropic-ai", "Anthropic", "Entrenamiento de Claude", "entrenamiento", True),
    ("PerplexityBot", "Perplexity", "Indice de busqueda de Perplexity", "busqueda", True),
    ("Google-Extended", "Google", "Opt-out de entrenamiento y grounding de Gemini (no afecta a Google Search)", "entrenamiento", True),
    ("CCBot", "Common Crawl", "Datos abiertos usados para entrenar modelos", "entrenamiento", True),
    ("Bytespider", "ByteDance", "IA de ByteDance", "entrenamiento", True),
    ("cohere-ai", "Cohere", "Modelos de Cohere", "entrenamiento", True),
    ("Applebot-Extended", "Apple", "Opt-out de entrenamiento de Apple Intelligence", "entrenamiento", True),
    ("Bingbot", "Microsoft", "Indice de Bing que alimenta a Copilot", "busqueda", True),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(str(e))


def parse_groups(text):
    groups, cur, last_was_ua = [], None, False
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if cur is None or not last_was_ua:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(v.lower())
            last_was_ua = True
        elif k in ("allow", "disallow") and cur is not None:
            cur["rules"].append((k, v))
            last_was_ua = False
        else:
            last_was_ua = False
    return groups


def verdict(groups, agent):
    a = agent.lower()
    specific = [g for g in groups if a in g["agents"]]
    star = [g for g in groups if "*" in g["agents"]]
    chosen, label = (specific, "especifica") if specific else (star, "comodin")
    if not chosen:
        return "permitido", "sin-grupo"
    best_len, allowed = -1, True
    for g in chosen:
        for kind, path in g["rules"]:
            if path == "" and kind == "disallow":
                continue
            if "/".startswith(path.rstrip("*")) or path in ("/", "/*"):
                if len(path) > best_len or (len(path) == best_len and kind == "allow"):
                    best_len, allowed = len(path), kind == "allow"
    state = "permitido" if allowed else "bloqueado"
    return (state, label) if specific else (state if allowed else "bloqueado", label)


def main():
    p = argparse.ArgumentParser(description="Que rastreadores de IA permite el robots.txt.")
    p.add_argument("site", nargs="?", help="Dominio o URL (ej. ejemplo.com).")
    p.add_argument("--robots-file", help="robots.txt local (modo manual).")
    p.add_argument("--out", help="JSON donde fusionar la clave 'crawlers' (ej. .../data/ai-features.json).")
    a = p.parse_args()

    def fail(reason):
        print(json.dumps({"ok": False, "reason": reason,
                          "fallback": "modo manual: abre /robots.txt y /llms.txt en el navegador y compara con la lista de rastreadores"},
                         ensure_ascii=False))
        sys.exit(0)

    if not a.site and not a.robots_file:
        fail("indica un sitio o --robots-file")
    status, text, llms = None, "", {"present": None, "note": "no comprobado"}
    site = a.site or "(archivo local)"
    try:
        if a.robots_file:
            text, status = open(a.robots_file, encoding="utf-8").read(), 200
        else:
            base = a.site if a.site.startswith("http") else "https://" + a.site
            base = base.rstrip("/")
            site = base
            status, text = get(base + "/robots.txt")
            if status in (403, 429, 503):
                fail(f"HTTP {status} en robots.txt: posible WAF. Pega el robots.txt con --robots-file.")
            ls, lt = get(base + "/llms.txt")
            llms = {"present": ls == 200 and bool(lt.strip()),
                    "note": "Opcional. Google Search no lo usa ni lo necesita; su valor para otras IAs no esta demostrado."}
    except (RuntimeError, OSError) as e:
        fail(str(e))

    groups = parse_groups(text) if status == 200 else []
    rows, blocked_search = [], []
    for agent, owner, purpose, kind, obeys in CRAWLERS:
        if not obeys:
            state = "no-aplica (ignora robots.txt)"
        elif status != 200:
            state = "permitido (sin robots.txt)"
        else:
            state, _ = verdict(groups, agent)
        rows.append({"agent": agent, "owner": owner, "purpose": purpose, "kind": kind,
                     "status": state, "obeys_robots": obeys})
        if state == "bloqueado" and kind == "busqueda":
            blocked_search.append(agent)
    advice = []
    if blocked_search:
        advice.append("Bloqueas rastreadores de BUSQUEDA con IA (" + ", ".join(blocked_search) +
                      "): no podran citarte. Confirma que es una decision de negocio.")
    advice.append("Decide por separado entrenamiento (GPTBot, CCBot, Google-Extended) y busqueda (OAI-SearchBot, PerplexityBot): bloquear uno no implica bloquear el otro.")
    advice.append("Los fetchers disparados por un usuario (ChatGPT-User) ignoran robots.txt; para limitarlos hay que usar controles en el servidor.")
    advice.append("Google-Extended no afecta al posicionamiento en Google Search ni a AI Overviews; la inclusion en AI Overviews depende de Googlebot.")
    res = {"ok": True, "site": site, "robots_status": status, "crawlers": rows, "llms_txt": llms, "advice": advice}
    if a.out:
        existing = {}
        if os.path.exists(a.out):
            try:
                existing = json.load(open(a.out, encoding="utf-8"))
            except ValueError:
                existing = {}
        existing["crawlers"] = rows
        existing["llms_txt"] = llms
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(existing, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
