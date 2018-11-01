import sys
assert sys.version_info >= (3,5)

class Device():
	"""
	Device, as seen in the control panel; includes location.
	"""

	def __init__(self,name="",extra=None,location=(0,0,0)):
		self.name=name
		self.extra=extra
		self.location=location

	def __str__(self):
		return "%s (%s) at %s"%(self.name,str(self.extra),str(self.location))

	def convertLocationFromPacked():
		pass

	def convertLocationToPacked():
		pass
