# kindle-weather

Inspired by https://mpetroff.net/2012/09/kindle-weather-display/ but made to run completely on the Kindle.

Since Python directly on the Kindle wasn't cooperating, I made a small Debian image to run the Python code. See https://www.mobileread.com/forums/showthread.php?t=96048 and https://www.mobileread.com/forums/showthread.php?t=133005 for details.

The weather-display is placed inside the debian image (currently /home/weatherman) and the screensaver folder is placed in the /mnt/us folder. The crontab file is placed at /etc/crontab/root.

Weather icons used are from http://www.alessioatzeni.com/meteocons/