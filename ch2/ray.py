from vec3 import Vec3

class Ray:
  def __init__(self,a = Vec3(),b = Vec3(),time=0.0):
    self.A = a
    self.B = b
    self._time = time

  @property
  def origin(self):
    return self.A

  @property
  def direction(self):
    return self.B

  @property
  def time(self):
    return self._time

  def point_at_parameter(self,t):
    return self.A + t*self.B