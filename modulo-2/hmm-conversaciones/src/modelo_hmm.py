"""HMM categórico fila-estocástico. Sin entrenamiento ni datos personales."""
import numpy as np

class HMM:
    def __init__(self, A, B, pi):
        self.A, self.B, self.pi = [np.asarray(x, dtype=float) for x in (A,B,pi)]
        n = len(self.pi)
        if self.pi.ndim != 1 or self.A.shape != (n,n) or self.B.ndim != 2 or self.B.shape[0] != n or self.B.shape[1] < 1:
            raise ValueError('Dimensiones incompatibles')
        for x in (self.A,self.B,self.pi):
            if not np.all(np.isfinite(x)) or np.any(x<0) or np.any(x>1) or not np.allclose(x.sum(axis=-1),1,atol=1e-10,rtol=0):
                raise ValueError('Probabilidades no válidas: cada fila debe sumar 1')

    def observations(self, obs):
        o=np.asarray(obs)
        if o.ndim != 1 or len(o)==0 or not np.issubdtype(o.dtype,np.integer) or np.any(o<0) or np.any(o>=self.B.shape[1]):
            raise ValueError('Secuencia no vacía de símbolos enteros requeridos')
        return o

    def forward(self, obs):
        """Devuelve log P(O) y P(S_t | O_1:t); escalado evita subdesbordamiento."""
        o=self.observations(obs); f=np.zeros((len(o),len(self.pi))); ll=0.
        for t,v in enumerate(o):
            a=(self.pi if t==0 else f[t-1]@self.A)*self.B[:,v]
            c=a.sum()
            if c==0: return -np.inf, f
            f[t]=a/c;ll+=np.log(c)
        return float(ll),f

    def viterbi(self, obs):
        """MAP de trayectoria completa; NO es pronóstico ni posterior marginal."""
        o=self.observations(obs)
        with np.errstate(divide='ignore'):
            la,lb,lp=np.log(self.A),np.log(self.B),np.log(self.pi)
        d=lp+lb[:,o[0]]; back=np.zeros((len(o),len(lp)),dtype=int)
        for t,v in enumerate(o[1:],1):
            scores=d[:,None]+la;back[t]=scores.argmax(axis=0);d=scores.max(axis=0)+lb[:,v]
        if np.all(np.isneginf(d)): raise ValueError('Secuencia imposible bajo el modelo')
        path=np.zeros(len(o),dtype=int);path[-1]=d.argmax()
        for t in range(len(o)-2,-1,-1): path[t]=back[t+1,path[t+1]]
        return path,float(d.max())

class LCG:
    """LCG32 idéntico a JS: x=(1664525*x+1013904223) mod 2^32."""
    def __init__(self,seed): self.state=int(seed)&0xffffffff
    def random(self):
        self.state=(1664525*self.state+1013904223)&0xffffffff
        return self.state/4294967296
    def categorical(self,p):
        u=self.random();c=0.
        for i,v in enumerate(p):
            c+=v
            if u<c:return i
        return len(p)-1

def simulate(model,length,seed):
    if not isinstance(length,int) or length<1: raise ValueError('Longitud positiva requerida')
    rng=LCG(seed);s=[];o=[]
    for t in range(length):
        s.append(rng.categorical(model.pi if t==0 else model.A[s[-1]]))
        o.append(rng.categorical(model.B[s[-1]]))
    return np.array(s),np.array(o)
