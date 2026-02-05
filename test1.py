from gpiozero import PWMLED
from gpiozero import LED
import time
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial

"""
LEFT_FORWARD_PIN = 16
LEFT_BACKWARD_PIN = 20
LEFT_ENABLE_PIN = 21
RIGHT_FORWARD_PIN = 19
RIGHT_BACKWARD_PIN = 26
RIGHT_ENABLE_PIN = 13
"""

LEFT_FORWARD_PIN = PWMLED(16)
LEFT_BACKWARD_PIN = PWMLED(20)
LEFT_ENABLE_PIN = LED(21)
RIGHT_FORWARD_PIN = PWMLED(19)
RIGHT_BACKWARD_PIN = PWMLED(26)
RIGHT_ENABLE_PIN = LED(13)

# LEFT_FORWARD_PIN.value = 0.5 
LEFT_BACKWARD_PIN.value = 0.5

last_channel_value = None


def print_frame(frame, status):
   global last_channel_value
   if hasattr(frame, "payload") and hasattr(frame.payload, "channels"):
       last_channel_value = frame.payload.channels[-1]
       print(last_channel_value)
       # print(",".join(str(val) for val in frame.payload.channels))
   else:
       pass

parser = CRSFParser(print_frame)

with Serial("/dev/ttyAMA0", 425000, timeout=2) as ser:
   buffer = bytearray()
   while True:
       data = ser.read(100)
       buffer.extend(data)
       parser.parse_stream(buffer)
       print(last_channel_value)

       value = last_channel_value / 2000
       LEFT_BACKWARD_PIN.value = value
       LEFT_ENABLE_PIN.on()
