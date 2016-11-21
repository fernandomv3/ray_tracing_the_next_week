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
  uu = u*u*(3-2*u)
  vv = v*v*(3-2*v)
  ww = w*w*(3-2*w)
  accum = 0.0
  for i in range(2):
    for j in range(2):
      for k in range(2):
        weight_v= Vec3(u-i,v-j,w-k)
        accum += (((i*uu) + (1-i)*(1-uu)) *
                  ((j*vv) + (1-j)*(1-vv)) *
                  ((k*ww) + (1-k)*(1-ww)) * Vec3.dot(c[i][j][k],weight_v))
  return accum

class Perlin:
  def turb(self,p,depth=7):
    accum = 0.0
    temp_p = p
    weight = 1.0
    for i in range(depth):
      accum += weight * self.noise(temp_p)
      weight *= 0.5
      temp_p *= 2
    return abs(accum)

  @staticmethod
  def perlin_generate():
    p = []
    for i in range(0,256):
      p.append(Vec3(-1 + 2*random(),-1 + 2*random(),-1 + 2*random()))
    return p

  @staticmethod
  def perlin_generate_perm():
    p = []
    for i in range(0,256):
      p.append(i)
    permute(p,256)
    return p

  ranvec = perlin_generate.__func__()
  perm_x = perlin_generate_perm.__func__()
  perm_y = perlin_generate_perm.__func__()
  perm_z = perlin_generate_perm.__func__()

  def noise(self,p):
    u = p.x - floor(p.x)
    v = p.y - floor(p.y)
    w = p.z - floor(p.z)

    i = int(floor(p.x))
    j = int(floor(p.y))
    k = int(floor(p.z))
    
    c = []
    for di in range(2):
      c.append([])
      for dj in range(2):
        c[di].append([])
        for dk in range(2):
          c[di][dj].append(Perlin.ranvec[Perlin.perm_x[(i+di)&255] ^ Perlin.perm_y[(j+dj)&255] ^ Perlin.perm_z[(k+dk)&255]])
    return trilinear_interp(c,u,v,w)

