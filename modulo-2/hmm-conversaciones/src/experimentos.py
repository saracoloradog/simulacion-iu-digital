"""Ejecutar desde el módulo: python src/experimentos.py. Regenera CSV y figuras."""
import json,sys,platform,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import t as student
from modelo_hmm import HMM,simulate
from simulador import ROOT,load_models
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':120,'savefig.dpi':300})
COLORS=['#08628b','#f5bf19','#c82332']
def metrics(s,v,f):
 risk=s==2;starts=np.flatnonzero(risk & np.r_[True,~risk[:-1]])
 ends=np.flatnonzero(risk & np.r_[~risk[1:],True]);dur=ends-starts+1
 tp=np.sum((v==2)&risk);fp=np.sum((v==2)&~risk);fn=np.sum((v!=2)&risk)
 return dict(p_s1=np.mean(s==0),p_s2=np.mean(s==1),p_s3=np.mean(risk),entradas=int(np.sum((s[1:]==2)&(s[:-1]!=2))),duracion_media=float(dur.mean()) if len(dur) else np.nan,exactitud=np.mean(s==v),precision_riesgo=tp/(tp+fp) if tp+fp else np.nan,recall_riesgo=tp/(tp+fn) if tp+fn else np.nan,brier_filtrado=np.mean((f[:,2]-risk)**2))
def summarize(df,group):
 rows=[]
 for key,g in df.groupby(group,sort=False):
  key=(key,) if not isinstance(key,tuple) else key
  for col in ['p_s1','p_s2','p_s3','entradas','duracion_media','exactitud','brier_filtrado']:
   x=g[col].dropna();n=len(x);mean=x.mean();sd=x.std(ddof=1);h=student.ppf(.975,n-1)*sd/np.sqrt(n) if n>1 else np.nan
   rows.append(dict(zip(group,key))|dict(metrica=col,n=n,media=mean,desviacion=sd,minimo=x.min(),maximo=x.max(),ic_inf=mean-h,ic_sup=mean+h))
 return pd.DataFrame(rows)
def main():
 models=load_models();seeds=np.random.SeedSequence(20261105).generate_state(1000).tolist();rows=[];conf={k:np.zeros((3,3),int) for k in models};reference=[]
 for k,m in models.items():
  for rep,seed in enumerate(seeds):
   s,o=simulate(m,100,seed);v,score=m.viterbi(o);ll,f=m.forward(o)
   rows.append(dict(escenario=k,replica=rep,semilla=seed,longitud=100,log_verosimilitud=ll,**metrics(s,v,f)))
   np.add.at(conf[k],(s,v),1)
   if rep==0: reference.append(dict(escenario=k,semilla=seed,s=s.tolist(),o=o.tolist(),v=v.tolist(),logp=ll,logv=score,filtrado=f.tolist()))
 df=pd.DataFrame(rows);df.to_csv(ROOT/'resultados/replicas.csv',index=False);summary=summarize(df,['escenario']);summary.to_csv(ROOT/'resultados/resumen.csv',index=False)
 (ROOT/'resultados/referencia.json').write_text(json.dumps(reference,indent=2))
 for k,c in conf.items():pd.DataFrame(c,index=['S1','S2','S3'],columns=['S1','S2','S3']).to_csv(ROOT/f'resultados/confusion_{k}.csv')
 sens=[]
 # Emisiones: mezcla convexa con uniforme. Inicial: riesgo puro. Transición: interpolación A->B.
 for factor in ['emision','transicion','inicial']:
  for x in [0,.25,.5,.75,1]:
   base=models['A'];a=base.A.copy();b=base.B.copy();pi=base.pi.copy()
   if factor=='emision':b=(1-x)*b+x/5
   if factor=='transicion':a=(1-x)*a+x*models['B'].A
   if factor=='inicial':pi=(1-x)*pi+x*np.array([0,0,1])
   m=HMM(a,b,pi)
   for rep,seed in enumerate(seeds[:250]):
    s,o=simulate(m,100,seed);v,_=m.viterbi(o);_,f=m.forward(o)
    # Mismo generador y estimador congruente; contraste adicional con decodificador nominal.
    vn,_=base.viterbi(o)
    sens.append(dict(factor=factor,nivel=x,replica=rep,semilla=seed,exactitud_nominal=np.mean(s==vn),**metrics(s,v,f)))
 sdf=pd.DataFrame(sens);sdf.to_csv(ROOT/'resultados/sensibilidad_replicas.csv',index=False);ss=summarize(sdf,['factor','nivel']);ss.to_csv(ROOT/'resultados/sensibilidad.csv',index=False)
 fig,ax=plt.subplots(figsize=(7,4));bottom=np.zeros(3)
 for i,col in enumerate(['p_s1','p_s2','p_s3']):
  vals=[df[df.escenario==k][col].mean() for k in models];ax.bar(list(models),vals,bottom=bottom,label=['Avance','Fricción','Riesgo'][i],color=COLORS[i]);bottom+=vals
 ax.set(ylabel='Proporción media de turnos',xlabel='Escenario',ylim=(0,1));ax.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,1.18));fig.tight_layout();fig.savefig(ROOT/'figuras/ocupacion.png');plt.close(fig)
 fig,axes=plt.subplots(1,3,figsize=(10,3.5))
 for ax,(k,c) in zip(axes,conf.items()):
  norm=c/c.sum(axis=1,keepdims=True);ax.imshow(norm,vmin=0,vmax=1,cmap='Blues')
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{norm[i,j]:.1%}',ha='center',va='center',color='white' if norm[i,j]>.5 else '#203a5e')
  ax.set(title=f'Escenario {k}',xticks=range(3),xticklabels=['S1','S2','S3'],yticks=range(3),yticklabels=['S1','S2','S3'],xlabel='Viterbi',ylabel='Estado sintético')
 fig.tight_layout();fig.savefig(ROOT/'figuras/confusion.png');plt.close(fig)
 fig,axes=plt.subplots(1,3,figsize=(10,3.5))
 for ax,factor in zip(axes,['emision','transicion','inicial']):
  for metric,label,color in [('p_s3','Ocupación riesgo',COLORS[2]),('exactitud','Exactitud',COLORS[0])]:
   z=ss[(ss.factor==factor)&(ss.metrica==metric)];ax.plot(z.nivel,z.media,'o-',label=label,color=color);ax.fill_between(z.nivel,z.ic_inf,z.ic_sup,color=color,alpha=.12)
  ax.set(title=factor.capitalize(),xlabel='Intensidad de perturbación',ylim=(0,1))
 axes[0].legend(fontsize=8);fig.tight_layout();fig.savefig(ROOT/'figuras/sensibilidad.png');plt.close(fig)
 r=reference[1];fig,ax=plt.subplots(figsize=(9,3));ax.step(range(1,101),np.array(r['s'])+1,where='mid',label='Sintético',color=COLORS[0]);ax.plot(range(1,101),np.array(r['v'])+1,'.',label='Viterbi',color=COLORS[2]);ax.set(xlabel='Turno',ylabel='Estado',yticks=[1,2,3]);ax.legend();fig.tight_layout();fig.savefig(ROOT/'figuras/trayectoria.png');plt.close(fig)
 expected=[]
 for k,m in models.items():
  state=m.pi.copy();mean=np.zeros(3)
  for step in range(100):mean+=state/100;state=state@m.A
  for j in range(3):expected.append(dict(escenario=k,estado=j+1,ocupacion_esperada=mean[j],ocupacion_observada=df[df.escenario==k][f'p_s{j+1}'].mean()))
 pd.DataFrame(expected).to_csv(ROOT/'resultados/esperanza_exacta.csv',index=False)
 from diagrama import draw
 draw()
 manifest=dict(fecha='2026-11-05',python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,matplotlib=matplotlib.__version__,semilla_maestra=20261105,replicas=1000,longitud=100,replicas_sensibilidad=250,generador='LCG32 para muestreo; NumPy SeedSequence para semillas de réplicas',sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'resultados').glob('*.csv'))})
 (ROOT/'resultados/manifiesto.json').write_text(json.dumps(manifest,indent=2));print(summary[summary.metrica.isin(['p_s3','exactitud'])].to_string(index=False))
if __name__=='__main__':main()
