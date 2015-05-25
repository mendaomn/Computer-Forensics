class Line(object):
	def __init__(self, p1, p2):
		self.m = (p2.y - p1.y) / (p2.x - p1.x)
		self.q = p2.y - (self.m * p2.x)
		self.points = list()
		
	def contains(self, p):
		y_ = (self.m * p.x) + self.q
		if abs(y_ - p.y) <= float(self.t):
			return True
		#print (abs(y_ - p.y) - float(self.t)) / 1000000, float(self.t) / 1000000
		return False
		
	def addPoint(self, p):
		points.append(p)
		
	def pointsNumber(self):
		return len(points)
		
	def __str__(self):
		return "y = " + str(self.m) + "x + "+ str(self.q) 
	
	def setThreshold(self, new_t):
		self.t = new_t