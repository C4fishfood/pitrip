# pitrip
Ntrip service on RaspberryPi

Place the following command in /etc/rc.local to create log file from GPS, filtering the GPS output to only log the line with ccordinate data:
cat /dev/ttyUSB1 | grep --line-buffered 'WGS*' > poslog.txt &



