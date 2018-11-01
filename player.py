import sys
assert sys.version_info >= (3,5)

class Player():
	"""
	Simple object to hold an player Steam id and display name.
	"""

	def __init__(self,steam_id=0,display_name=""):
		self.steam_id=int(steam_id)
		self.display_name=display_name

	def __str__(self):
		return "%s (%d)"%(self.display_name,self.steam_id)
