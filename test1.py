from Disk import *

print_disks(disks)
d1 = CreateDisk(1, 400)
print_disks(disks)
d1 = CreateDisk(2, 50)
print_disks(disks)

Write(1, 1, "hello")

print(Read(1, 1))

DeleteDisk(1)
print_disks(disks)

CreateDisk(3, 25)
print_disks(disks)

DeleteDisk(2)
print_disks(disks)

DeleteDisk(3)
print_disks(disks)
