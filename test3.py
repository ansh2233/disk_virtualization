from Snapshot import *

d1 = CreateDisk(1, 200)
print_disks(d1.disks)

Write(1, 0, "hello")
Write(1, 100, "hello 100")

c = Checkpoint(1)

print("Read block 100: " + Read(1, 100))

Write(1, 100, "hello 100 new")

print("Read block 100: " + Read(1, 100))

Rollback(1, c)
print("Read block 100 after rollback: " + str(Read(1, 100)))
