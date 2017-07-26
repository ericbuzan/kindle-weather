#!/bin/sh
#Thanks to bubnikv and tomashg for improvements!
echo "[*] Mounting Rootfs..." 
mount -o loop,noatime -t ext3 /mnt/base-us/debian.ext3 /mnt/debian
echo "[*] Preparing Filesystem..." 
mount -o bind /dev /mnt/debian/dev 
mount -o bind /proc /mnt/debian/proc 
mount -o bind /sys /mnt/debian/sys
echo "[*] Preparing Network Connections..." 
cp /etc/hosts /mnt/debian/etc/hosts 
cp /etc/resolv.conf /mnt/debian/etc/resolv.conf 

#/etc/init.d/powerd stop
/mnt/us/screensaver/weather.sh