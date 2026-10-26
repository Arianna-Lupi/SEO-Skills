"""Pruebas de estructura (solo stdlib + PyYAML opcional): el repo debe mantenerse coherente."""
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent


class EstructuraSkills(unittest.TestCase):
    def test_validador_sin_errores(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/validar_skills.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_todos_los_scripts_tienen_help(self):
        fallos = []
        for p in sorted(ROOT.glob("skills/*/scripts/*.py")):
            if p.name.startswith("_"):
                continue
            r = subprocess.run([sys.executable, str(p), "--help"], capture_output=True, text=True, timeout=30)
            if r.returncode != 0 or not r.stdout.strip():
                fallos.append(p.name)
        self.assertEqual(fallos, [], f"scripts sin --help funcional: {fallos}")


if __name__ == "__main__":
    unittest.main()
