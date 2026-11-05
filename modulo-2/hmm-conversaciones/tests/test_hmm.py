import unittest,itertools,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from modelo_hmm import HMM,simulate,LCG
from simulador import load_models
class TestHMM(unittest.TestCase):
 def setUp(self):self.m=HMM([[.7,.3],[.4,.6]],[[.5,.5],[.1,.9]],[.6,.4])
 def test_exhaustive(self):
  for o in itertools.product(range(2),repeat=4):
   paths=list(itertools.product(range(2),repeat=4));p=[]
   for s in paths:
    q=self.m.pi[s[0]]*self.m.B[s[0],o[0]]
    for t in range(1,4):q*=self.m.A[s[t-1],s[t]]*self.m.B[s[t],o[t]]
    p.append(q)
   ll,f=self.m.forward(o);v,score=self.m.viterbi(o)
   self.assertAlmostEqual(np.exp(ll),sum(p),14)
   self.assertAlmostEqual(np.exp(score),max(p),14)
   np.testing.assert_allclose(f.sum(axis=1),1)
 def test_validation(self):
  for a,b,p in [([[1,-.1],[0,1]],[[1],[1]],[1,0]),([[1,0],[0,1]],[[1],[1]],[.2,.2]),([[1,0],[0,1]],[[float('nan')],[1]],[1,0])]:
   with self.assertRaises(ValueError):HMM(a,b,p)
 def test_observations(self):
  for o in [[],[-1],[2],[.5]]:
   with self.assertRaises(ValueError):self.m.forward(o)
 def test_zero(self):
  m=HMM([[1]],[[1,0]],[1]);self.assertEqual(m.forward([1])[0],-np.inf)
  with self.assertRaises(ValueError):m.viterbi([1])
 def test_long(self):self.assertTrue(np.isfinite(self.m.forward([1]*10000)[0]))
 def test_repeat(self):
  m=load_models()['B'];a,b=simulate(m,100,42);c,d=simulate(m,100,42)
  np.testing.assert_array_equal(a,c);np.testing.assert_array_equal(b,d)
 def test_deterministic(self):
  m=HMM([[0,1],[1,0]],[[1,0],[0,1]],[1,0]);s,o=simulate(m,6,12)
  np.testing.assert_array_equal(s,[0,1,0,1,0,1]);np.testing.assert_array_equal(m.viterbi(o)[0],s)
 def test_rng(self):self.assertEqual(LCG(42).random(),1083814273/4294967296)
if __name__=='__main__':unittest.main()
