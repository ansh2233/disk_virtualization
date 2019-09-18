from Disk import VirtualDisk
from Disk import PhysicalDisk
from Disk import *

class VirtualSnapshotDisk(VirtualDisk):
	virtual_snapshot_disks = {}
	checkpoints = []

	def __init__(self, Id, num_blocks, disks):
		VirtualDisk.__init__(self, Id, num_blocks, disks)
		# transaction log
		if not self.virtual_snapshot_disks.has_key(Id):
			VirtualSnapshotDisk.virtual_snapshot_disks[Id] = self
			self.commands = []
			self.checkpoints = {}

	def Checkpoint(self):
		checkpnt_num = (len(self.checkpoints.keys()))
		self.checkpoints[checkpnt_num] = len(self.commands)
		return checkpnt_num

	def write(self, block_num, write_data, monitor_this_write = True):
		VirtualDisk.write(self, block_num, write_data)
		if monitor_this_write:
			self.commands.append((block_num, write_data))

	def Rollback(self, checkpnt_num):
		commands_to_apply = self.commands[:self.checkpoints[checkpnt_num]]
		for m in self.mapping:
			self.disks[m[0]].clean(m[1], m[2])
		for cmd in commands_to_apply:
			self.write(cmd[0], cmd[1], False)
		print (">> Checkpoint Rollback complete.")

def CreateDisk(Id, num_blocks):
	return VirtualSnapshotDisk(Id, num_blocks, disks)		

def DeleteDisk(Id):
	VirtualSnapshotDisk.virtual_snapshot_disks[Id].remove()

def Read(Id, block_num):
	return VirtualSnapshotDisk.virtual_snapshot_disks[Id].read(block_num)

def Write(Id, block_num, write_data):
	VirtualSnapshotDisk.virtual_snapshot_disks[Id].write(block_num, write_data)

def Checkpoint(Id):
	return VirtualSnapshotDisk.virtual_snapshot_disks[Id].Checkpoint()

def Rollback(Id, checkpnt_num):
	VirtualSnapshotDisk.virtual_snapshot_disks[Id].Rollback(checkpnt_num)


print(disks[0]),
print(", "),
print(disks[1])

d1 = CreateDisk(1, 200)

print(disks[0]),
print(", "),
print(disks[1])

Write(1, 0, "hello")
Write(1, 100, "hello 100")

c = Checkpoint(1)

print("Read block 100: " + str(Read(1, 100)))

Write(1, 100, "hello 100 new")

print("Read block 100: " + str(Read(1, 100)))

Rollback(1, c)
print("Read block 100 after rollback: " + str(Read(1, 100)))
