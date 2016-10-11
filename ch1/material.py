from vec3 import Vec3
from ray import Ray
from random import random
import math

class Material:
  def scatter(self,r_in,rec):
    pass

  @classmethod
  def random_in_unit_sphere(cls):
    while True:
      p = 2.0*Vec3(random(),random(),random()) - Vec3(1,1,1)
      if Vec3.dot(p,p) < 1.0:
        return p

class Lambertian(Material):
  def __init__(self, a = Vec3()):
    self.albedo = a

  def scatter(self, r_in,rec):
    target = rec["p"] + rec["normal"] + Material.random_in_unit_sphere()
    scattered = Ray(rec["p"],target - rec["p"])
    attenuation = self.albedo
    return attenuation,scattered

class Metal(Material):
  def __init__(self,a = Vec3(),f = 0.0):
    self.albedo = a
    self.fuzz = min(f, 1.0)

  def scatter(self, r_in,rec):
    reflected = Vec3.reflect(Vec3.unit_vector(r_in.direction),rec["normal"])
    scattered = Ray(rec["p"],reflected + self.fuzz * Material.random_in_unit_sphere())
    attenuation = self.albedo
    if Vec3.dot(scattered.direction,rec["normal"]) > 0:
      return attenuation,scattered
    else:
      return None,None

class Dielectric(Material):
  def __init__(self, ri):
    self.ref_idx = ri

  def scatter(self, r_in, rec):
    outward_normal = Vec3()
    reflected = Vec3.reflect(r_in.direction,rec["normal"])
    ni_over_nt = 0.0
    attenuation = Vec3(1.0,1.0,1.0)
    cosine = 0.0
    if Vec3.dot(r_in.direction,rec["normal"]) > 0:
      outward_normal = -rec["normal"]
      ni_over_nt = self.ref_idx
      cosine = self.ref_idx * Vec3.dot(r_in.direction,rec["normal"])/ r_in.direction.length()
    else:
      outward_normal = rec["normal"]
      ni_over_nt = 1.0 / self.ref_idx
      cosine = -Vec3.dot(r_in.direction,rec["normal"])/ r_in.direction.length()
    
    scattered = Ray()
    reflect_prob = 0.0
    refracted = Vec3.refract(r_in.direction,outward_normal,ni_over_nt)
    if refracted is not None:
      reflect_prob = schlick(cosine,self.ref_idx)
    else:
      reflect_prob = 1.0
    if random() < reflect_prob:
      scattered = Ray(rec["p"],reflected)
    else:
      scattered = Ray(rec["p"],refracted)
    return attenuation, scattered

def schlick(cosine,ref_idx):
  r0 = (1-ref_idx) / (1+ref_idx)
  r0 = r0*r0
  return r0 + (1-r0)*math.pow((1-cosine),5)