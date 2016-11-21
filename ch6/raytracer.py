#!/usr/bin/env python
from __future__ import print_function, division
from vec3 import Vec3
from ray import Ray
from math import sqrt
from random import random, seed
from hitable import Sphere
from hitable import MovingSphere
from hitable import HitableList
from hitable import FlipNormals
from hitable import XyRect, YzRect, XzRect
from camera import Camera
from material import Lambertian
from material import Metal
from material import Dielectric
from material import DiffuseLight
from texture import ConstantTexture
from texture import CheckerTexture
from texture import NoiseTexture

def color(r,world,depth):
  rec = world.hit(r,0.001,float('inf'))
  if rec is not None:
    emitted = rec["material"].emitted(rec["u"],rec["v"],rec["p"])
    if depth >= 50:
      return emitted
    attenuation,scattered =rec["material"].scatter(r,rec)
    if attenuation is not None:
      return emitted + attenuation * color(scattered,world,depth +1)
    else:
      return emitted
  else:
    return Vec3(0,0,0)

def random_scene():
  l = []
  checker = CheckerTexture(ConstantTexture(Vec3(0.2,0.3,0.1)),ConstantTexture(Vec3(0.9,0.9,0.9)))
  l.append(Sphere(Vec3(0,-1000,-1),1000,Lambertian(checker)))
  for a in range(-11,11):
    for b in range(-11,11):
      choose_mat = random()
      center = Vec3(a+0.9*random(),0.2,b+0.9*random())
      if (center -Vec3(4,0.2,0)).length() > 0.9:
        if choose_mat < 0.8: #diffuse
          l.append(MovingSphere(center,center+Vec3(0.0,0.5*random(),0.0),0.0,1.0,0.2,Lambertian(ConstantTexture(Vec3(random()*random(),random()*random(),random()*random())))))
        elif choose_mat < 0.95: #metal
          l.append(Sphere(center,0.2,Metal(Vec3(0.5*(1+random()),0.5*(1+random()),0.5*(1+random())),0.5*random())))
        else: #glass
          l.append(Sphere(center,0.2,Dielectric(1.5)))
  l.append(Sphere(Vec3(0,1,0),1.0,Dielectric(1.5)))
  l.append(Sphere(Vec3(-4,1,0),1.0,Lambertian(ConstantTexture(Vec3(0.4,0.2,0.1)))))
  l.append(Sphere(Vec3(4,1,0),1.0,Metal(Vec3(0.7,0.6,0.5),0.0)))
  return HitableList(l)

def two_perlin_spheres():
  pertext = NoiseTexture(4.0)
  l = []
  l.append(Sphere(Vec3(0,-1000,0),1000,Lambertian(pertext)))
  l.append(Sphere(Vec3(0,2,0),2,Lambertian(pertext)))
  return HitableList(l)

def simple_light():
  pertext = NoiseTexture(4)
  l = []
  l.append(Sphere(Vec3(0,-1000,0),1000,Lambertian(pertext)))
  l.append(Sphere(Vec3(0,2,0),2,Lambertian(pertext)))
  l.append(Sphere(Vec3(0,7,0),2,DiffuseLight(ConstantTexture(Vec3(4,4,4)))))
  l.append(XyRect(3,5,1,3,-2,DiffuseLight(ConstantTexture(Vec3(4,4,4)))))
  return HitableList(l)

def cornell_box():
  l=[]
  red = Lambertian(ConstantTexture(Vec3(0.65,0.05,0.05)))
  white = Lambertian(ConstantTexture(Vec3(0.73,0.73,0.73)))
  green = Lambertian(ConstantTexture(Vec3(0.12,0.45,0.15)))
  light = DiffuseLight(ConstantTexture(Vec3(15,15,15)))
  l.append(FlipNormals(YzRect(0,555,0,555,555,green)))
  l.append(YzRect(0,555,0,555,0,red))
  l.append(XzRect(213,343,227,332,554,light))
  l.append(FlipNormals(XzRect(0,555,0,555,555,white)))
  l.append(XzRect(0,555,0,555,0,white))
  l.append(FlipNormals(XyRect(0,555,0,555,555,white)))
  return HitableList(l)

def main():
  seed(20)
  nx = 200
  ny = 150
  ns = 100
  print ("P3\n",nx," ",ny,"\n255")

  world = cornell_box()

  lookfrom = Vec3(278,278,-800)
  lookat = Vec3(278,278,0)
  dist_to_focus = 10.0
  aperture = 0.0
  vfov = 40
  cam = Camera(lookfrom,lookat,Vec3(0,1,0),vfov,nx/ny,aperture,dist_to_focus,0.0,1.0)
  for j in reversed(range(ny)):
    for i in range(nx):
      col = Vec3(0,0,0)
      for s in range(ns):
        u = (i+random())/nx
        v = (j+random())/ny
        r = cam.get_ray(u,v)
        p = r.point_at_parameter(2.0)
        col += color(r,world,0)

      col /= ns
      col = Vec3(sqrt(col[0]),sqrt(col[1]),sqrt(col[2]))
      ir = int(255.99*col[0])
      ig = int(255.99*col[1])
      ib = int(255.99*col[2])
      print (ir," ",ig," ",ib)

if __name__ == '__main__':
  main()