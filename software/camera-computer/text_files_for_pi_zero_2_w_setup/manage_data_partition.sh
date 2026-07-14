#!/bin/sh
# Unmount the third partition if it's mounted.
umount /dev/mmcblk0p3

# Delete partition 3
parted /dev/mmcblk0 rm 3

parted /dev/mmcblk0 mkpart primary ext2 7618560s end

# Remove the ext2 signature if asked, because why not?
# Create a new filesystem on the third partition
mke2fs -v -E discard -m 0 -O ^has_journal /dev/mmcblk0p3

# Mount the new partition at `/home/drone/out`
mount /dev/mmcblk0p3 /home/drone/out

# Correct the permissions on the mounted `/home/drone/out` node
chown drone:drone /home/drone/out

# Disable this script so it doesn't ever run again
systemctl disable manage_data_partition.service
