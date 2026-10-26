"""Pruebas del enrutador /aprendoclub: manifiesto de requisitos, preflight, lanzador y actualización.

Solo stdlib. Ninguna prueba usa la red de verdad ni toca tu HOME (cada una usa carpetas temporales).
Ejecutar:  python3 tests/test_aprendoclub.py
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "aprendoclub" / "scripts"
REQ = SCRIPTS / "requisitos.py"
RUN = SCRIPTS / "aprendoclub-run"
SECRETO = "VALOR-SECRETO-123"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd, env_extra=None, home=None, **kw):
    env = dict(os.environ)
    env.pop("APRENDOCLUB_PYTHON", None)
    if home:
        env["HOME"] = str(home)
        env["APRENDOCLUB_HOME"] = str(Path(home) / ".claude" / "aprendoclub")
    env.update(env_extra or {})
    return subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120, **kw)


class Preflight(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / ".claude").mkdir()
        self.man = self.tmp / "req.json"
        self.man.write_text(json.dumps({
            "paquetes": {"modulo_que_no_existe_xyz": {"pip": "paquete-falso"}},
            "claves": {"CLAVE_FALSA_XYZ": {"para": "pruebas", "donde": "en ningún lado", "alternativa": "modo manual"}},
            "scripts": {"x/y.py": {"python": ["modulo_que_no_existe_xyz"], "env": {"CLAVE_FALSA_XYZ": "requerida"},
                                   "modo_manual": "hazlo a mano"}},
        }), encoding="utf-8")
        self.env = {"APRENDOCLUB_REQUISITOS": str(self.man)}

    def test_sin_dependencias_devuelve_needs_y_no_falla(self):
        r = run([sys.executable, str(REQ), "--check", "x/y.py"], self.env, self.tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertFalse(out["ok"])
        tipos = {n["type"] for n in out["needs"]}
        self.assertEqual(tipos, {"python_dep", "api_key"})
        self.assertIn("reason", out)       # contrato antiguo se conserva
        self.assertEqual(out["fallback"], "hazlo a mano")
        dep = next(n for n in out["needs"] if n["type"] == "python_dep")
        self.assertIn("--yes", dep["command"])
        self.assertTrue(dep["required"])

    def test_ejecutar_sin_requisitos_no_corre_y_sale_con_3(self):
        r = run([sys.executable, str(REQ), "x/y.py"], self.env, self.tmp)
        self.assertEqual(r.returncode, 3)
        self.assertFalse(json.loads(r.stdout)["ok"])

    def test_instalar_sin_yes_solo_muestra_el_plan(self):
        r = run([sys.executable, str(REQ), "--install", "x/y.py"], self.env, self.tmp)
        self.assertEqual(r.returncode, 3)
        out = json.loads(r.stdout)
        self.assertIn("plan", out)
        self.assertEqual(out["plan"]["packages"], ["paquete-falso"])
        self.assertFalse((self.tmp / ".claude" / "aprendoclub" / ".venv").exists())

    def test_yes_despues_del_script_se_reconoce(self):
        # el paquete falso no existe: la instalación debe INTENTARSE (y fallar), no quedarse pidiendo confirmación
        r = run([sys.executable, str(REQ), "--install", "x/y.py", "--yes"], self.env, self.tmp)
        self.assertEqual(r.returncode, 3)
        self.assertNotIn("falta confirmación", json.loads(r.stdout)["reason"])

    @unittest.skipUnless(os.environ.get("APRENDOCLUB_TEST_NET") == "1", "necesita red: APRENDOCLUB_TEST_NET=1")
    def test_instalacion_real_en_entorno_aislado(self):
        man = json.loads(self.man.read_text(encoding="utf-8"))
        man["paquetes"] = {"colorama": {"pip": "colorama"}}
        man["scripts"]["x/y.py"]["python"] = ["colorama"]
        self.man.write_text(json.dumps(man), encoding="utf-8")
        r = run([sys.executable, str(REQ), "--install", "x/y.py", "--yes"], self.env, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.tmp / ".claude" / "aprendoclub" / ".venv").exists())

    def test_clave_presente_en_archivo_no_se_pide_ni_se_imprime(self):
        (self.tmp / ".claude" / "seo-skills.env").write_text(f"CLAVE_FALSA_XYZ={SECRETO}\n", encoding="utf-8")
        r = run([sys.executable, str(REQ), "--check", "x/y.py"], self.env, self.tmp)
        out = json.loads(r.stdout)
        self.assertNotIn("api_key", {n["type"] for n in out["needs"]})
        self.assertNotIn(SECRETO, r.stdout + r.stderr)

    def test_status_no_filtra_valores(self):
        (self.tmp / ".claude" / "seo-skills.env").write_text(f"SERPAPI_API_KEY={SECRETO}\n", encoding="utf-8")
        r = run([sys.executable, str(REQ), "--status"], {}, self.tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["claves"]["SERPAPI_API_KEY"]["estado"], "archivo")
        self.assertNotIn(SECRETO, r.stdout)

    def test_lanzador_sin_python_explica_que_hacer(self):
        r = subprocess.run(["/bin/bash", str(RUN), "--check", "serp.py"], capture_output=True, text=True,
                           env={"PATH": "/nonexistent", "HOME": str(self.tmp)}, timeout=30)
        self.assertEqual(r.returncode, 3)
        out = json.loads(r.stdout)
        self.assertFalse(out["ok"])
        self.assertEqual(out["needs"][0]["type"], "python")

    def test_lanzador_con_python_chequea_script_real(self):
        r = run(["bash", str(RUN), "--check", "generar_plan.py"], {}, self.tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(json.loads(r.stdout)["ok"])

    def test_check_all_deduplica(self):
        r = run([sys.executable, str(REQ), "--check", "--all"], {}, self.tmp)
        needs = json.loads(r.stdout)["needs"]
        nombres = [(n["type"], n["name"]) for n in needs]
        self.assertEqual(len(nombres), len(set(nombres)))


class ManifiestoYValidador(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        shutil.copytree(ROOT / "skills", self.tmp / "skills", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "docs", self.tmp / "docs")
        self.v = load("validar", ROOT / "scripts" / "validar_skills.py")
        self.v.SKILLS = self.tmp / "skills"
        self.v.ROOT = self.tmp
        self.addCleanup(lambda: (setattr(self.v, "SKILLS", ROOT / "skills"), setattr(self.v, "ROOT", ROOT)))

    def test_todo_script_esta_en_el_manifiesto(self):
        errs, warns = [], []
        self.v.check_requisitos(errs, warns)
        self.assertEqual(errs, [])

    def test_detecta_script_sin_declarar_y_clave_distinta(self):
        mpath = self.tmp / "skills" / "aprendoclub" / "requisitos.json"
        man = json.loads(mpath.read_text(encoding="utf-8"))
        del man["scripts"]["analisis-serp-y-competencia/serp.py"]
        man["scripts"]["inventario-de-urls/inventario_urls.py"]["env"] = {"OTRA_VARIABLE": "opcional"}
        mpath.write_text(json.dumps(man), encoding="utf-8")
        errs, warns = [], []
        self.v.check_requisitos(errs, warns)
        texto = "\n".join(errs)
        self.assertIn("falta el script analisis-serp-y-competencia/serp.py", texto)
        self.assertIn("inventario_urls.py lee", texto)

    def test_detecta_skill_inexistente_en_el_enrutador(self):
        ref = self.tmp / "skills" / "aprendoclub" / "references" / "comandos-tecnico.md"
        ref.write_text(ref.read_text(encoding="utf-8") + "\nUsa `skill-que-no-existe`.\n", encoding="utf-8")
        errs = []
        self.v.check_router(errs, {p.name for p in (self.tmp / "skills").iterdir() if p.is_dir()},
                            {a.stem for a in (ROOT / "agents").glob("*.md")})
        self.assertTrue(any("skill-que-no-existe" in e for e in errs), errs)

    def test_detecta_comando_sin_documentar(self):
        (self.tmp / "docs" / "COMANDOS.md").write_text("# vacío\n", encoding="utf-8")
        errs = []
        self.v.check_router(errs, {p.name for p in (self.tmp / "skills").iterdir() if p.is_dir()},
                            {a.stem for a in (ROOT / "agents").glob("*.md")})
        self.assertTrue(any("falta documentar" in e for e in errs))


class Actualizacion(unittest.TestCase):
    def test_parse_changelog(self):
        act = load("actualizar", SCRIPTS / "actualizar.py")
        texto = "# N\n\n## Próxima versión\n\n- borrador\n\n## [1.4.0] - 2026-10-26\n\n- A\n- B\n\n## [1.3.0]\n\n- C\n"
        secs = act.parse_changelog(texto)
        self.assertEqual([s["version"] for s in secs], ["1.4.0", "1.3.0"])
        self.assertEqual(secs[0]["puntos"], ["A", "B"])
        self.assertEqual(secs[0]["fecha"], "2026-10-26")

    def test_comparacion_de_versiones(self):
        act = load("actualizar2", SCRIPTS / "actualizar.py")
        self.assertGreater(act.vtuple("1.10.0"), act.vtuple("1.9.9"))

    def test_check_sin_red_no_falla(self):
        env = {"https_proxy": "http://127.0.0.1:9", "HTTPS_PROXY": "http://127.0.0.1:9", "no_proxy": "", "NO_PROXY": ""}
        r = run([sys.executable, str(SCRIPTS / "actualizar.py"), "--check"], env)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertTrue(out["ok"])
        self.assertIs(out["conexion"], False)
        self.assertIn("comando_actualizar", out)

    def test_check_offline_no_usa_red(self):
        r = run([sys.executable, str(SCRIPTS / "actualizar.py"), "--check", "--offline"])
        out = json.loads(r.stdout)
        self.assertIsNone(out["conexion"])

    def test_aviso_apagado_por_defecto_no_imprime(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        r = run([sys.executable, str(SCRIPTS / "actualizar.py"), "--aviso"], home=tmp)
        self.assertEqual(r.stdout.strip(), "")
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
