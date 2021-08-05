import numpy as np
import array
import math
import time
import fileinput
import sys

#Init parameters
#Image Coordinate stuff
global pixWidth
global pixHeight 
global rows 
global cols 

#Camera Coordinate stuff
global near 
global left  # -W
global right  # W
global bottom  # -H
global top  # H
global back 

#Some Scene Stuff
global outFileName
global sceneAmbience

class ray:
    def __init__(self,origin,dir ):
        self.origin = origin # A point
        self.dir = dir #A direction vector
    
    def getOrigin(self):
        return self.origin
    
    def getDire(self):
        return self.dir

def vec3(x,y,z):
    return np.array([x,y,z,0])

def point3(x,y,z):
    return np.array([x,y,z,1])

def color(x,y,z):
    return np.array([x,y,z])

#Default ambience that will be overwritten
sceneAmbience = color(1,1,1)

#Produces a unit vector given a vector
def unitvector(v):
    return v/ np.linalg.norm(v)

#Used in sphere properties so we can transform canonical sphere later on 
def createTranformationMatrix(xScale,yScale,zScale,xTranslate,yTranslate,zTranslate):
    M = np.array([[xScale,0,0,xTranslate],[0,yScale,0,yTranslate],[0,0,zScale,zTranslate],[0,0,0,1]])
    M2 = np.linalg.inv(M)
    return M2

class sphere:
    def __init__(self,name, xpos, ypos,zpos,xscale,yscale,zscale,r,g,b,ambience,diffuse,spec,reflect,specexp):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos

        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale
        self.r = r
        self.g = g
        self.b = b
        self.ambience = ambience
        self.diffuse = diffuse
        self.spec = spec
        self.reflect = reflect
        self.specexp = specexp

        self.modelMatrix = createTranformationMatrix(xscale,yscale,zscale,xpos,ypos,zpos)
        self.color = color(r,g,b)


startTime = time.time()


#Color assigning logic
def ray_color2(rayIn: ray,back,spheres): 
    lowestt = 100000

    outColor = back
    #print("Batch")
    for s in spheres:
        intersectInfo = intersect3(rayIn,s)
        
        #Get color of closes intersecting sphere
        if  intersectInfo[1] < lowestt:
            lowestt = intersectInfo[1]   
            
        if(intersectInfo[0] and (intersectInfo[1] <= lowestt)):
            outColor = s.color*s.ambience*sceneAmbience

    return outColor       

#Ray and sphere intersection logic
def intersect3(ray: ray,sphere: sphere):  
    S = ray.origin 
    c = ray.dir

    #Drop homogenous coordinate
    S = S.reshape(-1,1)
    c = c.reshape(-1,1)
    
    #Do math from lecture 14 slides
    S = np.matmul(sphere.modelMatrix,S)
    c = np.matmul(sphere.modelMatrix,c)

    S = np.squeeze(S[:3]) 
    c = np.squeeze(c[:3])
 
    c = unitvector(c)

    r = 1

    A = np.dot(c,c)
    B = np.dot(S,c)
    C = np.dot(S,S)-r 

    #Used to test for solutions
    dis = B*B - A*C

    th = 100000

    if(dis>=0):
        th = -1*(B/A) + math.sqrt((B*B)-(A*C))/A
        thNeg = -1*(B/A) - math.sqrt((B*B)-(A*C))/A

        if(thNeg < th):
            th = thNeg
    
    #Return a tupple if we have a solution and the actual solution (<true/false>,th)
    #th > 0 so we dont account for the ray in the negative direction
    return((dis >= 0) and th>=0,th)


def main(argv):

    #Parse input
    fileName = argv[1]
    print("Opening: ", fileName)
    file = open(fileName,'r')

    lines = file.readlines()

    spheres = []
    #Parse each line and do effect based on token
    for line in lines:
        #print(line)
        line = line.strip("\n")
        tokens = line.split()
        for token in tokens:
            
            if token == "NEAR":
                near = int(tokens[1])

            if token == "LEFT":
                left = int(tokens[1])
            
            if token == "RIGHT":
                right = int(tokens[1])

            if token == "TOP":
                top = int(tokens[1])
            
            if token == "BOTTOM":
                bottom = int(tokens[1])
            
            if token == "RES":
                pixWidth = int(tokens[1])
                pixHeight = int(tokens[2])
                rows = pixWidth - 1
                cols =  pixHeight - 1

            if token == "SPHERE":
                #print(tokens[1:])
                spheres.append(sphere(tokens[1],float(tokens[2]),float(tokens[3]),float(tokens[4]),
                float(tokens[5]),float(tokens[6]),float(tokens[7]),float(tokens[8]),float(tokens[9]),
                float(tokens[10]),float(tokens[11]),float(tokens[12]),float(tokens[13]),float(tokens[14]),float(tokens[15])))
            
            if token == "LIGHT":
                doNothing = True

            if token == "BACK":
                back = color(float(tokens[1]),float(tokens[2]),float(tokens[3]))

            if token == "AMBIENT":
                global sceneAmbience
                sceneAmbience = color(float(tokens[1]),float(tokens[2]),float(tokens[3]))

            if token == "OUTPUT":
                outFileName = tokens[1]
                print("Outputting file as: ",outFileName)

    print("Working....")
    #print(len(spheres))

    #Set up coordinate system 
    eyePos = point3(0,0,0)

    camWidth = 2.0/2.0
    camHeight = 2.0/2.0

    u = vec3(camWidth,0,0)
    v = vec3(0,camHeight,0)
    n = vec3(0,0,near)

    #PPM header setup
    width = pixWidth
    height = pixHeight
    maxval = 255
    ppm_header = f'P6 {width} {height} {maxval}\n'
    
    image = np.ones([1,width*height,3],dtype=np.uint8)

    #Rendering Area - Fire ray through each pixel
    for y in range(pixHeight):
        for x in range(pixWidth):
            index = (y + pixWidth * x)
            uc = left + right*((2*y)/cols)
            vr = bottom + top*((2*x)/rows)

            rayDir =  u*uc + -1*v*vr - n
            rayDir = unitvector(rayDir)

            r = ray(eyePos,rayDir)

            #Decide pixel color based on intersection and color logic in method 
            pixColor = ray_color2(r,back,spheres)
            
            #Turn float "percentage based" color into int based color
            image[0,index] = pixColor*255

    #Flatten numpy array for correct ppm output
    image = image.flatten()

    # Save the PPM image as a binary file
    with open(outFileName, 'wb') as f:
        f.write(bytearray(ppm_header, 'ascii'))
        image.tofile(f) 

    endTime = time.time()

    totalTime = endTime - startTime
    print("Complete! Total time: ", totalTime)
    
if __name__ == "__main__":
    main(sys.argv)