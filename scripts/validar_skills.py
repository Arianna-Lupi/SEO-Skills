#!/usr/bin/env python3
"""Valida la estructura de todas las skills y agentes del repo.

Comprueba: frontmatter YAML estricto (con PyYAML si está; si no, una revisión básica),
`name` igual al de la carpeta, las dos cajas obligatorias, enlaces relativos a archivos que
existen, scripts que compilan, JSON de evals válidos, rayas largas fuera de las cajas y
agentes que solo referencian skills existentes.

Uso:  python3 scripts/validar_skills.py [--fix-frontmatter] [--json]
Salida: resumen legible (o JSON) y código 1 si hay errores.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"
# Skills utilitarias: no llevan la caja de cierre (dashboard-seo ES el cierre).
UTILITARIAS = {"dashboard-seo", "configurar-serpapi"}
DASH = re.compile("[—–]")


def split_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else (None, text)


def parse_yaml(block: str):
    try:
        import yaml  # type: ignore
    except ImportError:
        return None, "PyYAML no instalado (revisión básica)"
    try:
        return yaml.safe_load(block), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc).splitlines()[0]


def quote_unsafe_values(block: str) -> str:
    """Pone entre comillas los valores de primer nivel que YAML no podría leer (contienen ': ' o ' #')."""
    out = []
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s+(.*)$", line)
        if m and m.group(2) and m.group(2)[0] not in "\"'|>[{&*!%@`" and (": " in m.group(2) or " #" in m.group(2)):
            line = f"{m.group(1)}: {json.dumps(m.group(2), ensure_ascii=False)}"
        out.append(line)
    return "\n".join(out)


def check_router(errors: list[str], skill_names: set[str], agent_names: set[str]) -> None:
    """Valida el enrutador /aprendoclub: cada skill, agente y script que nombra debe existir,
    y cada comando de su tabla debe estar documentado en docs/COMANDOS.md."""
    router = SKILLS / "aprendoclub"
    if not router.is_dir():
        return
    scripts = {p.name for p in SKILLS.glob("*/scripts/*.py")}
    known = skill_names | agent_names | {"aprendoclub-run"}  # lanzador de scripts, no es skill
    for md in sorted(router.rglob("*.md")):
        rel = md.relative_to(ROOT)
        for token in set(re.findall(r"`([^`\n]+)`", md.read_text(encoding="utf-8"))):
            if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", token) and token not in known:
                errors.append(f"{rel}: nombra `{token}`, que no es una skill ni un agente existente")
            if re.fullmatch(r"[a-z0-9_]+\.py", token) and token not in scripts:
                errors.append(f"{rel}: nombra el script `{token}`, que no existe en skills/*/scripts/")
    text = (router / "SKILL.md").read_text(encoding="utf-8")
    commands = sorted(set(re.findall(r"`/aprendoclub ([a-z]+)", text)))
    if not commands:
        errors.append("aprendoclub/SKILL.md: no declara ningún comando")
    docs = ROOT / "docs" / "COMANDOS.md"
    if not docs.exists():
        errors.append("docs/COMANDOS.md: falta (documenta los comandos de /aprendoclub)")
    else:
        doc_text = docs.read_text(encoding="utf-8")
        for c in commands:
            if f"/aprendoclub {c}" not in doc_text:
                errors.append(f"docs/COMANDOS.md: falta documentar `/aprendoclub {c}`")
    for f in ("install.sh", "install.ps1", "uninstall.sh", "uninstall.ps1", ".claude-plugin/plugin.json",
              ".claude-plugin/marketplace.json"):
        if not (ROOT / f).exists():
            errors.append(f"{f}: falta (instalación rápida)")
    for f in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        pth = ROOT / f
        if pth.exists():
            try:
                json.loads(pth.read_text(encoding="utf-8"))
            except ValueError as exc:
                errors.append(f"{f}: JSON inválido ({exc})")
    ver = ROOT / "VERSION"
    if ver.exists():
        v = ver.read_text(encoding="utf-8").strip()
        try:
            pj = ROOT / ".claude-plugin" / "plugin.json"
            if pj.exists() and json.loads(pj.read_text(encoding="utf-8")).get("version") != v:
                errors.append("plugin.json: version no coincide con VERSION")
            mj = ROOT / ".claude-plugin" / "marketplace.json"
            if mj.exists():
                for plug in json.loads(mj.read_text(encoding="utf-8")).get("plugins", []):
                    if plug.get("version") != v:
                        errors.append("marketplace.json: la version del plugin no coincide con VERSION")
        except ValueError:
            pass
    if not (ROOT / "CHANGELOG.md").exists():
        errors.append("CHANGELOG.md: falta (novedades para alumnos, lo lee /aprendoclub update)")


ENV_RE = re.compile(r"""(?:environ(?:\.get)?\(?\[?|getenv\()\s*["']([A-Z][A-Z0-9_]+)["']""")


def check_requisitos(errors: list[str], warnings: list[str]) -> None:
    """requisitos.json: cada script del repo está en el manifiesto y coincide con lo que importa y lee."""
    path = SKILLS / "aprendoclub" / "requisitos.json"
    if not path.exists():
        errors.append("skills/aprendoclub/requisitos.json: falta el manifiesto de requisitos")
        return
    try:
        man = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        errors.append(f"requisitos.json: JSON inválido ({exc})")
        return
    std = getattr(sys, "stdlib_module_names", None)
    if std is None:
        warnings.append("requisitos.json: Python < 3.10, no se compararon los imports con el manifiesto")
    declared = man.get("scripts", {})
    known_env = set(man.get("claves", {})) | set(man.get("variables", {}))
    paquetes = man.get("paquetes", {})
    found = set()
    for py in sorted(SKILLS.glob("*/scripts/*.py")):
        skill = py.parent.parent.name
        if skill == "aprendoclub" or py.name.startswith("_"):
            continue
        key = f"{skill}/{py.name}"
        found.add(key)
        entry = declared.get(key)
        if entry is None:
            errors.append(f"requisitos.json: falta el script {key}")
            continue
        src = py.read_text(encoding="utf-8")
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        mods = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                mods.update(a.name.split(".")[0] for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                mods.add(n.module.split(".")[0])
        if std is not None:
            third = {m for m in mods if m not in std and not (py.parent / f"{m}.py").exists()}
            listed = set(entry.get("python", [])) | set(entry.get("python_opcional", []))
            if third - listed:
                errors.append(f"requisitos.json: {key} importa {sorted(third - listed)} que no están declarados")
            if listed - third:
                errors.append(f"requisitos.json: {key} declara {sorted(listed - third)} que el script no importa")
        for m in set(entry.get("python", [])) | set(entry.get("python_opcional", [])):
            if m not in paquetes:
                errors.append(f"requisitos.json: {key} usa el módulo {m} que no está en 'paquetes'")
        reads = set(ENV_RE.findall(src))
        declared_env = set(entry.get("env", {}))
        if reads != declared_env:
            errors.append(f"requisitos.json: {key} lee {sorted(reads)} pero declara {sorted(declared_env)}")
        for name in declared_env - known_env:
            errors.append(f"requisitos.json: {key} usa la variable {name} sin definirla en 'claves' o 'variables'")
        for tool in entry.get("herramientas", []):
            if tool not in man.get("herramientas", {}):
                errors.append(f"requisitos.json: {key} usa la herramienta {tool} sin definirla en 'herramientas'")
        needs_any = entry.get("python") or entry.get("python_opcional") or any(
            v == "requerida" for v in entry.get("env", {}).values()) or entry.get("herramientas")
        if needs_any and not entry.get("modo_manual"):
            errors.append(f"requisitos.json: {key} necesita algo externo pero no declara 'modo_manual'")
    for key in sorted(set(declared) - found):
        errors.append(f"requisitos.json: declara {key}, que no existe en skills/*/scripts/")
    for name in man.get("claves", {}):
        if any(x in name for x in ("=", " ")) or any(isinstance(v, str) and v.startswith("sk-") for v in man["claves"][name].values()):
            errors.append(f"requisitos.json: la clave {name} parece traer un valor; solo se guardan nombres")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fix-frontmatter", action="store_true", help="arregla valores sin comillas en el frontmatter")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    names = set()

    for sd in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        names.add(sd.name)
        md = sd / "SKILL.md"
        if not md.exists():
            errors.append(f"{sd.name}: falta SKILL.md")
            continue
        text = md.read_text(encoding="utf-8")
        block, body = split_frontmatter(text)
        if block is None:
            errors.append(f"{sd.name}: sin frontmatter")
            continue
        data, err = parse_yaml(block)
        if err and data is None and "PyYAML" not in err:
            if args.fix_frontmatter:
                fixed = quote_unsafe_values(block)
                data, err2 = parse_yaml(fixed)
                if data is not None:
                    md.write_text(text.replace(block, fixed, 1), encoding="utf-8")
                    warnings.append(f"{sd.name}: frontmatter arreglado (comillas)")
                    text = md.read_text(encoding="utf-8")
                    block, body = split_frontmatter(text)
                else:
                    errors.append(f"{sd.name}: frontmatter no parsea ni tras arreglar ({err2})")
            else:
                errors.append(f"{sd.name}: frontmatter YAML inválido ({err})")
        if isinstance(data, dict):
            if data.get("name") != sd.name:
                errors.append(f"{sd.name}: name del frontmatter ({data.get('name')!r}) no coincide con la carpeta")
            if not str(data.get("description", "")).strip():
                errors.append(f"{sd.name}: description vacía")
        if "Regla de datos" not in text:
            errors.append(f"{sd.name}: falta la caja 'Regla de datos'")
        if "Cierre en dashboard" not in text and sd.name not in UTILITARIAS:
            errors.append(f"{sd.name}: falta la caja 'Cierre en dashboard'")
        for line_no, line in enumerate(body.splitlines(), 1):
            if DASH.search(line) and not line.lstrip().startswith(">"):
                warnings.append(f"{sd.name}/SKILL.md:{line_no}: raya larga o media fuera de las cajas estándar")
                break
        for target in re.findall(r"\]\(((?!https?:|#|mailto:)[^)\s]+)\)", text):
            if not (sd / target.split("#")[0]).exists():
                errors.append(f"{sd.name}: enlace roto a {target}")
        for py in sd.rglob("*.py"):
            try:
                compile(py.read_text(encoding="utf-8"), str(py), "exec")
            except SyntaxError as exc:
                errors.append(f"{py.relative_to(ROOT)}: no compila ({exc.msg}, línea {exc.lineno})")
        for js in sd.rglob("evals/*.json"):
            try:
                json.loads(js.read_text(encoding="utf-8"))
            except ValueError as exc:
                errors.append(f"{js.relative_to(ROOT)}: JSON inválido ({exc})")
        refs = sd / "references"
        if refs.is_dir() and not (refs / "metodo-diploma.md").exists():
            warnings.append(f"{sd.name}: tiene references/ pero no metodo-diploma.md")

    for ag in sorted(AGENTS.glob("*.md")):
        text = ag.read_text(encoding="utf-8")
        ablock, _ = split_frontmatter(text)
        if ablock is None:
            errors.append(f"{ag.name}: sin frontmatter")
        else:
            adata, aerr = parse_yaml(ablock)
            if adata is None and aerr and "PyYAML" not in aerr:
                if args.fix_frontmatter:
                    fixed = quote_unsafe_values(ablock)
                    if parse_yaml(fixed)[0] is not None:
                        ag.write_text(text.replace(ablock, fixed, 1), encoding="utf-8")
                        warnings.append(f"{ag.name}: frontmatter arreglado (comillas)")
                        text = ag.read_text(encoding="utf-8")
                    else:
                        errors.append(f"{ag.name}: frontmatter no parsea ni tras arreglar")
                else:
                    errors.append(f"{ag.name}: frontmatter YAML inválido ({aerr})")
        missing = [r for r in re.findall(r"skills/([a-z0-9-]+)", text) if r not in names]
        if missing:
            errors.append(f"{ag.name}: referencia skills inexistentes {sorted(set(missing))}")

    check_router(errors, names, {a.stem for a in AGENTS.glob("*.md")})
    check_requisitos(errors, warnings)

    result = {"skills": len(names), "agentes": len(list(AGENTS.glob('*.md'))), "errores": errors, "avisos": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['skills']} skills · {result['agentes']} agentes · {len(errors)} errores · {len(warnings)} avisos")
        for e in errors:
            print("ERROR:", e)
        for w in warnings:
            print("aviso:", w)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
