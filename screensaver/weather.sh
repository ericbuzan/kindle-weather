refresh="0 15 30 45"

if [ "$(cat /proc/keypad)" = "keypad is locked" ] ; then
	chroot /mnt/debian python /home/weatherman/weather-display/weather.py
	cp /mnt/debian/home/weatherman/weather-display/weather.png /mnt/us/screensaver/weather.png
	for item in $refresh
	do
		if [ $(date +%M) == $item ]; then
			eips -c
		fi
	done
eips -g /mnt/us/screensaver/weather.png
fi

