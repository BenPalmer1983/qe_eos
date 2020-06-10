import numpy
from numpy import random

class eos_fit:

  @staticmethod
  def run(V, E):
  
    #  p[0] = V0
    #  p[1] = E0
    #  p[2] = B0
    #  p[3] = B0P
  
    random.seed(1)
  
    p = numpy.zeros((4))
    
    # 2nd order polynomial fit
    poly = numpy.polyfit(V, E, 2)
    
    # Starting points
    p[0] = (-1 * poly[1]) / (2 * poly[0])
    p[1] = (poly[0] * p[0] * p[0]) + (poly[1] * p[0]) + poly[2]
    p[2] = 2.0 * poly[0] * p[0]
    p[3] = 2.0
    
    # rss
    rss = eos_fit.rss(p, V, E)
    
    p = eos_fit.random_search_b0p(p, V, E)
    rss = eos_fit.rss(p, V, E)
    
    p = eos_fit.random_search(p, V, E)
    rss = eos_fit.rss(p, V, E)
    
    # Return parameter
    return p
    
    
  @staticmethod
  def random_search_b0p(p, V, E):
    loops = 1000
    best_rss = eos_fit.rss(p, V, E)
    max_variance = 0.1
    s = random.uniform(-1,1,loops)
    for i in range(loops):
      p_test = numpy.copy(p)
      p_test[3] = p[3] + max_variance * (0.5 - s[i])
      rss = eos_fit.rss(p_test, V, E)
      if(rss < best_rss):
        p = numpy.copy(p_test)
        best_rss = rss
    return p
    
  @staticmethod
  def random_search(p, V, E):
    loops = 1000
    best_rss = eos_fit.rss(p, V, E)
    max_variance = 0.1
    s = random.uniform(-1,1,loops)
    for i in range(loops):
      for j in range(4):
        p_test = numpy.copy(p)
        p_test[j] = p[j] + max_variance * (0.5 - s[i])
        rss = eos_fit.rss(p_test, V, E)
        if(rss < best_rss):
          p = numpy.copy(p_test)
          best_rss = rss
    return p  
  
  @staticmethod
  def rss(p, V, E):
    return sum((eos_fit.bm_calc(V[:],p) - E[:])**2)
    
  @staticmethod
  def bm_calc(V, p):
    eta = (V/p[0])**(1/3.0)
    return p[1] + (9/16.0) * (p[2] * p[0]) * ((eta*eta - 1)*(eta*eta - 1)) * (6.0 + p[3] * (eta * eta - 1) - 4 * eta * eta )