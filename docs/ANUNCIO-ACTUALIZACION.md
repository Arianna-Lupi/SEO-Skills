# Anuncio de actualización: SEO Skills 1.4.0

Texto listo para pegar en la comunidad. Revisa las viñetas antes de publicar.

---

Actualicé las SEO Skills a la versión 1.4.0.

**Qué hay de nuevo**

- Nuevo comando `/aprendoclub`: un solo punto de entrada. `/aprendoclub audit midominio.com` hace la auditoría completa paso a paso, con pausas para que confirmes, y termina siempre en el dashboard.
- Instalación mucho más rápida: dos comandos, sin preguntas y sin instalar nada extra. También puedes instalarlas como plugin de Claude Code.
- Actualizar es un solo paso: vuelve a correr el comando de instalación. Se conservan tus claves y tus carpetas `.seo-audit/`, y si habías cambiado una skill a mano, se guarda una copia antes.
- 10 skills nuevas: intención de búsqueda, actualización de contenido, calidad de contenido (E-E-A-T), sitemap y robots, imágenes, plan SEO, proyección con Search Console, SEO local, SEO de ecommerce y propuesta y reporte de servicios.
- Análisis de la competencia mejorado: ahora perfila las páginas del top de Google y las compara con la tuya, con un puntaje de costo de oportunidad y tareas listas para tu plan.
- Antes de usar un script, las skills revisan qué necesita (Python, paquetes, claves) y te preguntan antes de instalar algo o guardar una clave. Si dices que no, sigues en modo manual.

**Cómo actualizar (un solo paso)**

- macOS y Linux: pega esto en la terminal.

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
```

- Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex
```

- Si las instalaste como plugin de Claude Code:

```
/plugin update seo-skills@aprendoseo
```

Reinicia Claude Code cuando termine. Tus claves (`~/.claude/seo-skills.env`) y tus carpetas `.seo-audit/` no se tocan. Si habías modificado una skill a mano, el instalador guarda una copia antes de actualizar.

**Cómo ver si quedó bien**

Escribe `/aprendoclub update --check`. Te dice qué versión tienes y si estás al día.
