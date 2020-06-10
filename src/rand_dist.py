#!/bin/python3
################################################################################

import os
import sys
import time
import hashlib
import math

class rand_dist:

  def __init__(self, seed=None):
    # RNG vars
    if seed is None:
      self.seed = 12791244
    else:
      self.seed = seed
    self.xn = self.seed
    self.m = 4294967296
    self.a = 1103515245
    self.c = 12345
    #Dist Type vars
    self.lower = 0.0e0
    self.upper = 1.0e0
    self.distType = "flat"
    # make a new distribution table
    self.table = RandDistTable()
    
  def setSeed(self, seed):
    self.seed = seed

  def randomSeed(self):
    currentTime = time.time()
    myhash = hashlib.md5()
    message = "randnum"+str(currentTime)
    myhash.update(message.encode())
    seed = myhash.hexdigest()
    seedInt = int("0x"+seed[0:8],0)
    self.xn = (self.xn + seedInt) % self.m

  def setRange(self,lower,upper):
    self.lower = lower
    self.upper = upper

  def flat(self):
    self.distType = "flat"
    self.table.set = False

  def sqrt(self):
    self.distType = "sqrt"
    self.table.set = False

  def gheat(self, lower=-1.0e0, upper=1.0e0, p1=1.0, p2=0.0, p3=1.0, p4=4.0):
    self.distType = "gheat"
    self.table.set = False
    self.lower = lower
    self.upper = upper
    self.p1 = p1  # sigma
    self.p2 = p2  # mu
    self.p3 = p3  # factor
    self.p4 = p4  # factor

  def doubleGaussian(self, lower=-1.0e0, upper=1.0e0, p1=1.0, p2=0.0, p3=1.0, p4=4.0, p5=1.5, p6=0.8, p7=1.0, p8=4.0):
    self.distType = "doubleGaussian"
    self.table.set = False
    self.lower = lower
    self.upper = upper
    self.p1 = p1
    self.p2 = p2
    self.p3 = p3
    self.p4 = p4
    self.p5 = p5
    self.p6 = p6
    self.p7 = p7
    self.p8 = p8

  def getFloat(self):
    # Get a random float between 0 and 1
    self.xn = (self.a * self.xn + self.c) % self.m
    randFloat = self.xn / self.m
    return randFloat

  def rng(self):
    # Choose function
    if(self.distType=="flat"):
      self.randFloat = self.getFloat()
      randOut = self.lower + self.randFloat * (self.upper - self.lower)
    # Square root
    if(self.distType=="sqrt"):
      self.randFloat = self.getFloat()
      randOut = self.lower + self.randFloat * (self.upper - self.lower)
      randOut = math.sqrt(abs(randOut))
    # gheat
    if(self.distType=="gheat"):
      randOut = self.randDistF()
    # doubleGaussian
    if(self.distType=="doubleGaussian"):
      randOut = self.randDistF()
    # store and return output
    self.randOut = randOut
    return randOut

  def randDistF(self):
    # If a table hasn't been built for the function, build it now
    if(self.table.set==False):
      self.rand_MakeTable()
      #self.table.display()

    # Loop attempts
    loopTrials = True
    i = 0
    while(loopTrials and i<10000):
      i = i + 1
      randA = self.getFloat()  # Block
      randB = self.getFloat()  # xVal
      randC = self.getFloat()  # yVal
      if(randA==0):
        randBlock = 0
      else:
        randBlock = math.ceil(randA * self.table.size)-1
      xA = self.table.points_xA[randBlock]
      x_m = self.table.points_x_m[randBlock]
      xB = self.table.points_xB[randBlock]
      yA = self.table.points_yA[randBlock]
      y_m = self.table.points_y_m[randBlock]
      yB = self.table.points_yB[randBlock]
      yMax = self.table.points_yMax[randBlock]
      # set x,y coords
      x = xA + randB * (xB - xA)
      y = randC * yMax
      # Set up list
      interpPoints = [[0 for x in range(2)] for y in range(3)]
      interpPoints[0][0] = xA
      interpPoints[0][1] = yA
      interpPoints[1][0] = x_m
      interpPoints[1][1] = y_m
      interpPoints[2][0] = xB
      interpPoints[2][1] = yB
      # Interp
      fx = self.interp(x,interpPoints)
      if(y<=fx):
        loopTrials = False
      randNumber = x

    return randNumber

  def rand_MakeTable(self):
    # Calculate total area under function
    self.table.initPoints(256)
    randRange = self.upper - self.lower
    xInc = randRange / (self.table.targetSize - 1)
    xA = self.lower
    xB = xA + xInc
    area = 0.0
    for i in range(0,self.table.targetSize):
### Choose function
###---------------------------------------------
      if(self.distType=="gheat"):
        yA = self.rand_Gaussian(xA)
        yB = self.rand_Gaussian(xB)
      if(self.distType=="doubleGaussian"):
        yA = self.rand_DoubleGaussian(xA)
        yB = self.rand_DoubleGaussian(xB)
###--------------------------------------------
      # Calc area
      area = area + 0.5 * xInc * (yA + yB)
      # Increment
      xA = xB
      xB = xA + xInc
    # Area when split into blocks
    blockArea = area / self.table.targetSize
    xA = self.lower
    runLoop = True
    i = 0
    while(runLoop):
      i = i + 1
### Choose function
###---------------------------------------------
      if(self.distType=="gheat"):
        yA = self.rand_Gaussian(xA)
      if(self.distType=="doubleGaussian"):
        yA = self.rand_DoubleGaussian(xA)
###--------------------------------------------
# Find xB
      xInc = randRange * 0.0001
      xB = xA
      area = 0.0
      yMax = yA
      findArea = True
      while(findArea):
        xB = xB + xInc
        yB = self.rand_Gaussian(xB)
        if(yB>yA):
          yMax = yB
        area = area + 0.5 * xInc * yMax
        if(area>blockArea):
          findArea = False # Area has been found
      xB = xA + blockArea / yMax
      if(xB>self.upper):
        xB = self.upper
        yMax = area/(xB - xA)
        runLoop = False
        # set table size
        self.table.size = i
      #Run calculations
### Choose function
###--------------------------------------------
      x_m = 0.5 * (xA + xB)
      if(self.distType=="gheat"):
        yA = self.rand_Gaussian(xA)
        y_m = self.rand_Gaussian(x_m)
        yB = self.rand_Gaussian(xB)
      if(self.distType=="doubleGaussian"):
        yA = self.rand_DoubleGaussian(xA)
        y_m = self.rand_DoubleGaussian(x_m)
        yB = self.rand_DoubleGaussian(xB)
###--------------------------------------------
      # Store data points
      self.table.points_yMax.append(yMax)
      self.table.points_xA.append(xA)
      self.table.points_x_m.append(x_m)
      self.table.points_xB.append(xB)
      self.table.points_yA.append(yA)
      self.table.points_y_m.append(y_m)
      self.table.points_yB.append(yB)
      # Set xA for next loop
      xA = xB
    # Set table to true
    self.table.set = True

  def rand_Gaussian(self, x):
    fx = self.p3 * (0.398942 / self.p1)
    expV = (-0.5/(self.p1*self.p1)) * (self.p4 * self.p4 * (x - self.p2) * (x - self.p2))
    fx = fx * math.exp(expV)
    return fx

  def rand_DoubleGaussian(self, x):
    fxA = self.p3 * (0.398942 / self.p1)
    expV = (-0.5/(self.p1*self.p1)) * (self.p4 * self.p4 * (x - self.p2) * (x - self.p2))
    fxA = fxA * math.exp(expV)
    fxB = self.p7 * (0.398942 / self.p5)
    expV = (-0.5/(self.p5*self.p5)) * (self.p8 * self.p8 * (x - self.p6) * (x - self.p6))
    fxB = fxB * math.exp(expV)
    fx = fxA + fxB
    return fx

  def makeTally(self, tallySize=50, sampleSize=100000):
    # Declare list
    self.tally = []
    self.tallyX = []
    self.tallySize = tallySize
    sampleSize = 100000
    self.sampleSize = sampleSize
    halfIncrement = (self.upper - self.lower) / (2 * tallySize)
    # Loop through
    for i in range(0,tallySize):
      self.tally.append(0)
      xVal = self.lower + (2 * i + 1) * halfIncrement
      self.tallyX.append(xVal)
    for i in range(0,self.sampleSize):
      randNum = self.rng()
      binNum = randNum - self.lower
      binNum = binNum / (self.upper - self.lower)
      binNum = math.floor(binNum * tallySize)
      # Force to be in range
      if(binNum>=tallySize):
        binNum = tallySize - 1
      if(binNum<0):
        binNum = 0
      self.tally[binNum] = self.tally[binNum] + 1

  def displayTally(self):
    print("==============================")
    print("     Tally: ",self.distType)
    print("==============================")
    for i in range(0,self.tallySize):
      #print(i,"  ",self.tally[i],"  ",self.tallyX[i],"  ",self.tally[i])
      print('{0:3G},{1:8G},{2:5f},{3:8G}'.format(i,self.tally[i],self.tallyX[i],self.tally[i]))
    print("==============================")
    print()


  @staticmethod
  def interp(x, points):
    # Lagrange interpolation
    output = 0.0
    count = len(points)
    coefficients = []
    # Make coefficients
    for i in range(0,count):
      numerator = 1.0
      denominator = 1.0
      for j in range(0,count):
        if(i!=j):
          numerator = numerator * (x - points[j][0])
          denominator = denominator * (points[i][0] - points[j][0])
      coefficients.append(numerator/denominator)
    # Calculate y
    y = 0
    for i in range(0,count):
      y = y + points[i][1] * coefficients[i]
    return y



class RandDistTable:
  def __init__(self):
    self.set = False

  def initPoints(self,targetSize=256):
    self.size = 0
    self.targetSize = targetSize
    self.points_yMax = []
    self.points_xA = []
    self.points_x_m = []
    self.points_xB = []
    self.points_yA = []
    self.points_y_m = []
    self.points_yB = []

  def display(self):
    print("======================")
    print("        Table         ")
    print("======================")
    print("Size:   ", self.size )
    print("")
    for i in range(0,self.size):
      print(i,"     ",end="")
      print(self.points_yMax[i],"     ",end="")
      print(self.points_xA[i],self.points_x_m[i],self.points_xB[i],"",sep="    ",end="")
      print(self.points_yA[i],self.points_y_m[i],self.points_yB[i],"",sep="    ",end="\n")
    print("")
    print("")
    print("======================")




############################################################
# Random Number Generator (testing)
############################################################


class Test_RandDist:

  @staticmethod
  def testRandFloatSingle():
    rd = rand_dist()
    print(rd.rng())
    print(rd.rng())
    print(rd.rng())
    rd.randomSeed()
    print(rd.rng())
    print(rd.rng())
    print(rd.rng())


  @staticmethod
  def testRandFloat():
    rd = rand_dist()
    rd.makeTally()
    rd.displayTally()

  @staticmethod
  def testRandSqrt():
    rd = rand_dist()
    rd.sqrt()
    rd.makeTally()
    rd.displayTally()

  @staticmethod
  def testRandGheat():
    rd = rand_dist()
    rd.gheat(-1.0,1.0,1.0,0.0,1.0,4.0)
    rd.makeTally()
    rd.displayTally()

  @staticmethod
  def testRandDoublegaussian():
    rd = rand_dist()
    rd.doubleGaussian(-1.0,1.0,1.0,0.0,1.0,4.0,1.5,0.8,1.0,4.0)
    rd.makeTally()
    rd.displayTally()



