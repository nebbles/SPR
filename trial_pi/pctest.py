#to send a file of gcode to the printer
from printcore import printcore
#from printrun import gcoder
import time

print("Creating printer instance...")
p = printcore('/dev/ttyACM0', 115200)
time.sleep(3)
print("Created printer instance.")

#gcode=[i.strip() for i in open('filename.gcode')] # or pass in your own array of gcode lines instead of reading from a file
#gcode = gcoder.LightGCode(gcode)
#p.startprint(gcode) # this will start a print

#If you need to interact with the printer:
#p.send_now("M106 100") # this will send M105 immediately, ahead of the rest of the print
#p.pause() # use these to pause/resume the current print
#p.resume()

# print("sending command")
# p.send_now("G0 X50 Y50")
# p.send_now("M106 0")

try:
    while True:
        cmd = input("Input GCODE line: ")
        print("Sending command...")
        p.send_now(cmd)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting cleanly...")
    time.sleep(1)
    p.disconnect()
    print("Disconnected. Goodbye.")
