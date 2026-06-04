#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
build_dashboard.py — Genera el dashboard SEO local (HTML) a partir de los datos
estructurados que las skills/agentes dejan en .seo-audit/<sitio>/data/*.json.

Es el PASO DE CIERRE de cualquier flujo SEO: una sola página con todo lo encontrado
(issues, keywords, clusters, competidores, AI/GEO, auditorías, inventario, próximos
pasos). Funciona con los archivos que existan: las secciones sin datos se ocultan.

REGLA: el dashboard solo muestra lo que está en los JSON. Nunca inventa números;
los datos faltantes deben ir marcados como "pendiente" en su JSON (o en meta.pending_data).

Convención de carpeta (gitignored, datos del cliente):
  <repo>/.seo-audit/<sitio>/
    data/                      ← lo escriben las skills/agentes
      meta.json                (resumen global + summary + pending_data + data_sources)
      issues.json              ({issues:[{id,title,severity,block,fix,status,evidence,verified,github}], counts})
      keywords.json            ({candidates:[...], golden:[{kw,cluster,why}], note})
      clusters.json            ({clusters:[{pilar,url,spokes:[]}]})
      competitors.json         ({by_pillar:[{pillar,query,results:[{position,domain,title,url}]}], strategic:[]})
      ai-features.json         ({queries:[{query,ai_overview,featured_snippet,paa,recommendation}]})
      content-briefs.json      ({briefs:[{keyword,type,url,meta_title,angle,status}]})
      prior-audits.json        ({audits:[{name,score,date,summary,file}]})
      inventory-summary.json   ({total_urls,source,http_sample,note})
      next-steps.json          ({steps:[{prio,area,action,impact,effort}]})
    index.html                 ← lo genera este script

Uso:
  uv run build_dashboard.py --site juan-tech.com
  uv run build_dashboard.py --site juan-tech.com --serve --port 8787
  # o desde otra ruta de repo:
  uv run build_dashboard.py --site ejemplo.com --root /ruta/al/repo

Salida (JSON a stdout):
  {"ok": true, "dir": "...", "index": ".../index.html", "url": "http://127.0.0.1:8787/",
   "serve_cmd": "python3 -m http.server 8787 --directory ..."}

Deps: stdlib.
"""
import argparse
import json
import os
import sys

TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auditoría SEO</title>
<style>
  :root{--bg:#0b0f17;--panel:#131a26;--panel2:#0f1521;--line:#223049;--txt:#e6edf6;--mut:#8aa0bd;
    --acc:#4f9dff;--ok:#3fb950;--crit:#f85149;--high:#ff8c42;--med:#e3b341;--low:#58a6ff;--pend:#a371f7;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
  header{padding:28px 32px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,#0f1726,#0b0f17)}
  header h1{margin:0 0 4px;font-size:24px}
  header .sub{color:var(--mut);font-size:14px}
  .wrap{max-width:1180px;margin:0 auto;padding:24px 32px 80px}
  .grid{display:grid;gap:16px}
  .cards{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}
  .stat{text-align:center}.stat .n{font-size:30px;font-weight:700;line-height:1}
  .stat .l{color:var(--mut);font-size:12px;margin-top:6px;text-transform:uppercase;letter-spacing:.04em}
  section{margin-top:34px}
  section h2{font-size:18px;border-left:3px solid var(--acc);padding-left:10px;margin:0 0 14px}
  .pend-banner{background:rgba(163,113,247,.12);border:1px solid var(--pend);border-radius:10px;padding:12px 16px;color:#d2c2f5;font-size:14px}
  table{width:100%;border-collapse:collapse;font-size:14px;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
  th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
  th{background:var(--panel2);color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
  tr:last-child td{border-bottom:none}
  .pill{display:inline-block;padding:1px 9px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap}
  .Crítico{background:rgba(248,81,73,.18);color:var(--crit)}
  .Alto{background:rgba(255,140,66,.18);color:var(--high)}
  .Medio,.Bajo-Medio{background:rgba(227,179,65,.16);color:var(--med)}
  .Bajo{background:rgba(88,166,255,.16);color:var(--low)}
  .pend{color:var(--pend);font-style:italic}
  .tag{display:inline-block;background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:1px 7px;font-size:12px;color:var(--mut);margin:2px 3px 2px 0}
  .gold{background:rgba(227,179,65,.12);border-color:var(--med);color:#f0d98a}
  .muted{color:var(--mut)}.src{font-size:12px;color:var(--mut);margin-top:4px}
  .chk{color:var(--ok)}.warn{color:var(--med)}.no{color:var(--crit)}
  code{background:var(--panel2);padding:1px 5px;border-radius:5px;font-size:13px}
  .foot{margin-top:50px;color:var(--mut);font-size:12px;border-top:1px solid var(--line);padding-top:16px}
  .empty{color:var(--mut);font-size:13px}
</style>
</head>
<body>
<header><h1>Auditoría SEO — <span id="site"></span></h1><div class="sub" id="subhead"></div></header>
<div class="wrap" id="app">Cargando…</div>
<script>
const J={};const FILES=["meta","issues","prior-audits","keywords","clusters","competitors","ai-features","content-briefs","inventory-summary","next-steps"];
const $=(h)=>{const t=document.createElement('template');t.innerHTML=h.trim();return t.content.firstChild};
const esc=(s)=>String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
async function boot(){
  await Promise.all(FILES.map(async f=>{try{const r=await fetch(`data/${f}.json`);J[f]=r.ok?await r.json():{}}catch(e){J[f]={}}}));
  const m=J["meta"]||{},s=m.summary||{};
  document.getElementById('site').textContent=m.site||'(sitio)';
  document.title='Auditoría SEO — '+(m.site||'');
  document.getElementById('subhead').innerHTML=[m.stack,m.market,m.repo?('repo <code>'+esc(m.repo)+'</code>'):'',m.generated?('generado '+esc(m.generated)):''].filter(Boolean).map(x=>typeof x==='string'&&x.includes('<code')?x:esc(x)).join(' · ');
  const app=document.getElementById('app');app.innerHTML='';
  if(s&&Object.keys(s).length){
    const labels=[["URLs","urls"],["Issues","issues_total"],["Críticos","issues_critical"],["Altos","issues_high"],["Keywords","keyword_candidates"],["10 de Oro","golden_keywords"],["Clusters","clusters"],["Auditorías","prior_audits"]];
    const cg=$(`<section><div class="grid cards"></div></section>`);
    labels.forEach(([l,k])=>{if(s[k]!=null)cg.firstChild.appendChild($(`<div class="card stat"><div class="n">${s[k]}</div><div class="l">${l}</div></div>`))});
    if(cg.firstChild.children.length)app.appendChild(cg);
  }
  if(m.pending_data&&m.pending_data.length)app.appendChild($(`<section><div class="pend-banner"><b>⏳ Datos pendientes (NO se inventan):</b> ${m.pending_data.map(esc).join(' · ')}</div></section>`));
  // issues
  rows(app,"🔧 Issues técnicos (por severidad)",["Sev","Issue","Bloque","Fix","Estado","Evidencia"],
    (J["issues"].issues||[]).map(i=>[`<span class="pill ${esc(i.severity)}">${esc(i.severity)}</span>`,
      `<b>${esc(i.title)}</b>${i.github?` <a href="https://github.com/${esc(m.repo)}/issues/${i.github}">#${i.github}</a>`:''}`,
      esc(i.block),esc(i.fix),
      `${esc(i.status)} ${i.verified===true?'<span class="chk">✓verif</span>':i.verified==='no confirmado'?'<span class="no">⚠ sin confirmar</span>':'<span class="warn">~</span>'}`,
      `<span class="src">${esc(i.evidence)}</span>`]),srcOf(J["issues"]));
  rows(app,"📋 Auditorías previas",["Auditoría","Score","Resumen","Archivo"],
    (J["prior-audits"].audits||[]).map(a=>[`<b>${esc(a.name)}</b>`,`<span class="tag">${esc(a.score)}</span>`,esc(a.summary),a.file?`<code>${esc(a.file)}</code>`:'']),srcOf(J["prior-audits"]));
  rows(app,"⭐ Las 10 de Oro",["Keyword","Cluster","Por qué"],
    (J["keywords"].golden||[]).map(g=>[`<span class="pill gold">${esc(g.kw)}</span>`,esc(g.cluster),esc(g.why)]),
    J["keywords"].note?`<div class="src">${esc(J["keywords"].note)}</div>`:'');
  // clusters
  if((J["clusters"].clusters||[]).length){const cl=$(`<section><h2>🗂️ Topic Clusters (pilar → spokes)</h2></section>`);
    J["clusters"].clusters.forEach(c=>cl.appendChild($(`<div class="card" style="margin-bottom:10px"><b>${esc(c.pilar)}</b> ${c.url?`<code>${esc(c.url)}</code>`:''}<div>${(c.spokes||[]).map(x=>`<span class="tag">${esc(x)}</span>`).join('')}</div></div>`)));app.appendChild(cl);}
  rows(app,"🥊 Competidores en la SERP",["Pilar / query","Top dominios"],
    (J["competitors"].by_pillar||[]).map(p=>[`<b>${esc(p.pillar)}</b><div class="muted">${esc(p.query)}</div>`,
      (p.results||[]).slice(0,6).map(r=>`<span class="tag">#${r.position} ${esc(r.domain)}</span>`).join('')]),
    (J["competitors"].strategic||[]).length?`<div class="src">Estratégicos: ${J["competitors"].strategic.map(c=>esc(c.name)+' ('+esc(c.url)+')').join(' · ')}</div>`:'');
  rows(app,"🤖 Búsqueda con IA (GEO/AEO)",["Query","AI Overview","Featured","PAA","Recomendación"],
    (J["ai-features"].queries||[]).map(q=>[`<code>${esc(q.query)}</code>`,q.ai_overview?'<span class="chk">Sí</span>':'<span class="muted">No</span>',
      (q.featured_snippet&&q.featured_snippet.present)?'Sí':'<span class="muted">No</span>',String((q.paa||[]).length),esc(q.recommendation)]),srcOf(J["ai-features"]));
  rows(app,"✍️ Briefs / Contenido",["Keyword","Tipo","Meta título","Ángulo","Estado"],
    (J["content-briefs"].briefs||[]).map(b=>[`<b>${esc(b.keyword)}</b> ${b.url?`<code>${esc(b.url)}</code>`:''}`,esc(b.type),esc(b.meta_title),esc(b.angle),`<span class="chk">${esc(b.status)}</span>`]));
  // inventory
  const iv=J["inventory-summary"]||{};
  if(iv.total_urls!=null||iv.http_sample){const s2=$(`<section><h2>🗺️ Inventario y rastreabilidad</h2></section>`);
    s2.appendChild($(`<div class="card"><b>${iv.total_urls??'—'} URLs</b> ${iv.source?`vía <code>${esc(iv.source)}</code>`:''}. ${iv.http_sample?('HTTP live: '+esc(JSON.stringify(iv.http_sample))):''}<div class="src">${esc(iv.note||'')}</div></div>`));app.appendChild(s2);}
  rows(app,"🚀 Próximos pasos (priorizado)",["#","Área","Acción","Impacto","Esfuerzo"],
    (J["next-steps"].steps||[]).map(st=>[`<b>${esc(st.prio)}</b>`,esc(st.area),esc(st.action),esc(st.impact),esc(st.effort)]));
  if(m.data_sources&&m.data_sources.length)app.appendChild($(`<div class="foot">Fuentes: ${m.data_sources.map(esc).join(' · ')}<br>Datos estructurados en <code>data/*.json</code> · regla activa: <b>cero números inventados</b>.</div>`));
  if(!app.children.length)app.appendChild($(`<div class="empty">No hay datos todavía. Corre las skills/agentes para llenar <code>data/*.json</code> y recarga.</div>`));
}
function rows(app,title,head,body,extra){if(!body||!body.length)return;
  const t=$(`<table><thead><tr>${head.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody></tbody></table>`);
  const tb=t.querySelector('tbody');body.forEach(r=>tb.appendChild($(`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`)));
  const s=$(`<section><h2>${title}</h2></section>`);s.appendChild(t);if(extra)s.appendChild($(`<div>${extra}</div>`));app.appendChild(s);}
function srcOf(o){return (o&&o.source)?`<div class="src">Fuente: ${esc(o.source)}</div>`:''}
boot();
</script>
</body>
</html>
"""


def find_root(start):
    """Sube buscando un .git para anclar el repo; si no, usa cwd."""
    d = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.abspath(start)
        d = parent


def main():
    ap = argparse.ArgumentParser(
        description="Genera (y opcionalmente sirve) el dashboard SEO local.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run build_dashboard.py --site juan-tech.com --serve',
    )
    ap.add_argument("--site", required=True, help="Dominio del proyecto, p.ej. ejemplo.com")
    ap.add_argument("--root", help="Raíz del repo/proyecto (default: detecta .git o usa cwd)")
    ap.add_argument("--serve", action="store_true", help="Sirve el dashboard (bloquea; Ctrl+C para parar)")
    ap.add_argument("--port", type=int, default=8787, help="Puerto para --serve (default 8787)")
    args = ap.parse_args()

    root = args.root or find_root(os.getcwd())
    outdir = os.path.join(root, ".seo-audit", args.site)
    datadir = os.path.join(outdir, "data")
    os.makedirs(datadir, exist_ok=True)

    index = os.path.join(outdir, "index.html")
    with open(index, "w", encoding="utf-8") as f:
        f.write(TEMPLATE)

    data_files = sorted(
        os.path.basename(p) for p in os.listdir(datadir)
    ) if os.path.isdir(datadir) else []
    url = f"http://127.0.0.1:{args.port}/"
    serve_cmd = f"python3 -m http.server {args.port} --bind 127.0.0.1 --directory {outdir}"

    result = {
        "ok": True, "site": args.site, "dir": outdir, "index": index,
        "data_files": data_files, "url": url, "serve_cmd": serve_cmd,
    }
    print(json.dumps(result, ensure_ascii=False))

    if args.serve:
        import http.server
        import socketserver
        os.chdir(outdir)
        with socketserver.TCPServer(("127.0.0.1", args.port), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"Sirviendo en {url}  (Ctrl+C para parar)", file=sys.stderr)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
