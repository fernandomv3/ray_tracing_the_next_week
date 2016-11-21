from __future__ import print_function, division
from vec3 import Vec3
from math import sqrt, atan2, asin, pi
from material import Material
from aabb import Aabb
from random import randint
import sys

def getSphereUv(p):
  phi = atan2(p.z,p.x)
  theta = asin(p.y)
  u = 1-(phi + pi)/(2*pi)
  v = (theta +pi/2) / pi
  return u,v

class Hitable:
  def hit(self,r,t_min,t_max):
    pass
  def bounding_box(self,t0,t1):
    pass

class Sphere(Hitable):
  def __init__(self, cen = Vec3(), r = 1.0, material=Material()):
    self.center = cen
    self.radius = r
    self.material = material

  def hit(self,r,t_min,t_max):
    rec = None
    oc = r.origin - self.center
    a = Vec3.dot(r.direction,r.direction)
    b = Vec3.dot(oc,r.direction)
    c = Vec3.dot(oc,oc) - (self.radius*self.radius)
    discriminant = (b*b) - (a*c)
    if discriminant > 0:
      rec = {}
      temp = (-b - sqrt(discriminant)) / a
      if t_min < temp < t_max:
        rec["t"] = temp
        rec["p"] = r.point_at_parameter(rec["t"])
        rec["u"],rec["v"] =getSphereUv((rec["p"] - self.center) / self.radius)
        rec["normal"] = (rec["p"] - self.center) / self.radius
        rec["material"] = self.material
        return rec
      temp = (-b + sqrt(discriminant)) / a
      if t_min < temp < t_max:
        rec["t"] = temp
        rec["p"] = r.point_at_parameter(rec["t"])
        rec["u"],rec["v"] =getSphereUv((rec["p"] - self.center) / self.radius)
        rec["normal"] = (rec["p"] - self.center) / self.radius
        rec["material"] = self.material
        return rec
    return None

  def bounding_box(self,t0,t1):
    rad = Vec3(self.radius,self.radius,self.radius)
    box = Aabb(self.center- rad,self.center + rad)
    return box


class MovingSphere(Hitable):
  def __init__(self,cen0,cen1,t0,t1,r,m):
    self.center0 = cen0
    self.center1 = cen1
    self.time0 = t0
    self.time1 = t1
    self.radius = r
    self.material = m

  def center(self,time):
    return self.center0 +((time-self.time0)/(self.time1-self.time0)) * (self.center1 -self.center0)

  def hit(self,r,t_min,t_max):
    rec = None
    oc = r.origin - self.center(r.time)
    a = Vec3.dot(r.direction,r.direction)
    b = Vec3.dot(oc,r.direction)
    c = Vec3.dot(oc,oc) - (self.radius*self.radius)
    discriminant = (b*b) - (a*c)
    if discriminant > 0:
      rec = {}
      temp = (-b - sqrt(discriminant)) / a
      if t_min < temp < t_max:
        rec["t"] = temp
        rec["p"] = r.point_at_parameter(rec["t"])
        rec["u"],rec["v"] =getSphereUv((rec["p"] - self.center) / self.radius)
        rec["normal"] = (rec["p"] - self.center(r.time)) / self.radius
        rec["material"] = self.material
        return rec
      temp = (-b + sqrt(discriminant)) / a
      if t_min < temp < t_max:
        rec["t"] = temp
        rec["p"] = r.point_at_parameter(rec["t"])
        rec["u"],rec["v"] =getSphereUv((rec["p"] - self.center) / self.radius)
        rec["normal"] = (rec["p"] - self.center(r.time)) / self.radius
        rec["material"] = self.material
        return rec
    return None

def surrounding_box(box0,box1):
  small = Vec3(
      min(box0.min["x"],box1.min["x"]),
      min(box0.min["y"],box1.min["y"]),
      min(box0.min["z"],box1.min["z"])
    )
  big = Vec3(
      max(box0.max["x"],box1.max["x"]),
      max(box0.max["y"],box1.max["y"]),
      max(box0.max["z"],box1.max["z"])
    )
  return Aabb(small,big)

def compareX(hitable):
  box = hitable.bounding_box(0,0)
  if box is None:
    print("no bounding box in BvhNode constructor", file=sys.stderr) 
  return box.min[0]

def compareY(hitable):
  box = hitable.bounding_box(0,0)
  if box is None:
    print("no bounding box in BvhNode constructor", file=sys.stderr) 
  return box.min[1]

def compareZ(hitable):
  box = hitable.bounding_box(0,0)
  if box is None:
    print("no bounding box in BvhNode constructor", file=sys.stderr) 
  return box.min[2]

class BvhNode(Hitable):
  def __init__(self,l,time0,time1):
    axis = randint(0,2)
    if axis == 0:
      l = sorted(l,key= compareX)
    elif axis == 1:
      l = sorted(l,key= compareY)
    else:
      l = sorted(l,key= compareZ)
    n = len(l)
    if n == 1:
      self.left = l
      self.right = l
    elif n == 2:
      self.left = l[0]
      self.right = l[1]
    else:
      self.left = BvhNode(l[:n//2+1],time0,time1)
      self.right = BvhNode(l[n//2:],time0,time1)

    box_left = self.left.bounding_box(time0,time1)
    box_right = self.right.bounding_box(time0,time1)
    if (box_left is None) or (box_right is None):
      print("no bounding box in BvhNode constructor", file=sys.stderr)
    self.box = surrounding_box(box_left,box_right)

  def bounding_box(self,t0,t1):
    return self.box

  def hit(self,r,t_min,t_max):
    if self.box.hit(r,t_min,t_max):
      left_rec = self.left.hit(r,t_min,t_max)
      right_rec = self.right.hit(r,t_min,t_max)
      if((left_rec is not None) and (right_rec is not None)):
        if left_rec["t"] < right_rec["t"]:
          return left_rec
        else:
          return right_rec
      elif left_rec is not None:
        return left_rec
      elif right_rec is not None:
        return right_rec
    return None

class FlipNormals(Hitable):
  def __init__(self,p):
    self.ptr = p

  def hit(self,r,t_min,t_max):
    rec = self.ptr.hit(r,t_min,t_max)
    if rec is not None:
      rec["normal"] = -rec["normal"]
      return rec
    else:
      return None

  def bounding_box(self,t0,t1):
    return self.ptr.bounding_box(t0,t1)

class HitableList(Hitable):
  def __init__(self,l = []):
    self.list = l

  def hit(self,r,t_min,t_max):
    result = {}
    hit_anything = False
    closest_hit = t_max
    for h in self.list:
      temp_rec = h.hit(r,t_min,closest_hit)
      if temp_rec is not None:
        hit_anything = True
        closest_hit = temp_rec["t"]
        result = temp_rec
    if hit_anything:
      return result
    return None

class XyRect(Hitable):
  def __init__(self,_x0,_x1,_y0,_y1,_k,mat):
    self.x0=_x0
    self.x1=_x1
    self.y0=_y0
    self.y1=_y1
    self.k =_k
    self.mp = mat

  def hit(self,r,t0,t1):
    t = (self.k- r.origin.z)/r.direction.z
    if (t < t0) or (t > t1):
      return None
    x = r.origin.x + t * r.direction.x
    y = r.origin.y + t * r.direction.y
    if (x < self.x0) or (x > self.x1) or (y < self.y0) or (y > self.y1):
      return None
    rec = {}
    rec["u"] = (x - self.x0)/(self.x1-self.x0)
    rec["v"] = (y - self.y0)/(self.y1-self.y0)
    rec["t"] = t
    rec["material"] = self.mp
    rec["p"] = r.point_at_parameter(t)
    rec["normal"] = Vec3(0,0,1)
    return rec

  def bounding_box(self,t0,t1):
    box = Aabb(Vec3(self.x0,self.y0,self.k-0.0001),Vec3(self.x1,self.y1,self.k+0.0001))
    return box

class XzRect(Hitable):
  def __init__(self,_x0,_x1,_z0,_z1,_k,mat):
    self.x0=_x0
    self.x1=_x1
    self.z0=_z0
    self.z1=_z1
    self.k =_k
    self.mp = mat

  def hit(self,r,t0,t1):
    t = (self.k- r.origin.y)/r.direction.y
    if (t < t0) or (t > t1):
      return None
    x = r.origin.x + t * r.direction.x
    z = r.origin.z + t * r.direction.z
    if (x < self.x0) or (x > self.x1) or (z < self.z0) or (z > self.z1):
      return None
    rec = {}
    rec["u"] = (x - self.x0)/(self.x1-self.x0)
    rec["v"] = (z - self.z0)/(self.z1-self.z0)
    rec["t"] = t
    rec["material"] = self.mp
    rec["p"] = r.point_at_parameter(t)
    rec["normal"] = Vec3(0,1,0)
    return rec

  def bounding_box(self,t0,t1):
    box = Aabb(Vec3(self.x0,self.k-0.0001,self.z0),Vec3(self.x1,self.k+0.0001,self.z1))
    return box

class YzRect(Hitable):
  def __init__(self,_y0,_y1,_z0,_z1,_k,mat):
    self.y0=_y0
    self.y1=_y1
    self.z0=_z0
    self.z1=_z1
    self.k =_k
    self.mp = mat

  def hit(self,r,t0,t1):
    t = (self.k- r.origin.x)/r.direction.x
    if (t < t0) or (t > t1):
      return None
    z = r.origin.z + t * r.direction.z
    y = r.origin.y + t * r.direction.y
    if (z < self.z0) or (z > self.z1) or (y < self.y0) or (y > self.y1):
      return None
    rec = {}
    rec["u"] = (z - self.z0)/(self.z1-self.z0)
    rec["v"] = (y - self.y0)/(self.y1-self.y0)
    rec["t"] = t
    rec["material"] = self.mp
    rec["p"] = r.point_at_parameter(t)
    rec["normal"] = Vec3(1,0,0)
    return rec

  def bounding_box(self,t0,t1):
    box = Aabb(Vec3(self.k-0.0001,self.y0,self.z0),Vec3(self.k+0.0001,self.y1,self.z1))
    return box