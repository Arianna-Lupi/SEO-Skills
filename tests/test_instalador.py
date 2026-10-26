"""Pruebas del instalador rápido, la actualización y la desinstalación (install.sh, uninstall.sh).

Usan siempre --dir con carpetas temporales: no tocan ~/.claude ni la red.
Ejecutar:  python3 tests/test_instalador.py
"""
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL = ROOT / "install.sh"
UNINSTALL = ROOT / "uninstall.sh"
NO_NET = {"https_proxy": "http://127.0.0.1:9", "HTTPS_PROXY": "http://127.0.0.1:9", "no_proxy": "", "NO_PROXY": ""}


def sh(args, cwd=None, env=None, stdin=None):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run(["bash", *args], capture_output=True, text=True, cwd=cwd, env=e, timeout=120, stdin=stdin)


class Instalador(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.dest = self.tmp / "destino"

    def instalar(self, *extra, **kw):
        return sh([str(INSTALL), "--dir", str(self.dest), *extra], stdin=subprocess.DEVNULL, **kw)

    def test_instala_todo_sin_preguntar_y_rapido(self):
        t0 = time.time()
        r = self.instalar()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertLess(time.time() - t0, 10, "la instalación rápida debe tardar menos de ~10 s")
        skills = [p for p in (self.dest / "skills").iterdir() if (p / "SKILL.md").exists()]
        self.assertEqual(len(skills), len(list((ROOT / "skills").glob("*/SKILL.md"))))
        self.assertTrue((self.dest / "skills" / "aprendoclub" / "requisitos.json").exists())
        self.assertTrue(os.access(self.dest / "skills" / "aprendoclub" / "scripts" / "aprendoclub-run", os.X_OK))
        self.assertEqual(len(list((self.dest / "agents").glob("*.md"))), len(list((ROOT / "agents").glob("*.md"))))
        self.assertEqual((self.dest / "skills" / ".seo-skills-version").read_text().strip(),
                         (ROOT / "VERSION").read_text().strip())
        self.assertIn("/aprendoclub audit", r.stdout)
        self.assertFalse(list(self.dest.rglob("__pycache__")))

    def test_no_instala_uv_ni_pregunta_por_defecto(self):
        r = self.instalar(env={"PATH": "/usr/bin:/bin"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("Instalando uv", r.stdout)

    def test_idempotente_y_sin_respaldos_si_nadie_toco_nada(self):
        self.instalar()
        r = self.instalar()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dest / ".seo-skills-backups").exists())
        self.assertNotIn("Detecté", r.stdout)

    def test_actualizar_conserva_config_y_seo_audit_y_respalda_cambios(self):
        self.instalar()
        # estado "de una versión anterior" con trabajo del usuario
        (self.dest / "skills" / ".seo-skills-version").write_text("1.2.0\n")
        skill = self.dest / "skills" / "brief-de-contenido" / "SKILL.md"
        skill.write_text(skill.read_text() + "\n# nota mía\n")
        (self.dest / "skills" / "plan-seo" / "MI-ARCHIVO.txt").write_text("importante")
        propia = self.dest / "skills" / "mi-skill-propia"
        propia.mkdir()
        (propia / "SKILL.md").write_text("---\nname: mi-skill-propia\n---\n")
        env_file = self.dest / "seo-skills.env"
        env_file.write_text("SERPAPI_API_KEY=abc\n")
        audit = self.dest / ".seo-audit" / "x.com" / "data"
        audit.mkdir(parents=True)
        (audit / "issues.json").write_text("{}")

        r = self.instalar()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Actualizadas", r.stdout)
        self.assertIn("1.2.0", r.stdout)
        # respaldo creado con lo que el usuario cambió
        backups = list((self.dest / ".seo-skills-backups").glob("*"))
        self.assertEqual(len(backups), 1)
        self.assertIn("# nota mía", (backups[0] / "brief-de-contenido" / "SKILL.md").read_text())
        self.assertTrue((backups[0] / "plan-seo" / "MI-ARCHIVO.txt").exists())
        # la skill vuelve a la versión oficial
        self.assertNotIn("# nota mía", skill.read_text())
        # se conserva lo del usuario
        self.assertEqual(env_file.read_text(), "SERPAPI_API_KEY=abc\n")
        self.assertTrue((audit / "issues.json").exists())
        self.assertTrue((propia / "SKILL.md").exists())

    def test_instalacion_via_pipe_con_tarball(self):
        pkg = self.tmp / "pkg"
        raiz = pkg / "SEO-Skills-main"
        shutil.copytree(ROOT / "skills", raiz / "skills", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "agents", raiz / "agents")
        shutil.copy(ROOT / "VERSION", raiz / "VERSION")
        tgz = pkg / "pkg.tgz"
        with tarfile.open(tgz, "w:gz") as tf:
            tf.add(raiz, arcname="SEO-Skills-main")
        cwd = self.tmp / "otra-carpeta"
        cwd.mkdir()
        with open(INSTALL, "rb") as fh:
            r = subprocess.run(["bash", "-s", "--", "--dir", str(self.dest)], stdin=fh, capture_output=True, text=True,
                               cwd=cwd, timeout=120, env=dict(os.environ, SEO_SKILLS_TARBALL_URL=f"file://{tgz}"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.dest / "skills" / "aprendoclub" / "SKILL.md").exists())

    def test_check_sin_red_no_falla(self):
        self.instalar()
        r = sh([str(INSTALL), "--dir", str(self.dest), "--check"], env=NO_NET, stdin=subprocess.DEVNULL)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Instalada:", r.stdout)

    def test_ayuda_y_flag_invalido(self):
        self.assertEqual(sh([str(INSTALL), "--help"]).returncode, 0)
        self.assertEqual(sh([str(INSTALL), "--nope"]).returncode, 1)
        self.assertEqual(sh([str(INSTALL), "--client", "raro", "--dir", str(self.dest)]).returncode, 0)  # --dir manda

    def test_cliente_desconocido_falla(self):
        r = sh([str(INSTALL), "--client", "raro"], cwd=self.tmp, stdin=subprocess.DEVNULL,
               env={"HOME": str(self.tmp)})
        self.assertEqual(r.returncode, 1)

    def test_otros_clientes_instalan_solo_skills(self):
        r = sh([str(INSTALL), "--client", "cursor"], cwd=self.tmp, stdin=subprocess.DEVNULL)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.tmp / ".cursor" / "skills" / "aprendoclub" / "SKILL.md").exists())
        self.assertFalse((self.tmp / ".cursor" / "agents").exists())


class Desinstalador(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.dest = self.tmp / "destino"
        sh([str(INSTALL), "--dir", str(self.dest)], stdin=subprocess.DEVNULL)
        propia = self.dest / "skills" / "mi-skill-propia"
        propia.mkdir()
        (propia / "SKILL.md").write_text("x")

    def test_simulacro_no_borra(self):
        r = sh([str(UNINSTALL), "--dir", str(self.dest), "--dry-run"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.dest / "skills" / "aprendoclub").exists())

    def test_borra_solo_lo_instalado(self):
        r = sh([str(UNINSTALL), "--dir", str(self.dest)])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dest / "skills" / "aprendoclub").exists())
        self.assertFalse((self.dest / "agents").exists())
        self.assertTrue((self.dest / "skills" / "mi-skill-propia" / "SKILL.md").exists())


class PublicarVersion(unittest.TestCase):
    def test_sube_version_genera_anuncio_y_no_toca_git(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        for f in ("VERSION", "CHANGELOG.md"):
            shutil.copy(ROOT / f, tmp / f)
        shutil.copytree(ROOT / ".claude-plugin", tmp / ".claude-plugin")
        shutil.copytree(ROOT / "docs", tmp / "docs")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "publicar_version.py"), "--version", "9.9.9",
                            "--root", str(tmp)], capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((tmp / "VERSION").read_text().strip(), "9.9.9")
        self.assertIn('"version": "9.9.9"', (tmp / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn('"version": "9.9.9"', (tmp / ".claude-plugin" / "marketplace.json").read_text())
        self.assertIn("## [9.9.9]", (tmp / "CHANGELOG.md").read_text())
        anuncio = (tmp / "docs" / "ANUNCIO-ACTUALIZACION.md").read_text()
        for texto in ("install.sh | bash", "install.ps1 | iex", "/plugin update seo-skills@aprendoseo", "/aprendoclub update --check"):
            self.assertIn(texto, anuncio)
        self.assertNotIn("—", anuncio)
        self.assertFalse((tmp / ".git").exists())
        self.assertIn("no los hice yo", r.stdout)

    def test_rechaza_version_menor(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "publicar_version.py"), "--version", "0.0.1",
                            "--dry-run"], capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
