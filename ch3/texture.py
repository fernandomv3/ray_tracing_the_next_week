from vec3 import Vec3
from math import sin

class Texture:
  def value(self,u,v,p):
    pass

class ConstantTexture(Texture):
  def __init__(self,c):
    self.color = c

  def value(self,u,v,p):
    return self.color

class CheckerTexture(Texture):
  def __init__(self,t0,t1):
    self.even = t0
    self.odd = t1

  def value(self,u,v,p):
    sines = sin(10*p.x)*sin(10*p.y)*sin(10*p.z)
    if sines < 0:
      return self.odd.value(u,v,p)
    else:
      return self.even.value(u,v,p)