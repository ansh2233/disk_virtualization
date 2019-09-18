from Replica import *

d1 = CreateDisk(1, 110)
print_disks(d1.disks)
Write(1, 10, "hello")

print(Read(1, 10))
print_disks(d1.disks)

DeleteDisk(1)
print_disks(d1.disks)