from Disk import VirtualDisk
from Disk import PhysicalDisk
from Disk import *
import random
import bisect

class PhysicalReplicaDisk(PhysicalDisk):
	physical_replica_disks = []

	def __init__(self, num_blocks):
		PhysicalDisk.__init__(self, num_blocks)
		self.bad_blocks = []
		self.physical_replica_disks.append(self)

	def read(self, block_num, turn):
		if turn==1:
			rand = random.randint(1, 100)
			if rand<10:
				bisect.insort(self.bad_blocks, block_num)
				return None
		return ''.join(self.data[block_num])


class VirtualReplicaDisk(VirtualDisk):
	virtual_replica_disks = {}

	def __init__(self, Id, num_blocks, disks):
		VirtualDisk.__init__(self, Id, num_blocks, disks)
		self.virtual_replica_disks[Id] = self

	def allocate(self):
		total_free_space = sum([disk.num_free_blocks for disk in self.disks])
		if(total_free_space<2*self.num_blocks):
			print("ERROR: Not enough free space on the physical disks.")
			return
		mapping = VirtualDisk.allocate(self)
		copy_mapping = VirtualDisk.allocate(self)
		return (mapping, copy_mapping)

	def remove(self):
		for i in self.mapping:
			for m in i:
				self.disks[m[0]].free(m[1], m[2])

	def read(self, block_num):
		if(self.num_blocks > block_num):
			print("ERROR: Block index out of range")
			return ""
		b = find_physical_block(self.mapping[0], block_num)
		ans = b[0].read(b[1], 1)
		if ans==None:
			print("first read failed")
			b = find_physical_block(self.mapping[1], block_num)
			ans = b[0].read(b[1], 2)
			blck = allocate_best_block(1, self.disks) 	# disk_no, start, size
			# make a new mapping for this block 
			self.change_mapping(block_num, blck)
			# copy the data there
			self.disks[blck[0]].write(blck[1], ans)
		return ans 
	
	def change_mapping(self, blck):
		# only for a single block i.e blck[2]=1
		i = block_num
		for ind in range(len(self.mapping[0])):
			m = self.mapping[0][ind]
			if(m[2]==1 and i==0):
				self.mapping[0][ind] = blck
				return
			elif(m[2]-1 == i):
				self.mapping[0][ind][2] -= 1
				# also check if it merges with the right block
				if(ind+2<len(self.mapping[0]) and self.mapping[0][ind+2][0]==blck[0] and self.mapping[0][ind+2][1]==blck[1]+1):
					self.mapping[0][ind+2][1] -= 1
				else:
					self.mapping[0].insert(ind+1, blck)	
				return
			elif(i==0):
				self.mapping[0][ind][1] += 1
				# check if it merges on the left
				if(ind-1>=0 and self.mapping[0][ind-1][0]==blck[0] and (self.mapping[0][ind-1][1] + self.mapping[0][ind-1][2]==blck[1])):
					self.mapping[0][ind-1][2] += 1
				else:
					self.mapping[0].insert(ind, blck)
				return
			elif(m[2]>i):
				self.mapping[0][ind][2] = i
				self.mapping[0].insert(ind+1, blck)
				self.mapping[0].insert(ind+2, (m[0], m[1]+i+1, m[2]-i-1))
			i -= m[2]

	def write(self, block_num, write_data):
		if(self.num_blocks > block_num):
			print("ERROR: Block index out of range")
			return ""
		for maps in self.mapping:
			b = find_physical_block(map, block_num)
			b[0].write(b[1])


def CreateDisk(Id, num_blocks):
	return VirtualReplicaDisk(Id, num_blocks, PhysicalReplicaDisk.physical_replica_disks)

def DeleteDisk(Id):
	VirtualReplicaDisk.virtual_replica_disks[Id].remove()
	

def Read(Id, block_num):
	return VirtualReplicaDisk.virtual_replica_disks[Id].read(block_num)

def Write(Id, block_num, write_data):
	VirtualReplicaDisk.virtual_replica_disks[Id].write(block_num, write_data)


# initialisation
INFINITY = 10000000
disk_sizes = [200, 300]
disks = [PhysicalReplicaDisk(x) for x in disk_sizes]

print(disks[0]),
print(", "),
print(disks[1])

d1 = CreateDisk(1, 110)

# d2 = CreateDisk(2, 50)
# d1.test_changes()


print(disks[0]),
print(", "),
print(disks[1])

# DeleteDisk(1)

# print(disks[0]),
# print(", "),
# print(disks[1])


print()
# print(len(VirtualDisk.virtual_disks))