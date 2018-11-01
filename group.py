import sys
assert sys.version_info >= (3,5)

from enum import Enum

class Group():
	"""
	Group of devices, as seen in the control panel in-game.
	"""

	def __init__(self,name="",group_type=None,devices=None):
		self.name=name
		self.group_type=group_type
		self.devices=devices

	class Type(Enum):
		"""
		Indicators for whether a group was created via autogrouping or not.
		"""

		MANUAL=0
		OLD_AUTO=1
		AUTO=256

	def __str__(self):
		device_str=str(None)
		if self.devices is not None:
			device_str=",".join(str(d) for d in self.devices)
		type_str=str(None)
		if self.group_type is not None:
			type_str=self.group_type.name
		return "%s (%s): %s"%(self.name, type_str, device_str)

	def set_type_from_raw(self,raw):
		for enum in Group.Type:
			if enum.value==raw:
				self.group_type=enum
				return
