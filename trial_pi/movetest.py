
import serial, time

# Baud rate on the Marlin firmware is most commonly 250000, 
# followed by 115200.
ser = serial.Serial('/dev/ttyACM0', 9600) 
print("Opened serial")

time.sleep(5)

# Not sure of the line ending character (maybe \n, \r or even \r\n)
#ser.write(b'G28 X\n')
ser.write(b'M106 100\n')
ser.flush()
print("Wrote line to serial")

time.sleep(2)

print("Closing serial")

ser.close()
