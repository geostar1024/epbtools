import sys
assert sys.version_info >= (3,6)

from enum import Enum
import datetime as dt

class Blueprint():
	"""
	Empyrion blueprint object.
	"""

	EPOCH=dt.datetime(1827, 9, 25, 18, 40, 30)

	def __init__(self,name=""):
		self.name=name
		self.version=21 # latest version, need to keep updating
		self.type=Blueprint.Type.BA
		self.dimensions=(1,1,1) # (width, height, length)
		self.grid=None
		self.creator=None
		self.user=None
		self.blocks=0
		self.lights=0
		self.devices=0
		self.triangles=0
		self.eleon_class_size=0
		self.groups=None
		self.game_build=0
		self.block_type_list=None
		self.datetime=None

	class Type(Enum):
		"""
		Blueprint types.
		"""

		VOXEL=0
		BA=2
		SV=4
		CV=8
		HV=16

	def set_type_from_raw(self,raw):
		for enum in Blueprint.Type:
			if enum.value==raw:
				self.type=enum
				return

	def update_eleon_class_size(self):
		self.eleon_class_size=max(round((self.devices*.01+self.lights*.05+self.triangles*0.00025)/3,2),1)

	def list_groups(self):
		if self.groups is not None:
			for group in self.groups:
				print(group)

	def list_properties(self):
		"""
		Prints out a formatted list of the blueprint's properties
		"""

		width=25
		print(f"{'name:':<{width}} {self.name}")
		print(f"{'structure type:':<{width}} {self.type.name}")
		print(f"{'epb version:':<{width}} {self.version}")
		print(f"{'dimensions:':<{width}} {self.dimensions}")
		print(f"{'datetime:':<{width}} {self.datetime}")
		print(f"{'creator:':<{width}} {self.creator}")
		print(f"{'current user:':<{width}} {self.user}")
		print(f"{'number of blocks:':<{width}} {self.blocks}")
		print(f"{'number of devices:':<{width}} {self.devices}")
		print(f"{'number of lights:':<{width}} {self.lights}")
		print(f"{'number of triangles:':<{width}} {self.triangles}")
		print(f"{'eleon class size:':<{width}} {self.eleon_class_size}")
		if self.groups is None:
			print(f"{'number of groups:':<{width}} {0}")
		else:
			print(f"{'number of groups:':<{width}} {len(self.groups)}")

