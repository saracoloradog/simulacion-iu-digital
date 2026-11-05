"""Genera el informe completo desde contenido.json y metadatos.json."""
import json,html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def render(b):
 t=b['type']
 if t in ['p','h3']:return f'<{t}>{b["text"]}</{t}>'
 if t in ['formula','pre']:
  tag='pre' if t=='pre' else 'div'
  return f'<{tag} class="{t}">{html.escape(b["text"])}</{tag}>'
 if t=='fig':return f'<figure><img src="figuras/{b["file"]}" alt="{b["caption"]}"><figcaption class="note">{b["caption"]}</figcaption></figure>'
 if t=='table':return '<div class="table-wrap"><table><caption>'+b['caption']+'</caption><thead><tr>'+''.join('<th>'+h+'</th>' for h in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in r)+'</tr>' for r in b['rows'])+'</tbody></table></div>'
def main():
 pages=json.loads((R/'articulo/contenido.json').read_text());m=json.loads((R/'articulo/metadatos.json').read_text())
 nav='<div class="toolbar"><span>IU DIGITAL · SIMULACIÓN · MÓDULO 2</span><nav><a href="demo.html">Simulador</a><a href="laboratorio.html">Laboratorio HMM</a><a href="articulo/articulo.pdf">Artículo PDF</a><button onclick="window.print()">Imprimir</button></nav></div>'
 toc='<aside><strong>CONTENIDO</strong><a href="#portada">Portada</a>'+''.join(f'<a href="#{p["id"]}">{p["title"]}</a>' for p in pages)+'</aside>'
 cover=f'''<section class="page" id="portada"><div class="cover"><div class="brand">IU DIGITAL</div><div>INSTITUCIÓN UNIVERSITARIA DIGITAL DE ANTIOQUIA</div><div class="divider"></div><h1>{m['title'].upper()}<br><small>{m['subtitle']}</small></h1><p>{m['activity']}</p><div class="gap"></div><p><b>{m['author']}</b></p><p>{m['program']}<br>Asignatura: {m['course']}<br>Docente: {m['teacher']}</p><div class="gap"></div><p>Medellín, Antioquia · {m['date']}</p><p class="note">Actividad de simulación con datos sintéticos</p></div><div class="footer"><span>SIMULACIÓN | ACTIVIDAD 2-M2</span><span>1</span></div></section>'''
 body='\n'.join(f'<section class="page" id="{p["id"]}"><div class="kicker">Simulación · Sara Colorado Gil</div><h2>{p["title"]}</h2>'+''.join(render(b) for b in p['blocks'])+f'<div class="footer"><span>IU DIGITAL | ACTIVIDAD 2-M2</span><span>{i+2}</span></div></section>' for i,p in enumerate(pages))
 (R/'index.html').write_text('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+m['title']+' | IU Digital</title><link rel="stylesheet" href="style.css?v=editorial-3"></head><body>'+nav+'<div class="layout">'+toc+'<main class="pages">'+cover+body+'</main></div></body></html>')
if __name__=='__main__':main()
