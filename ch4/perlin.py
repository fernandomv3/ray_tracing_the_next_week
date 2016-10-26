from vec3 import Vec3
from random import random
from math import floor

def permute(p,n):
  for i in range(n-1,0,-1):
    target = int(random()*(i+1))
    p[i],p[target] = p[target],p[i]

class Perlin:
  @staticmethod
  def perlin_generate():
    p = []
    for i in range(0,256):
      p.append(random())
    return p

  @staticmethod
  def perlin_generate_perm():
    p = []
    for i in range(0,256):
      p.append(i)
    permute(p,256)
    return p

  ranfloat = perlin_generate.__func__()
  perm_x = perlin_generate_perm.__func__()
  perm_y = perlin_generate_perm.__func__()
  perm_z = perlin_generate_perm.__func__()

  def noise(self,p):
    u = p.x - floor(p.x)
    v = p.y - floor(p.y)
    w = p.z - floor(p.z)

    i = int(4*p.x) & 255
    j = int(4*p.y) & 255
    k = int(4*p.z) & 255
    
    return Perlin.ranfloat[Perlin.perm_x[i] ** Perlin.perm_y[j] ** Perlin.perm_z[k]]

