#!/bin/sh

# Correct the permissions on the mounted `/home/drone/out` node
chown drone:drone /home/drone/out

# Disable this script so it doesn't ever run again
systemctl disable chown_data_partition.service
