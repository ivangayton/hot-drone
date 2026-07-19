# Setting Up From Firmware/Images

## KB2040

Installing firmware is a simple matter of connecting the KB2040 to a host PC over USB. Hold down the "BOOT" button on the KB2040 while connecting to force the KB2040 to enter the UF2 bootloader. This causes the KB2040 to appear as a USB mass storage device on your PC, provided the Raspberry Pis are not connected (make sure the KB2040 is not connected to the other subsystems before attempting this). From there, drag or otherwise copy the .UF2 file to to KB2040 mass storage drive. After a few seconds, the drive will disappear from your PC. Wait a few more seconds just for good measure, then detach the KB2040 and it's ready to be reconnected to the target system (the camera subsystem). One sign that the KB2040 is correctly flashed is that the onboard RGB LED will flash on and off in red. This is an indication the firmware is awaiting a USB host to connect and start streaming drone data from the KB2040.

## Raspberry Pi Zero 2 W

An image file is provided that can be written to a microSD card with the [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

Inside the Raspberry Pi Imager, make the following selections:

* Raspberry Pi Device: Raspberry Pi Zero 2 W
* Operating System: choose "Use custom", and then choose the disk `.img` file provided by this `hot-drone` project.
* Storage: choose a microSD card connected to your host PC.

Choose "Next", and then "Edit Settings". Inside "OS Customization", configure the following:

* General
  * Set hostname: "drone-1" or "drone-2" or "drone-3", to make the name unique for each Pi Zero unit inside the camera assembly.
  * Set username and password:
    * Username: "drone"
    * Password: "geocene"
  * Configure wireless LAN:
    * SSID: use your prefered Wi-Fi network name
    * Password: the password for your Wi-Fi network
    * Hidden SSID: unchecked
    * Wireless LAN country: "US"
  * Set locale settings:
    * Time zone: "America/Los_Angeles"
    * Keyboard layout: "US"
* Service
  * Enable SSH: checked
  * Use password authentication (you can do public-key authentication too, if you're familiar with how to set it up properly)

Choose "Save", then choose "Yes" to continue to writing the microSD card. Once the software says the SD card is ready, remove it and install it in the appropriate Pi Zero unit.

The Pi may require a few minutes to get itself sorted out. Among other things, it will resize the disk image to take up the full amount of the microSD card it was written to. So allow each Pi a few minutes to do its thing before disconnecting power and trying to troubleshoot perceived Wi-Fi problems. (This is the voice of experience!) It also seems that on first boot, the Wi-Fi doesn't come up. So during first boot from a freshly imaged SD card, wait a few minutes and then power-cycle the Zero. After a minute of rebooting, it should connect to your Wi-Fi.

To find the Pi on your network, you can install arp-scan to find all of the devices on the network. First, find your own IP address on the network (you must be on the same network as the Pi) with ```ip addr show```. Then issue the command ```arp-scan xxx.xxx.xxx.xxx/24 (the x's represent your own IP address, though the bit after the last period can be 0). Then ssh in with ```ssh drone@xxx.xxx.xxx.xxx``` and type in the relevant password. 

It may be that without public-key authentication isn't set up, the pi won't be configured to accept ssh connections. You have a few options:
- Connect the pi to a monitor, which will get you a terminal, and edit the relevant config file by typing ```sudo nano /etc/ssh/ssdh_config``` and changing the line ```PasswordAuthentication No``` to ```PasswordAuthentication Yes```.
- If you don't have a monitor, you can turn off the Pi, plug the SD card into a computer, enter the ```rootfs``` partition, find the file ```/etc/ssh/sshd_config```, edit as above, put the card back in the Pi and try again.

I've also found running `sudo iw wlan0 set power_save off` on a Raspberry Pi makes its Wi-Fi more reliable to connect to, and less hurky-jerky in use on a weak Wi-Fi network.

Once you're logged in, you should resize the third partition on the SD card. It looks like this:

```
# Unmount the third partition if it's mounted.
sudo umount /dev/mmcblk0p3

# Run `fdisk` to delete and recreate the third partition with a larger size
sudo fdisk /dev/mmcblk0

# Command: d (delete a partition)
# Partition number: 3
# Command: n (add a new partition)
# Partition type: p
# Partition number: 3
# First sector: 7618560
# Last sector: <recommended default, the last sector of the SD card, however large yours is>
# Remove the ext2 signature if asked, because why not?
# Command: w (write partition table to disk)

# Create a new filesystem on the third partition
sudo mke2fs -v -E discard -m 0 -O ^has_journal /dev/mmcblk0p3

# Mount the new partition at `/home/drone/out`
sudo mount /dev/mmcblk0p3 /home/drone/out

# Correct the permissions on the mounted `/home/drone/out` node
sudo chown drone:drone /home/drone/out
```

## Do the above directly on the SD card instead of logging into the Pi
If we don't want to connect to the Pi Zero 2 W with a terminal (either via SSH or using a keyboard and monitor), we can do this directly on the SD card filesystem in a Linux laptop.

```
# Run `fdisk` to delete and recreate the third partition with a larger size
# SD card probably shows up as /dev/sda (check that!)
sudo fdisk /dev/sda

# Command: d (delete a partition)
# Partition number: 3
# Command: n (add a new partition)
# Partition type: p
# Partition number: 3
# First sector: 7618560
# Last sector: <recommended default, the last sector of the SD card, however large yours is>
# Remove the ext2 signature if asked, because why not?
# Command: w (write partition table to disk)

# Create a new filesystem on the third partition
sudo mke2fs -v -E discard -m 0 -O ^has_journal /dev/sda3
```

If doing it this way, don't bother to mount the filesystem because you're not on the Pi; the mount point is created on the fly on the actual machine, not on the OS media! However, you still have to chown the mount point, which can't be done on another machine (because the mount point doesn't exist on the other machine)

We can create a Systemd serivce to do the change owner operation (which requires mount point actually exist before it can be chowned). Paste the ```chown_data_partition.service``` file into ```/media/$USER/rootfs/lib/systemd/system/```. Paste ```chown_data_partition.sh``` into ```/media/$USER/rootfs/opt/```. Activate the service with ```sudo ln -s /etc/systemd/system/chown_data_partition.service``` (it looks like you're pointing the symlink to your computer's ```etc``` folder, but don't worry, the target text will be interpreted correctly as referreing to the Pi's /etc/ directory when it's running on the Pi.

Be sure to edit ```rootfs/etc/ssh/sshd-config``` to change ```PasswordAuthentication no``` to ```PasswordAuthentication yes``` (unless you set up ssh keys on the Pi on setup and are sure you'll only ever want to ssh in from the machines with those keys). 

### TODO: Add the resizing operation to the script called by the service (probably using parted instead of fdisk) to eliminate the manual steps above.

## Done!

Now, reboot the Pi Zero, and it should be fully functional.

```
sudo reboot
```
