# Raytracer in Python

## 1. Example of intersecting objects drawn

### The following input:
[Test Intersection](input/testIntersection.txt)
```
NEAR 1
LEFT -1
RIGHT 1
BOTTOM -1
TOP 1
RES 600 600
SPHERE s1 4 1 -10 2 2 1 0.5 0 0 1 0 0 0 100
SPHERE s2 0 0 -10 4 4 1 0 0.5 0 1 0 0 0 10
SPHERE s3 -4 1 -10 2 2 1 0.5 0 0 1 0 0 0 1000
SPHERE s4 0 4 -10 3 3 1 0 0 0.5 1 0 0 0 1000
LIGHT l1 0 0 0 0.7 0.7 0.7
LIGHT l2 5 5 -5 1 1 1
BACK 1 1 1
AMBIENT 0.85 0.85 0.85
OUTPUT testIntersection.ppm
```
### Produces:

![Example output for testIntersection.ppm](/output/pngs/testIntersection.png)

## 2. Example of objects rendered with ambient lighting

### The following input:

[Test Ambient Lighting](input/testAmbient.txt)
```
NEAR 1
LEFT -1
RIGHT 1
BOTTOM -1
TOP 1
RES 600 600
SPHERE s1 0 0 -10 2 4 2 0.5 0 0 1 0 0 0 50
SPHERE s2 4 4 -10 1 2 1 0 0.5 0 1 0 0 0 50
SPHERE s3 -4 2 -10 1 2 1 0 0 0.5 1 0 0 0 50
LIGHT l1 0 0 0 0.3 0.3 0.3
LIGHT l2 10 10 -10 0.9 0.9 0
LIGHT l3 -10 5 -5 0 0 0.9
BACK 1 1 1
AMBIENT 0.75 0.75 0.75
OUTPUT testAmbient.ppm
```

### Produces:

![Example output for testAmbient.ppm](/output/pngs/testAmbient.png)

## 3. Example of a scene rendering the blue background in addition to 5 objects 

### The following input:
[Test Background](input/testBackground.txt)
```
NEAR 1
LEFT -1
RIGHT 1
BOTTOM -1
TOP 1
RES 600 600
SPHERE s1 0 0 -10 3 3 1 0.5 0 0 1 0 0 0 50
SPHERE s2 5 5 -10 3 3 1 0.5 0 0 1 0 0 0 50
SPHERE s3 5 -5 -10 3 3 1 0.5 0 0 1 0 0 0 50
SPHERE s4 -5 5 -10 3 3 1 0.5 0 0 1 0 0 0 50
SPHERE s5 -5 -5 -10 3 3 1 0.5 0 0 1 0 0 0 50
LIGHT l1 0 0 0 0.3 0.3 0.3
BACK 0 0 1
AMBIENT 0.5 0.5 0.5
OUTPUT testBackground.ppm
```
### Produces:

![Example output for testBackground.ppm](/output/pngs/testBackground.png)

## 4. Example of image plane intersecting a very close object

### The following input:
[Test Image Plane](input/testImgPlane.txt)
```
NEAR 1
LEFT -1
RIGHT 1
BOTTOM -1
TOP 1
RES 600 600
SPHERE s1 0 0 -1 0.5 0.5 0.5 0 0 0.5 1 1 1 0 50
LIGHT l1 0 0 -10 0.3 0.3 0.3
BACK 1 1 1
AMBIENT 0.5 0.5 0.5
OUTPUT testImgPlane.ppm
```
### Produces:

![Example output for testImgPlane.ppm](/output/pngs/testImgPlane.png)

## 5. Example of objects when behind the eye

### The following input:
[Test Behind](input/testBehind.txt)
```
NEAR 1
LEFT -1
RIGHT 1
BOTTOM -1
TOP 1
RES 600 600
SPHERE s1 0 0 10 2 4 2 0.5 0 0 1 0 0 0 50
SPHERE s2 4 4 10 1 2 1 0 0.5 0 1 0 0 0 50
SPHERE s3 -4 2 10 1 2 1 0 0 0.5 1 0 0 0 50
LIGHT l1 0 0 0 0.3 0.3 0.3
LIGHT l2 10 10 -10 0.9 0.9 0
LIGHT l3 -10 5 -5 0 0 0.9
BACK 0.5 0.5 0.5
AMBIENT 0.5 0.5 0.5
OUTPUT testBehind.ppm
```
### Produces:

![Example output for testBehind.ppm](/output/pngs/testBehind.png)
