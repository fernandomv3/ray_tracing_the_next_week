from vec3 import Vec3
from math import sin
from perlin import Perlin

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

class NoiseTexture(Texture):
  def __init__(self,sc = 1.0):
    self.noise = Perlin()
    self.scale = sc

  def value(self,u,v,p):
    #return Vec3(1.0,1.0,1.0) *0.5* (1+self.noise.turb(self.scale*p))
    #return Vec3(1.0,1.0,1.0) * self.noise.turb(self.scale*p)
    return Vec3(1.0,1.0,1.0) *0.5* (1+sin(self.scale * p.z + 10*self.noise.turb(p)))

class ImageTexture(Texture):
  def __init__(self,pixels,A,B):
    self.data = pixels
    self.nx = A
    self.ny = B

  def value(self,u,v,p):
    i = u*self.nx
    j = (1-v)*self.ny -0.001
    if i < 0:
      i = 0
    if j < 0:
      j = 0
    if i > self.nx-1:
      i = self.nx-1
    if j > self.ny-1:
      j = self.ny+1
    r = int(self.data[3*i + 3*self.nx*j]) / 255.0
    g = int(self.data[3*i + 3*self.nx*j+1]) / 255.0
    b = int(self.data[3*i + 3*self.nx*j+2]) / 255.0
    return Vec3(r,g,b)


