"""Diagrama del HMM: el índice temporal no es una etiqueta de régimen."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1]
def draw():
 fig,ax=plt.subplots(figsize=(8,3));ax.set(xlim=(-.8,5.7),ylim=(-.6,2.5));ax.axis('off')
 for x,t in [(0,'1'),(2,'2'),(4,'3')]:
  for y,label,color in [(1.7,f'S{t} (latente)','#203a5e'),(0,f'O{t} (señal)','#08628b')]:
   ax.add_patch(FancyBboxPatch((x-.7,y-.28),1.4,.56,boxstyle='round,pad=0.05',facecolor=color,edgecolor=color));ax.text(x,y,label,color='white',ha='center',va='center',fontsize=11)
  ax.annotate('',xy=(x,.34),xytext=(x,1.35),arrowprops=dict(arrowstyle='->',lw=2,color='#08628b'));ax.text(x+.12,.8,'B',fontsize=12,color='#08628b')
  if x<4:
   ax.annotate('',xy=(x+1.2,1.7),xytext=(x+.8,1.7),arrowprops=dict(arrowstyle='->',lw=2,color='#203a5e'));ax.text(x+1,2.05,'A',ha='center',color='#203a5e',fontsize=12)
 ax.text(5,1.7,'…',fontsize=24);ax.text(5,0,'…',fontsize=24);ax.text(2,2.4,'Evolución temporal: cada Sₜ puede ser avance, fricción o riesgo',ha='center',fontsize=10)
 fig.tight_layout();fig.savefig(ROOT/'figuras/estructura.png',dpi=300);plt.close(fig)
if __name__=='__main__':draw()
