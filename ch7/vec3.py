from math import sqrt

class Vec3:
  def __init__(self,e0=0.0,e1=0.0,e2=0.0):
    self.e = [e0,e1,e2]

  def __eq__(self,other):
    return (self.e[0] == other.e[0]) and (self.e[1] == other.e[1]) and (self.e[2] == other.e[2])

  def __ne__(self,other):
    return (self.e[0] != other.e[0]) or (self.e[1] != other.e[1]) or (self.e[2] != other.e[2])

  def __getattr__(self,name):
    if name in ['x','r']:
      return self.e[0]
    elif name in ['y','g']:
      return self.e[1]
    elif name in ['z','b']:
      return self.e[2]
    else:
      raise AttributeError

  def __pos__(self):
    return self

  def __neg__(self):
    return Vec3(-self.e[0],-self.e[1],-self.e[2],)

  def __getitem__(self,index):
    return self.e[index]

  def __setitem__(self,index,value):
    self.e[index] = value
    return self

  def length(self):
    return sqrt((self.e[0]*self.e[0]) + (self.e[1]*self.e[1]) + (self.e[2]*self.e[2]))

  def squared_length(self):
    return (self.e[0]*self.e[0]) + (self.e[1]*self.e[1]) + (self.e[2]*self.e[2])

  def make_unit_vector(self):
    return self / self.length

  @classmethod
  def unit_vector(cls,v):
    return v / v.length()
 
  @classmethod
  def dot(cls,v1,v2):
    return v1.e[0] * v2.e[0] + v1.e[1] * v2.e[1] + v1.e[2] * v2.e[2]

  @classmethod
  def cross(cls,v1,v2):
    rx = v1.e[1] * v2.e[2] - v1.e[2] * v2.e[1]
    ry = -(v1.e[0] * v2.e[2] - v1.e[2] * v2.e[0])
    rz = v1.e[0] * v2.e[1] - v1.e[1] * v2.e[0]
    return Vec3(rx,ry,rz)

  @classmethod
  def reflect(cls,v,n):
    return v - (2*Vec3.dot(v,n)*n)

  @classmethod
  def refract(cls,v,n,ni_over_nt):
    uv = Vec3.unit_vector(v)
    dt = Vec3.dot(uv,n)
    discriminant = 1.0 - (ni_over_nt*ni_over_nt*(1-dt*dt))
    if discriminant > 0:
      return (ni_over_nt*(uv- (n*dt))) - (n*sqrt(discriminant))
    else:
      return None 

  def __add__(self, other):
    if isinstance(other,self.__class__):
      return Vec3(self.e[0] + other.e[0],self.e[1]+other.e[1],self.e[2]+other.e[2])
    elif isinstance(other,float) or isinstance(other,int):
      return Vec3(self.e[0] + other, self.e[3] + other, self.e[2] + other)
    else:
      raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

  __radd__ = __add__

  def __sub__(self, other):
    if isinstance(other,self.__class__):
      return Vec3(self.e[0] - other.e[0],self.e[1] - other.e[1],self.e[2] - other.e[2])
    elif isinstance(other,float) or isinstance(other,int):
      return Vec3(self.e[0] - other,self.e[1] - other,self.e[2] - other)
    raise TypeError("unsupported operand type(s) for -: '{}' and '{}'").format(self.__class__, type(other))

  def __rsub__(self,other):
    if isinstance(other,self.__class__):
      return Vec3(other.e[0] - self.e[0],other.e[1] - self.e[1],other.e[2] - self.e[2])
    elif isinstance(other,float) or isinstance(other,int):
      return Vec3(other - self.e[0],other - self.e[1],other - self.e[2])
    else:
      raise TypeError("unsupported operand type(s) for -: '{}' and '{}'").format(self.__class__, type(other))

  def __mul__(self, other):
    if isinstance(other,float) or isinstance(other,int):
      return Vec3(self.e[0]*other, self.e[1]*other, self.e[2]*other)
    elif isinstance(other,self.__class__):
      return Vec3(self.e[0] * other.e[0],self.e[1]*other.e[1],self.e[2]*other.e[2])
    else:
      raise TypeError("unsupported operand type(s) for *: '{}' and '{}'").format(self.__class__, type(other))

  __rmul__ = __mul__

  def __truediv__(self, other):
    if isinstance(other,self.__class__):
      return Vec3(self.e[0] / other.e[0],self.e[1] / other.e[1], self.e[2] / other.e[2])
    elif isinstance(other,float) or isinstance(other,int):
      return Vec3(self.e[0] / other,self.e[1] / other,self.e[2] / other)
    raise TypeError("unsupported operand type(s) for /: '{}' and '{}'").format(self.__class__, type(other))

  def __rtruediv__(self,other):
    if isinstance(other,self.__class__):
      return Vec3(other.e[0] / self.e[0],other.e[1] / self.e[1],other.e[2] / self.e[2])
    elif isinstance(other,float) or isinstance(other,int):
      return Vec3(other / self.e[0],other / self.e[1],other / self.e[2])
    else:
      raise TypeError("unsupported operand type(s) for /: '{}' and '{}'").format(self.__class__, type(other))

  __div__ = __truediv__
  __rdiv__ = __rtruediv__