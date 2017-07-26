if [ "$(lipc-get-prop com.lab126.wifid cmState)" = "CONNECTED" ] ; then
  cd /mnt/us/screensaver
  rm /mnt/us/screensaver/weather.png
  sftp weather@192.168.1.105:/home/weather/weather-display/weather.png

  if [ "$(cat /proc/keypad)" = "keypad is locked" ] ; then
  	eips -c
    eips -g /mnt/us/screensaver/weather.png
  fi
fi
