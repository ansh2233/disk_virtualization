class Block():
	def __init__(self):
		self.data = ['' for i in range(100)]

class PhysicalDisk:
	physical_disks = []

	def __init__(self, num_blocks):
		self.num_blocks = num_blocks
		self.data = [Block for i in range(num_blocks)]
		self.free_blocks = [(0, num_blocks)]	# free space in tuples (start, size)
		self.num_free_blocks = num_blocks
		self.physical_disks.append(self)

	def free(self, start, num_blocks):
		self.num_free_blocks += num_blocks
		# check if it is already empty
		ind = 0
		left = False
		right = False
		for i in range(len(self.free_blocks)):
			b = self.free_blocks[i]
			if(b[0]>start+num_blocks-1):
				if(i-1>=0):
					l = self.free_blocks[i-1]
					if(l[0]+l[1]==start):
						left = True
				if(i+1<len(self.free_blocks)):
					l = self.free_blocks[i+1]
					if(l[0]==start+num_blocks):
						right = True
				break
			if(b[0]+b[1]-1<start):
				ind += 1
		# add (start, num_blocks) at index ind 
		if(left and right):
			bl = self.free_blocks[ind-1]
			br = self.free_blocks[ind]
			self.free_blocks[ind-1] = (bl[0], bl[0]+num_blocks+br[1])
			self.free_blocks.remove(br)
		elif(left):
			b = self.free_blocks[ind-1]
			self.free_blocks[ind-1] = (b[0], b[1] + num_blocks)
		elif(right):
			b = self.free_blocks[ind]
			self.free_blocks[ind] = (b[0] - num_blocks, b[1])
		else:
			self.free_blocks.insert(ind, (start, num_blocks))

	def remove(self, start, num_blocks):
		self.num_free_blocks -= num_blocks
		for i in range(len(self.free_blocks)):
			b = self.free_blocks[i]
			if(b[0]==start):
				if(b[1]==num_blocks):
					self.free_blocks.remove(b)
				elif(b[1]>num_blocks):
					self.free_blocks[i] = (b[0]+num_blocks, b[1]-num_blocks)
				else:
					print("ERROR: Something wrong happened. Check allocate_best_block call")

	def read(self, block_num):
		return ''.join(self.data[block_num])

	def write(self, block_num, write_data):
		array = ['' for i in range(100)]
		for i in range(len(write_data)):
			array[i] = write_data[i]
		self.data[block_num].data = array

	def __repr__(self):
		return (str(self.num_free_blocks) + " free out of " + str(self.num_blocks) + ". { " + str(self.free_blocks) + " }")

class VirtualDisk:
	virtual_disks = {}

	def __init__(self, Id, num_blocks, disks):
		if(self.virtual_disks.has_key(Id)):
			print("ERROR: Disk with Id=" + str(Id) + " already exists")
			return
		self.Id = Id
		self.disks = disks
		self.num_blocks = num_blocks
		self.mapping = self.allocate()	# tuples of (disk_no, start, size)
		self.virtual_disks[Id] = self

	def allocate(self):
		mapping = []
		total_free_space = sum([disk.num_free_blocks for disk in self.disks])
		if(total_free_space<self.num_blocks):
			print("ERROR: Not enough free space on the physical disks.")
			return
		to_allocate = self.num_blocks 
		while(to_allocate>0):
			alloc = allocate_best_block(to_allocate, self.disks)
			mapping.append(alloc)
			to_allocate -= alloc[2]
		return mapping

	def remove(self):
		for m in self.mapping:
			self.disks[m[0]].free(m[1], m[2])

	def read(self, block_num):
		if(self.num_blocks > block_num):
			print("ERROR: Block index out of range")
			return ""
		b = find_physical_block(self.mapping, block_num)
		return b[0].read(b[1])

	def write(self, block_num, write_data):
		if(self.num_blocks > block_num):
			print("ERROR: Block index out of range")
			return ""
		b = find_physical_block(self.mapping, block_num)
		b[0].write(b[1])		

def find_physical_block(mapping, block_num):
	i = block_num
	for m in mapping:
		if(m[2] >= i):
			return (m[0], m[1] + i)
		i -= m[2]

def allocate_best_block(space, disks):
	max_less = (-1, -1, -1)		# (disk_no, start, size)
	min_geq = (-1, -1, INFINITY)
	for i in range(len(disks)):
		d = disks[i]
		for b in d.free_blocks:
			if(b[1]<space and b[1]>max_less[2]):
				max_less = (i, b[0], b[1])
			elif(b[1]>=space and b[1]<min_geq[2]):
				min_geq = (i, b[0], b[1])
	if(min_geq[0] != -1):
		disks[min_geq[0]].remove(min_geq[1], space)
		return (min_geq[0], min_geq[1], space)
	disks[max_less[0]].remove(max_less[1], max_less[2])
	return max_less

def CreateDisk(Id, num_blocks):
	return VirtualDisk(Id, num_blocks, disks)		

def DeleteDisk(Id):
	VirtualDisk.virtual_disks[Id].remove()

def Read(Id, block_num):
	return VirtualDisk.virtual_disks[Id].read(block_num)

def Write(Id, block_num, write_data):
	VirtualDisk.virtual_disks[Id].write(block_num, write_data)

# b1 = Block()

INFINITY = 10000000
disk_sizes = [200, 300]
disks = [PhysicalDisk(x) for x in disk_sizes]

# print(disks[0]),
# print(", "),
# print(disks[1])

# d1 = CreateDisk(1, 400)
# d1 = CreateDisk(2, 50)
# # d1.test_changes()


# print(disks[0]),
# print(", "),
# print(disks[1])

# DeleteDisk(1)
# # print(VirtualDisk.virtual_disks.has_key(1))

# print(disks[0]),
# print(", "),
# print(disks[1])


# print()
# # print(len(VirtualDisk.virtual_disks))