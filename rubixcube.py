#!/usr/bin/python

"""
Corner pieces:
-1 of 8 positions
-3 colors
-3 orientations

Center pieces:
-1 of 4 positions
-1 color
-1 orientation

Edge Pieces:
-1 of 12 positions
-2 colors
-2 orientations

Total Colors:
-Red
-Blue
-Green
-Yellow
-Orange
-White
"""

#=============#
#   imports   #
#=============#

import random

#====================#
#   custom classes   #
#====================#

class Color:
	def __init__(self,colorName):
		self.colorName = colorName
	def __str__(self):
		return self.getColorInitial()
	def getColorInitial(self):
		return self.colorName[0].upper()
	def getColorName(self):
		return self.colorName

class CornerBlock:
	def __init__(self, color1, color2, color3):
		self.colors = []
		self.colors.append(color1)
		self.colors.append(color2)
		self.colors.append(color3)
	def getColor(self,colorNumber):
		return self.colors[colorNumber]
	def randomize(self):
		random.shuffle(self.colors)
	def swapColors(self,colorNumber1,colorNumber2):
		self.colors[colorNumber2],self.colors[colorNumber1] = self.colors[colorNumber1],self.colors[colorNumber2]

class CenterBlock:
	def __init__(self, color):
		self.color = color
	def getColor(self):
		return self.color

class EdgeBlock:
	def __init__(self, color1, color2):
		self.colors = []
		self.colors.append(color1)
		self.colors.append(color2)
	def getColor(self,colorNumber):
		return self.colors[colorNumber]
	def randomize(self):
		random.shuffle(self.colors)
	def swapColors(self):
		self.colors[1],self.colors[0] = self.colors[0],self.colors[1]

class Side:
	def __init__(self,centerColor,cornerColors,edgeColors):
		self.centerColor = centerColor
		self.cornerColors = cornerColors
		self.edgeColors = edgeColors
	def __str__(self):
		return "%s\t%s\t%s\n%s\t%s\t%s\n%s\t%s\t%s\n" % (self.cornerColors[1],self.edgeColors[0],self.cornerColors[0],
		                                                 self.edgeColors[1],self.centerColor,self.edgeColors[3],
		                                                 self.cornerColors[2],self.edgeColors[2],self.cornerColors[3])
	def getRow(self,rowNumber):
		if(rowNumber == 0):
			row = (self.cornerColors[1],self.edgeColors[0],self.cornerColors[0])
		elif(rowNumber == 1):
			row = (self.edgeColors[1],self.centerColor,self.edgeColors[3])
		elif(rowNumber == 2):
			row = (self.cornerColors[2],self.edgeColors[2],self.cornerColors[3])
		else:
			raise Exception("ERROR: Invalid row number")
		return row
	
	def getColumn(self,colNumber):
		if(colNumber == 0):
			col = (self.cornerColors[1],self.edgeColors[1],self.cornerColors[2])
		elif(colNumber == 1):
			col = (self.edgeColors[0],self.centerColor,self.edgeColors[2])
		elif(colNumber == 2):
			col = (self.cornerColors[0],self.edgeColors[3],self.cornerColors[3])
		else:
			raise Exception("ERROR: Invalid column number")
		return col

class RubixCube:
	#setup colors
	RED = Color("red")
	BLUE = Color("blue")
	GREEN = Color("green")
	YELLOW = Color("yellow")
	ORANGE = Color("orange")
	WHITE = Color("white")

	#block colors
	CORNER_COLORS = [(BLUE,ORANGE,WHITE),
	                 (BLUE,ORANGE,RED),
	                 (BLUE,RED,YELLOW),
	                 (BLUE,YELLOW,WHITE),
	                 (GREEN,ORANGE,WHITE),
	                 (GREEN,ORANGE,RED),
	                 (GREEN,RED,YELLOW),
	                 (GREEN,YELLOW,WHITE)]
	CENTER_COLORS = [BLUE,ORANGE,RED,YELLOW,WHITE,GREEN]
	EDGE_COLORS = [(BLUE,ORANGE),
	               (BLUE,RED),
	               (BLUE,YELLOW),
	               (BLUE,WHITE),
	               (GREEN,ORANGE),
	               (GREEN,RED),
	               (GREEN,YELLOW),
	               (GREEN,WHITE),
	               (ORANGE,RED),
	               (RED,YELLOW),
	               (YELLOW,WHITE),
	               (WHITE,ORANGE)]
	
	def __init__(self):
		#initialize local vars
		self.corners = []
		self.centers = []
		self.edges = []
		
		#create corner blocks
		for colors in self.CORNER_COLORS:
			self.corners.append(CornerBlock(colors[0],colors[1],colors[2]))
		
		#create center blocks
		for color in self.CENTER_COLORS:
			self.centers.append(CenterBlock(color))
		
		for colors in self.EDGE_COLORS:
			self.edges.append(EdgeBlock(colors[0],colors[1]))
	
	def __str__(self):
		#get all sides
		top = self.getSide(0)
		back = self.getSide(1)
		left = self.getSide(2)
		front = self.getSide(3)
		right = self.getSide(4)
		bottom = self.getSide(5)
		
		#get the format string
		oneSideString = "    %s%s%s\n    %s%s%s\n    %s%s%s\n"
		threeSideString = "%s%s%s %s%s%s %s%s%s\n%s%s%s %s%s%s %s%s%s\n%s%s%s %s%s%s %s%s%s\n"
		formatString = "%s\n%s\n%s\n%s\n%s" % (oneSideString,oneSideString,threeSideString,oneSideString,oneSideString[:-1])
		
		#get the format string arguments
		arguments = []
		arguments += bottom.getRow(0) + bottom.getRow(1) + bottom.getRow(2)
		arguments += back.getRow(0) + back.getRow(1) + back.getRow(2)
		arguments += left.getRow(0) + top.getRow(0) + right.getRow(0)
		arguments += left.getRow(1) + top.getRow(1) + right.getRow(1)
		arguments += left.getRow(2) + top.getRow(2) + right.getRow(2)
		arguments += front.getRow(0) + front.getRow(1) + front.getRow(2)
		arguments += bottom.getRow(0) + bottom.getRow(1) + bottom.getRow(2)
		
		#return formatString
		
		#build the return string
		returnString = formatString % tuple(arguments)
		return returnString
	
	def randomize(self):
		#randomizes the cube
		
		#randomize the block orientation
		for corner in self.corners:
			corner.randomize()
		for edge in self.edges:
			edge.randomize()
		
		#randomize the block positions
		random.shuffle(self.corners)
		random.shuffle(self.edges)
	
	def getSide(self,sideNumber):
		#map sides to corners and edges
		if(sideNumber == 0):
			cornerCoords = [(0,0),(1,0),(2,0),(3,0)]
			edgeCoords = [(0,0),(1,0),(2,0),(3,0)]
		elif(sideNumber == 1):
			cornerCoords = [(4,1),(5,1),(1,1),(0,1)]
			edgeCoords = [(4,1),(8,0),(0,1),(11,1)]
		elif(sideNumber == 2):
			cornerCoords = [(1,2),(5,2),(6,1),(2,1)]
			edgeCoords = [(8,1),(5,1),(9,0),(1,1)]
		elif(sideNumber == 3):
			cornerCoords = [(3,1),(2,2),(6,2),(7,1)]
			edgeCoords = [(2,1),(9,1),(6,1),(10,0)]
		elif(sideNumber == 4):
			cornerCoords = [(4,2),(0,2),(3,2),(7,2)]
			edgeCoords = [(11,0),(3,1),(10,1),(7,1)]
		elif(sideNumber == 5):
			cornerCoords = [(7,0),(6,0),(5,0),(4,0)]
			edgeCoords = [(6,0),(5,0),(4,0),(7,0)]
		else:
			raise Exception("ERROR: Invalid side number")
		
		#get colors
		cornerColors = []
		edgeColors = []
		centerColor = self.centers[sideNumber].getColor()
		for corner,color in cornerCoords:
			cornerColors.append(self.corners[corner].getColor(color))
		for edge,color in edgeCoords:
			edgeColors.append(self.edges[edge].getColor(color))
		
		return Side(centerColor,cornerColors,edgeColors)
		
	def rotateSide(self,sideNumber,direction):
		if(direction == "clockwise"):
			if(sideNumber == 0):
				#rearrange the corners
				self.corners[1],self.corners[0] = self.corners[0],self.corners[1]
				self.corners[2],self.corners[1] = self.corners[1],self.corners[2]
				self.corners[3],self.corners[2] = self.corners[2],self.corners[3]
				self.corners[0].swapColors(1,2)
				self.corners[3].swapColors(1,2)
				
				#rearrange the edges
				self.edges[1],self.edges[0] = self.edges[0],self.edges[1]
				self.edges[2],self.edges[1] = self.edges[1],self.edges[2]
				self.edges[3],self.edges[2] = self.edges[2],self.edges[3]
			elif(sideNumber == 1):
				#rearrange the corners
				self.corners[5],self.corners[4] = self.corners[4],self.corners[5]
				self.corners[1],self.corners[5] = self.corners[5],self.corners[1]
				self.corners[0],self.corners[1] = self.corners[1],self.corners[0]
				self.corners[4].swapColors(0,2)
				self.corners[0].swapColors(0,2)
				self.corners[5].swapColors(0,2)
				self.corners[1].swapColors(0,2)
				
				#rearrange the edges
				self.edges[8],self.edges[4] = self.edges[4],self.edges[8]
				self.edges[0],self.edges[8] = self.edges[8],self.edges[0]
				self.edges[11],self.edges[0] = self.edges[0],self.edges[11]
				self.edges[8].swapColors()
				self.edges[4].swapColors()
			elif(sideNumber == 2):
				#rearrange the corners
				self.corners[5],self.corners[1] = self.corners[1],self.corners[5]
				self.corners[6],self.corners[5] = self.corners[5],self.corners[6]
				self.corners[2],self.corners[6] = self.corners[6],self.corners[2]
				self.corners[1].swapColors(1,0)
				self.corners[2].swapColors(1,2)
				self.corners[2].swapColors(0,2)
				self.corners[6].swapColors(0,2)
				self.corners[5].swapColors(0,2)
				self.corners[5].swapColors(1,2)
				
				#rearrange the edges
				self.edges[5],self.edges[8] = self.edges[8],self.edges[5]
				self.edges[9],self.edges[5] = self.edges[5],self.edges[9]
				self.edges[1],self.edges[9] = self.edges[9],self.edges[1]
				self.edges[5].swapColors()
				self.edges[9].swapColors()
			elif(sideNumber == 3):
				#rearrange the corners
				self.corners[2],self.corners[3] = self.corners[3],self.corners[2]
				self.corners[6],self.corners[2] = self.corners[2],self.corners[6]
				self.corners[7],self.corners[6] = self.corners[6],self.corners[7]
				self.corners[3].swapColors(1,2)
				self.corners[3].swapColors(0,2)
				self.corners[6].swapColors(1,2)
				self.corners[6].swapColors(0,1)
				self.corners[2].swapColors(0,1)
				self.corners[7].swapColors(0,2)
				
				#rearrange the edges
				self.edges[9],self.edges[2] = self.edges[2],self.edges[9]
				self.edges[6],self.edges[9] = self.edges[9],self.edges[6]
				self.edges[10],self.edges[6] = self.edges[6],self.edges[10]
				self.edges[6].swapColors()
				self.edges[10].swapColors()
			elif(sideNumber == 4):
				#rearrange the corners
				self.corners[0],self.corners[4] = self.corners[4],self.corners[0]
				self.corners[3],self.corners[0] = self.corners[0],self.corners[3]
				self.corners[7],self.corners[3] = self.corners[3],self.corners[7]
				self.corners[4].swapColors(1,0)
				self.corners[0].swapColors(0,1)
				self.corners[3].swapColors(1,0)
				self.corners[7].swapColors(0,1)
				
				#rearrange the edges
				self.edges[3],self.edges[11] = self.edges[11],self.edges[3]
				self.edges[10],self.edges[3] = self.edges[3],self.edges[10]
				self.edges[7],self.edges[10] = self.edges[10],self.edges[7]
				self.edges[7].swapColors()
				self.edges[11].swapColors()
			elif(sideNumber == 5):
				#rearrange the corners
				self.corners[6],self.corners[7] = self.corners[7],self.corners[6]
				self.corners[5],self.corners[6] = self.corners[6],self.corners[5]
				self.corners[4],self.corners[5] = self.corners[5],self.corners[4]
				self.corners[5].swapColors(1,2)
				self.corners[4].swapColors(2,1)
				
				#rearrange the edges
				self.edges[5],self.edges[6] = self.edges[6],self.edges[5]
				self.edges[4],self.edges[5] = self.edges[5],self.edges[4]
				self.edges[7],self.edges[4] = self.edges[4],self.edges[7]
			else:
				raise Exception("ERROR: Invalid side number")
		elif(direction == "counter-clockwise"):
			if(sideNumber == 0):
				#rearrange the corners
				self.corners[3],self.corners[2] = self.corners[2],self.corners[3]
				self.corners[2],self.corners[1] = self.corners[1],self.corners[2]
				self.corners[1],self.corners[0] = self.corners[0],self.corners[1]
				self.corners[0].swapColors(1,2)
				self.corners[1].swapColors(1,2)
				
				#rearrange the edges
				self.edges[3],self.edges[2] = self.edges[2],self.edges[3]
				self.edges[2],self.edges[1] = self.edges[1],self.edges[2]
				self.edges[1],self.edges[0] = self.edges[0],self.edges[1]
			elif(sideNumber == 1):
				#rearrange the corners
				self.corners[0],self.corners[1] = self.corners[1],self.corners[0]
				self.corners[1],self.corners[5] = self.corners[5],self.corners[1]
				self.corners[5],self.corners[4] = self.corners[4],self.corners[5]
				self.corners[4].swapColors(0,2)
				self.corners[0].swapColors(0,2)
				self.corners[5].swapColors(0,2)
				self.corners[1].swapColors(0,2)
				
				#rearrange the edges
				self.edges[11],self.edges[0] = self.edges[0],self.edges[11]
				self.edges[0],self.edges[8] = self.edges[8],self.edges[0]
				self.edges[8],self.edges[4] = self.edges[4],self.edges[8]
				self.edges[0].swapColors()
				self.edges[8].swapColors()
			elif(sideNumber == 2):
				#rearrange the corners
				self.corners[2],self.corners[6] = self.corners[6],self.corners[2]
				self.corners[6],self.corners[5] = self.corners[5],self.corners[6]
				self.corners[5],self.corners[1] = self.corners[1],self.corners[5]
				self.corners[1].swapColors(2,0)
				self.corners[1].swapColors(1,2)
				self.corners[6].swapColors(1,2)
				self.corners[6].swapColors(0,2)
				self.corners[5].swapColors(0,1)
				self.corners[2].swapColors(0,2)
				
				#rearrange the edges
				self.edges[1],self.edges[9] = self.edges[9],self.edges[1]
				self.edges[9],self.edges[5] = self.edges[5],self.edges[9]
				self.edges[5],self.edges[8] = self.edges[8],self.edges[5]
				self.edges[1].swapColors()
				self.edges[9].swapColors()
			elif(sideNumber == 3):
				#rearrange the corners
				self.corners[7],self.corners[6] = self.corners[6],self.corners[7]
				self.corners[6],self.corners[2] = self.corners[2],self.corners[6]
				self.corners[2],self.corners[3] = self.corners[3],self.corners[2]
				self.corners[3].swapColors(0,2)
				self.corners[2].swapColors(1,2)
				self.corners[2].swapColors(1,0)
				self.corners[6].swapColors(0,1)
				self.corners[7].swapColors(2,1)
				self.corners[7].swapColors(0,2)
				
				#rearrange the edges
				self.edges[10],self.edges[6] = self.edges[6],self.edges[10]
				self.edges[6],self.edges[9] = self.edges[9],self.edges[6]
				self.edges[9],self.edges[2] = self.edges[2],self.edges[9]
				self.edges[2].swapColors()
				self.edges[10].swapColors()
			elif(sideNumber == 4):
				#rearrange the corners
				self.corners[7],self.corners[3] = self.corners[3],self.corners[7]
				self.corners[3],self.corners[0] = self.corners[0],self.corners[3]
				self.corners[0],self.corners[4] = self.corners[4],self.corners[0]
				self.corners[4].swapColors(1,0)
				self.corners[0].swapColors(0,1)
				self.corners[3].swapColors(1,0)
				self.corners[7].swapColors(0,1)
				
				#rearrange the edges
				self.edges[7],self.edges[10] = self.edges[10],self.edges[7]
				self.edges[10],self.edges[3] = self.edges[3],self.edges[10]
				self.edges[3],self.edges[11] = self.edges[11],self.edges[3]
				self.edges[3].swapColors()
				self.edges[11].swapColors()
			elif(sideNumber == 5):
				#rearrange the corners
				self.corners[4],self.corners[5] = self.corners[5],self.corners[4]
				self.corners[5],self.corners[6] = self.corners[6],self.corners[5]
				self.corners[6],self.corners[7] = self.corners[7],self.corners[6]
				self.corners[7].swapColors(1,2)
				self.corners[4].swapColors(2,1)
				
				#rearrange the edges
				self.edges[7],self.edges[4] = self.edges[4],self.edges[7]
				self.edges[4],self.edges[5] = self.edges[5],self.edges[4]
				self.edges[5],self.edges[6] = self.edges[6],self.edges[5]
			else:
				raise Exception("ERROR: Invalid side number")
		else:
			raise Exception("ERROR: Invalid direction")

#==========#
#   main   #
#==========#

def main():
	myRubixCube = RubixCube()
	print myRubixCube
	myRubixCube.randomize()
	
	while True:
		print "-----------"
		print myRubixCube
		
		#get side to rotate from user
		simonSays = raw_input("Choose a side to rotate by entering the center color:")
		if(simonSays[0].upper() == 'B'):
			side = 0
		elif(simonSays[0].upper() == 'O'):
			side = 1
		elif(simonSays[0].upper() == 'R'):
			side = 2
		elif(simonSays[0].upper() == 'Y'):
			side = 3
		elif(simonSays[0].upper() == 'W'):
			side = 4
		elif(simonSays[0].upper() == 'G'):
			side = 5
		elif(simonSays.upper() == "EXIT"):
			break
		else:
			side = None
		
		#get direction
		if(side != None):
			simonSays = raw_input("Choose a direction to rotate - 1)Clockwise 2)Counter-clockwise:")
			if(simonSays[0] == '1'):
				direction = "clockwise"
			else:
				direction = "counter-clockwise"
			myRubixCube.rotateSide(side,direction)
		else:
			print "Sorry, I didn't understand that color"



#code to run main upon execution of program
if __name__=='__main__':
	main()
