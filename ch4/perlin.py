from __future__ import print_function
from vec3 import Vec3
from random import random, shuffle
from math import floor
import sys

def permute(p,n):
  for i in range(n-1,0,-1):
    target = int(random()*(i+1))
    p[i],p[target] = p[target],p[i]

def trilinear_interp(c,u,v,w):
  accum = 0.0
  for i in range(2):
    for j in range(2):
      for k in range(2):
        accum += ((i*u + (1-i)*(1-u)) *
                  (j*v + (1-j)*(1-v)) *
                  (k*w + (1-k)*(1-w)) * c[i][j][k])
  return accum

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
    #permute(p,256)
    shuffle(p)
    return p

  ranfloat = perlin_generate.__func__()
  perm_x = perlin_generate_perm.__func__()
  perm_y = perlin_generate_perm.__func__()
  perm_z = perlin_generate_perm.__func__()

  def noise(self,p):
    u = p.x - floor(p.x)
    v = p.y - floor(p.y)
    w = p.z - floor(p.z)
#
#    i = int(4*p.x) & 255
#    j = int(4*p.y) & 255
#    k = int(4*p.z) & 255
#    
#    return Perlin.ranfloat[Perlin.perm_x[i] ^ Perlin.perm_y[j] ^ Perlin.perm_z[k]]
    i = int(floor(p.x))
    j = int(floor(p.y))
    k = int(floor(p.z))
    c = [[[0.0]*2]*2]*2
    for di in range(2):
      for dj in range(2):
        for dk in range(2):
          c[di][dj][dk] = Perlin.ranfloat[Perlin.perm_x[(i+di)&255] ^ Perlin.perm_y[(j+dj)&255] ^ Perlin.perm_z[(k+dk)&255]]
    return trilinear_interp(c,u,v,w)

