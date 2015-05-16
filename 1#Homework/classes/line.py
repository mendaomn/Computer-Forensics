class Line(object):
	
		def __init__(self, p1, p2):
			self.m = (p2.y - p1.y) / (p2.x - p1.x)
			self.q = p2.y - (self.m * p2.x)
			self.points = list()
			
		def contains(self, p):
			if (self.m * p.x) + self.q == p.y:
				return True
			return False
			
		def addPoint(self, p):
			points.append(p)
			
		def pointsNumber(self):
			return len(points)
			
		def __str__(self):
			return "y = " + str(self.m) + "x + "+ str(self.q) 
			
