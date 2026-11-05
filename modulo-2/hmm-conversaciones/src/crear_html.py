"""Regenera las páginas internas del informe desde articulo/contenido.json.
Conserva portada, barra de navegación y encabezado del HTML existente.
"""
import json,html,re
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
if __name__=='__main__':
 p=R/'index.html';s=p.read_text();pages=json.loads((R/'articulo/contenido.json').read_text());start=s.index('<section class="page" id="resumen">');end=s.index('</main>',start)
 body=''.join(f'<section class="page" id="{q["id"]}"><div class="kicker">Simulación · Modelo sintético · Sara Colorado Gil</div><h2>{q["title"]}</h2>'+''.join(render(b) for b in q['blocks'])+f'<div class="footer"><span>IU DIGITAL | ACTIVIDAD 2-M2</span><span>{i+2}</span></div></section>' for i,q in enumerate(pages));p.write_text(s[:start]+body+s[end:])
