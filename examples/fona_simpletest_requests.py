import time
import board
import busio
import digitalio
from adafruit_fona.adafruit_fona import FONA
import adafruit_fona.adafruit_fona_socket as cellular_socket
import adafruit_requests as requests

SERVER_ADDRESS = ("wifitest.adafruit.com", 80)

# Get GPRS details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("GPRS secrets are kept in secrets.py, please add them there!")
    raise

# Create a serial connection for the FONA connection using 4800 baud.
# These are the defaults you should use for the FONA Shield.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
uart = busio.UART(board.TX, board.RX, baudrate=4800)
rst = digitalio.DigitalInOut(board.D4)

# Initialize FONA module (this may take a few seconds)
fona = FONA(uart, rst, debug=True)

print("Adafruit FONA WebClient Test")

# Enable GPS
fona.gps = True

# Bring up cellular connection
fona.configure_gprs((secrets["apn"], secrets["apn_username"], secrets["apn_password"]))

# Bring up GPRS
fona.gprs = True


# Initialize a requests object with a socket and cellular interface
requests.set_socket(cellular_socket, fona)

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_GET_URL = "http://httpbin.org/get"
JSON_POST_URL = "http://httpbin.org/post"


print("Fetching text from %s" % TEXT_URL)
response = requests.get(TEXT_URL)
print("-" * 40)

print("Text Response: ", response.text)
print("-" * 40)
response.close()

"""
print("Connecting to: ", SERVER_ADDRESS[0])
sock.connect(SERVER_ADDRESS)

print("Connected to:", sock.getpeername())

# Make a HTTP Request
sock.send(b"GET /testwifi/index.html HTTP/1.1\n")
sock.send(b"Host: 104.236.193.178")
sock.send(b"Connection: close\n\n")

bytes_avail = 0
while not bytes_avail:
    bytes_avail = sock.available()
    if bytes_avail > 0:
        print("bytes_avail: ", bytes_avail)
        data = sock.recv(bytes_avail)
        print(data.decode())
        break
    time.sleep(0.05)

sock.close()
print("Socket connected: ", sock.connected)
"""