"""Genera PDF y fuente LaTeX del mismo contenido usado en el informe HTML."""
from pathlib import Path
import json,re,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
ROOT=Path(__file__).resolve().parents[1]
FONT=Path(matplotlib.get_data_path())/'fonts/ttf'
for name,f in [('DV','DejaVuSans.ttf'),('DV-B','DejaVuSans-Bold.ttf'),('DV-I','DejaVuSans-Oblique.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/f)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-B',italic='DV-I',boldItalic='DV-B')
C=colors.HexColor('#203a5e');styles={
'p':ParagraphStyle('p',fontName='DV',fontSize=9.2,leading=14.1,spaceAfter=9,textColor=colors.HexColor('#26303d')),
'h2':ParagraphStyle('h2',fontName='DV-B',fontSize=16,leading=21,textColor=C,spaceAfter=18),
'h3':ParagraphStyle('h3',fontName='DV-B',fontSize=10.2,leading=15,textColor=colors.HexColor('#08628b'),spaceBefore=8,spaceAfter=7,keepWithNext=True),
'small':ParagraphStyle('small',fontName='DV',fontSize=7.4,leading=11,spaceAfter=8),
'formula':ParagraphStyle('formula',fontName='DV',fontSize=9,leading=17,spaceBefore=8,spaceAfter=13,backColor=colors.HexColor('#f0f5f9'),borderPadding=8),
'cover':ParagraphStyle('cover',fontName='DV-B',fontSize=21,leading=32,textColor=C,alignment=1,spaceAfter=25),
'center':ParagraphStyle('center',fontName='DV',fontSize=11,leading=20,alignment=1,spaceAfter=16)}
def clean(s):
 s=re.sub(r'<a href="(?!https?://)([^"]+)">',lambda m:'<a href="https://saracoloradog.github.io/simulacion-iu-digital/modulo-2/hmm-conversaciones/'+m.group(1)+'">',s)
 s=re.sub(r'<a href="([^"]+)">',r'<link href="\1" color="#08628b">',s).replace('</a>','</link>')
 return s.replace('−','-').replace('–','-').replace('—','-')
def para(s,sty='p'):return Paragraph(clean(s),styles[sty])
def foot(c,d):
 w,h=d.pagesize;c.setFillColor(C);c.rect(0,h-10,w,10,fill=1,stroke=0);c.setFillColor(colors.HexColor('#c82332'));c.rect(w*.75,h-10,w*.15,10,fill=1,stroke=0);c.setFillColor(colors.HexColor('#f5bf19'));c.rect(w*.9,h-10,w*.1,10,fill=1,stroke=0);c.setFillColor(C);c.setFont('DV',7);c.drawString(48,27,'IU DIGITAL · SIMULACIÓN · SARA COLORADO GIL · 2026');c.drawRightString(w-48,27,str(d.page))
def main():
 pages=json.loads((ROOT/'articulo/contenido.json').read_text());story=[]
 story += [Spacer(1,55),para('IU DIGITAL','cover'),para('INSTITUCIÓN UNIVERSITARIA DIGITAL DE ANTIOQUIA','center'),Spacer(1,32),para('Estados conversacionales latentes y riesgo de abandono','cover'),para('Un banco de simulación con Modelos Ocultos de Markov','center'),Spacer(1,35),para('Actividad didáctica 2 · Módulo 2','center'),para('<b>Sara Colorado Gil</b>','center'),para('Ingeniería de Software y Datos<br/>Asignatura: Simulación<br/>Docente: Julián Andrés Loaiza López','center'),Spacer(1,35),para('Medellín, Antioquia<br/>Noviembre de 2026','center'),para('Investigación computacional con datos sintéticos','center'),PageBreak()]
 for idx,p in enumerate(pages):
  story.append(para(p['title'],'h2'))
  for b in p['blocks']:
   t=b['type']
   if t in ['p','h3']:story.append(para(b['text'],t))
   elif t in ['formula','pre']:
    story.append(para(html.escape(b['text']).replace('\n','<br/>'),'formula'))
   elif t=='fig':
    im=Image(str(ROOT/'figuras'/b['file']));scale=480/im.imageWidth;im.drawWidth=480;im.drawHeight=im.imageHeight*scale
    story.append(KeepTogether([im,Spacer(1,5),para(b['caption'],'small')]))
   elif t=='table':
    rows=[[para(str(v),'small') for v in b['headers']]]+[[para(str(v),'small') for v in r] for r in b['rows']]
    n=len(b['headers']);w=[480/n]*n
    if n==3:w=[65,180,235]
    if n==2:w=[135,345]
    tb=Table(rows,colWidths=w,repeatRows=1,hAlign='LEFT');tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5edf5')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cbd8e3')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8fb')])]))
    story.extend([para(b['caption'],'h3'),tb,Spacer(1,9)])
  if idx<len(pages)-1:story.append(PageBreak())
 doc=SimpleDocTemplate(str(ROOT/'articulo/articulo.pdf'),pagesize=(595.28,841.89),rightMargin=55,leftMargin=55,topMargin=48,bottomMargin=48,title='Estados conversacionales latentes y riesgo de abandono',author='Sara Colorado Gil')
 doc.build(story,onFirstPage=foot,onLaterPages=foot)
 # LaTeX/Overleaf source: same blocks and numeric tables, compile with XeLaTeX.
 def tex(s):
  s=re.sub(r'<a href="[^"]+">(.*?)</a>',r'\1',s);s=re.sub('<[^>]+>','',s);s=html.unescape(s)
  mapping={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
  return ''.join(mapping.get(c,c) for c in s)
 equations=[r'\lambda=(S,V,A,B,\pi),\quad A_{ij}=P(S_{t+1}=j\mid S_t=i),\quad B_{jk}=P(O_t=k\mid S_t=j)',r'P(S_{t+1}\mid S_{1:t})=P(S_{t+1}\mid S_t),\quad P(O_t\mid S_{1:t},O_{1:t-1})=P(O_t\mid S_t)',r'P(s_{1:T},o_{1:T})=\pi_{s_1}B_{s_1,o_1}\prod_{u=2}^T A_{s_{u-1},s_u}B_{s_u,o_u}']
 out=[r'\documentclass[10pt,a4paper]{article}',r'\usepackage[margin=23mm]{geometry}',r'\usepackage{fontspec}\setmainfont{DejaVu Serif}',r'\usepackage[spanish]{babel}\usepackage{amsmath,graphicx,longtable,booktabs,hyperref,xcolor}',r'\definecolor{institucional}{HTML}{203A5E}\hypersetup{colorlinks=true,urlcolor=institucional}',r'\title{Estados conversacionales latentes y riesgo de abandono: un banco de simulación con HMM}',r'\author{Sara Colorado Gil\\IU Digital de Antioquia\\Ingeniería de Software y Datos\\Simulación · Actividad didáctica 2 · Módulo 2\\Docente: Julián Andrés Loaiza López}',r'\date{Noviembre de 2026}\begin{document}\maketitle\newpage']
 for p in pages:
  out.append(r'\section*{'+tex(p['title'])+'}')
  for b in p['blocks']:
   t=b['type']
   if t=='h3':out.append(r'\subsection*{'+tex(b['text'])+'}')
   elif t=='p':out.append(tex(b['text'])+'\n\n')
   elif t=='formula':
    text=b['text']
    if text.startswith('λ='):out.append(r'\['+equations[0]+r'\]')
    elif text.startswith('P(Sₜ₊₁'):out.append(r'\['+equations[1]+r'\]')
    elif text.startswith('P(s₁:'):out.append(r'\['+equations[2]+r'\]')
    elif text.startswith('α₁'):out.append(r'\[\alpha_t(j)=\left[\sum_i f_{t-1}(i)A_{ij}\right]B_j(O_t),\quad c_t=\sum_j\alpha_t(j),\quad f_t=\alpha_t/c_t\]'+r'\[\log P(O)=\sum_t\log c_t\]')
    elif text.startswith('δ₁'):out.append(r'\[\delta_1(j)=\log\pi_j+\log B_j(O_1)\]'+r'\[\delta_t(j)=\max_i[\delta_{t-1}(i)+\log A_{ij}]+\log B_j(O_t)\]')
    elif text.startswith('IC95'):out.append(r'\[IC_{95\%}=\bar{x}\pm t_{0.975,n-1}\frac{s}{\sqrt{n}},\quad s^2=\frac{\sum_r(x_r-\bar{x})^2}{n-1}\]')
    else:out.append(r'\begin{center}'+tex(text).replace('\n',r'\\')+r'\end{center}')
   elif t=='pre':out.append(r'\begin{verbatim}'+'\n'+b['text']+'\n'+r'\end{verbatim}')
   elif t=='fig':out.append(r'\begin{figure}[ht]\centering\includegraphics[width=\linewidth]{../figuras/'+b['file']+r'}\caption{'+tex(b['caption'])+r'}\end{figure}')
   elif t=='table':
    n=len(b['headers']);cols=''.join('p{'+str(round(.93/n,3))+r'\linewidth}' for _ in range(n))
    out.append(r'{\small\begin{longtable}{'+cols+r'}\caption{'+tex(b['caption'])+r'}\\\toprule'+' & '.join(tex(str(v)) for v in b['headers'])+r'\\\midrule\endfirsthead')
    out+=[' & '.join(tex(str(v)) for v in r)+r'\\' for r in b['rows']];out.append(r'\bottomrule\end{longtable}}')
  out.append(r'\clearpage')
 out.append(r'\end{document}');(ROOT/'articulo/articulo.tex').write_text('\n'.join(out))
 print('PDF y fuente LaTeX generados')
if __name__=='__main__':main()
