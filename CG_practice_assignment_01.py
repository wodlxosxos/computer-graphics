#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)


class Box:
	def __init__(self, minPt, maxPt, diffuse, shtype):
		self.minPt = minPt
		self.maxPt = maxPt
		self.shtype = shtype
		self.figure = 'Box'
		self.diffuseColor = diffuse
#		if self.type == 'Phong'

class Sphere:
	def __init__(self, center, radius, shType, diffuse, *args):
		self.center = center
		self.radius = radius
		self.shType = shType
		self.figure = 'Sphere'
		self.diffuseColor = diffuse
		self.specularColor = []
		self.exponent = 0
		if self.shType == 'Phong':
			self.specularColor = args[0]
			self.exponent = args[1]
def trace_ray(arr, viewD, point):
	minDistance = np.inf	
	minIdx = -1
	index = 0
	
	for sORb in arr:
		if sORb.figure == 'Sphere':
			a = np.dot(viewD, viewD)
			b = np.dot((point-sORb.center), viewD) * 2
			c = np.dot((point-sORb.center), (point-sORb.center)) - sORb.radius ** 2
			if b**2 - 4*a*c >= 0:
				if -b + np.sqrt(b ** 2 - 4 * a * c) >= 0:
					if minDistance >= (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2.0*a):
						minDistance = (-b + np.sqrt(b ** 2 - a * c)) / (2.0*a)
						minIdx = index
				if -b - np.sqrt(b ** 2 - 4 * a * c) >= 0:
					if minDistance >= (-b - np.sqrt(b ** 2 - 4 * a * c)) / (2.0*a):
						minDistance = (-b - np.sqrt(b ** 2 - 4 * a * c)) / (2.0*a)
						minIdx = index
		index = index + 1
	return [minDistance, minIdx]

def main():


	tree = ET.parse(sys.argv[1])
	root = tree.getroot()
	viewPoint = []
	viewDir = np.array([0,0,-1]).astype(np.float)
	viewUp = np.array([0,1,0]).astype(np.float)
	viewProjNormal = -1*viewDir
	viewWidth=1.0
	viewHeight=1.0
	projDistance=1.0
	intensity=np.array([1,1,1]).astype(np.float)

	imgSize=np.array(root.findtext('image').split()).astype(np.int)

	for c in root.findall('camera'):
		viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float)
		viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
		viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float)
		viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
		if(c.findtext('projDistance')):
			projDistance = float(c.findtext('projDistance'))
		viewWidth = float(c.findtext('viewWidth'))
		viewHeight = float(c.findtext('viewHeight'))
	
	boxOrsphere = []
	for c in root.findall('surface'):
		ref = ''
		if c.get('type') == 'Sphere':
			sphereCenter = np.array(c.findtext('center').split()).astype(np.float)
			radius = float(c.findtext('radius'))
			for child in c:
				if child.tag == 'shader':
					ref = child.get('ref')
			for sh in root.findall('shader'):
				if sh.get('name') == ref:
					diffColor = np.array(sh.findtext('diffuseColor').split()).astype(np.float)
					if sh.get('type') == 'Lambertian':
						boxOrsphere.append(Sphere(sphereCenter, radius, 'Lambertian', diffColor))
					elif sh.get('type') == 'Phong':
						speColor = np.array(sh.findtext('specularColor').split()).astype(np.float)
						expo = float(sh.findtext('exponent'))
						boxOrsphere.append(Sphere(sphereCenter, radius, 'Phong', diffColor, speColor, expo))

	lightList = []
	for c in root.findall('light'):
		position = np.array(c.findtext('position').split()).astype(np.float)
		intensity_l = np.array(c.findtext('intensity').split()).astype(np.float)
		lightList.append(np.array([position, intensity_l]))
	
	# Create an empty image
	channels=3
	img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
	img[:,:]=0
	
	width = viewWidth / imgSize[0]
	height = viewHeight / imgSize[1]

	u = np.cross(viewDir, viewUp)
	v = np.cross(viewDir, u) / np.sqrt(np.dot(np.cross(viewDir, u), np.cross(viewDir, u)))

	unit_viewDir = viewDir / np.sqrt(np.dot(viewDir,viewDir))
	u = u / np.sqrt(np.dot(u,u))

	zero2 = unit_viewDir * projDistance - u*width*((imgSize[0]/2) + 1/2) - v*height*((imgSize[1]/2) + 1/2)
	for x in np.arange(imgSize[0]):
		for y in np.arange(imgSize[1]):
			viewD = zero2 + u * x * width + v * y * height
			min = trace_ray(boxOrsphere, viewD, viewPoint)
			if min[1] == -1:
				img[y][x] = np.array([0,0,0])
			else:
				normal = np.array([0,0,0])
				if boxOrsphere[min[1]].figure == 'Sphere':
					#normal vector 구하는 과정
					normal = viewPoint + min[0]*viewD - boxOrsphere[min[1]].center
					normal /= np.sqrt(np.dot(normal, normal))
				near = -min[0]*viewD
				xLight = 0
				yLight = 0
				zLight = 0
				for src in lightList:
					light = src[0] - viewPoint + near
					light = light / np.sqrt(np.dot(light, light))
					same = trace_ray(boxOrsphere, -light, src[0])
					if same[1] == min[1]:
						if boxOrsphere[min[1]].shType == 'Lambertian':
							if np.dot(light, normal) > 0:
								xLight += boxOrsphere[min[1]].diffuseColor[0] * src[1][0] * np.dot(light, normal)
								yLight += boxOrsphere[min[1]].diffuseColor[1] * src[1][1] * np.dot(light, normal)
								zLight += boxOrsphere[min[1]].diffuseColor[2] * src[1][2] * np.dot(light, normal)
						elif boxOrsphere[min[1]].shType == 'Phong':
							unitOfnear = near / np.sqrt(np.dot(near, near))
							lightRef = unitOfnear + light
							lightRef = lightRef/np.sqrt(np.dot(lightRef, lightRef))#PDF 04_2 raytracing. 44pg
							xLight += boxOrsphere[min[1]].diffuseColor[0] * max(0, np.dot(light, normal))*src[1][0] + boxOrsphere[min[1]].specularColor[0] * pow(max(0, np.dot(normal, lightRef)), boxOrsphere[min[1]].exponent) * src[1][0]
							yLight += boxOrsphere[min[1]].diffuseColor[1] * max(0, np.dot(light, normal))*src[1][1] + boxOrsphere[min[1]].specularColor[1] * pow(max(0, np.dot(normal, lightRef)), boxOrsphere[min[1]].exponent) * src[1][1]
							zLight += boxOrsphere[min[1]].diffuseColor[2] * max(0, np.dot(light, normal))*src[1][2] + boxOrsphere[min[1]].specularColor[2] * pow(max(0, np.dot(normal, lightRef)), boxOrsphere[min[1]].exponent) * src[1][2]
				sha = Color(xLight,yLight,zLight)
				sha.gammaCorrect(2.2)
				img[y][x] = sha.toUINT8()
	rawimg = Image.fromarray(img, 'RGB')
	rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
	main()
