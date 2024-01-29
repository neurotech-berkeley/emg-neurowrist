import csv
import serial
import subprocess
from datetime import datetime

output = subprocess.run(["ls /dev/tty.*"], stdout=subprocess.PIPE, shell=True, text=True)
ports = output.stdout.split("\n")[:-1]
i = 0
print("\n>> Select UART/USB to read from:\n")
for port in ports:
    print("  ", i, ":", port)
    i += 1
index = int(input("\n>> "))
port = ports[index]
print("\nOK, opening", port)

serialPort = serial.Serial(port=port, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

now = datetime.now()
dt_string = now.strftime("%m-%d-%Y-%H:%M:%S")
csvfilename = "recordings/{}.csv".format(dt_string)
print(csvfilename)

# create a CSV file to store the data
csvfile = open(csvfilename, "w", newline="")
fieldnames = ['time', 'ch0', 'ch1', 'ch2']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
while serialPort:
    x = serialPort.readline()
    try: 
        millis, ch0, ch1, ch2 = x.decode("utf-8").split()
    except:
        continue
    millis = int(millis)
    ch0 = int(ch0)
    ch1 = int(ch1)
    ch2 = int(ch2)
    print(millis, ch0, ch1, ch2)
    writer.writerow({'millis': millis, 'ch0': ch0, 'ch1': ch1, 'ch2': ch2})