from vec3 import Vec3

def ffmin(a,b):
  return a if a < b else b

def ffmax(a,b):
  return a if a > b else b

class Aabb:
  def __init__(self,a,b):
    self.min = a
    self.max = b

  @property
  def min(self):
    return self.min

  @property
  def max(self):
    return self.max

  def hit(self,r,tmin,tmax):
#    for a in range(0,3):
#      t0 = ffmin(
#      	(self.min[a] - r.origin[a]) / r.direction[a],
#      	(self.max[a] - r.origin[a]) / r.direction[a] 
#      	)
#      t1 = ffmax(
#      	(self.min[a] - r.origin[a]) / r.direction[a],
#      	(self.max[a] - r.origin[a]) / r.direction[a] 
#      	)
#      tmin = ffmax(t0,tmin)
#      tmax = ffmin(t1,tmax)
#      if tmax <= tmin:
#      	return False
#    return True
    for a in range(0,3):
      invD = 1.0 / r.direction[a]
      t0 = (self.min[a] - r.origin[a]) * invD
      t1 = (self.max[a] - r.origin[a]) * invD
      if invD < 0.0:
        t0,t1 = t1,t0
      tmin = t0 if t0 > tmin else tmin
      tmax = t1 if t1 < tmax else tmax
      if tmax <= tmin:
        return False
    return True
