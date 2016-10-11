from vec3 import Vec3
from math import sqrt
from material import Material

class Hitable:
  def hit(self,r,t_min,t_max):
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
        rec["normal"] = (rec["p"] - self.center) / self.radius
        rec["material"] = self.material
        return rec
      temp = (-b + sqrt(discriminant)) / a
      if t_min < temp < t_max:
        rec["t"] = temp
        rec["p"] = r.point_at_parameter(rec["t"])
        rec["normal"] = (rec["p"] - self.center) / self.radius
        rec["material"] = self.material
        return rec
    return None

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
        rec["normal"] = (rec["p"] - self.center(r.time)) / self.radius
        rec["material"] = self.material
        return rec
      temp = (-b + sqrt(discriminant)) / a
      if t_min < temp < t_max:
        rec["t"] = temp
        rec["p"] = r.point_at_parameter(rec["t"])
        rec["normal"] = (rec["p"] - self.center(r.time)) / self.radius
        rec["material"] = self.material
        return rec
    return None

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