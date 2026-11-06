import network
import time
import urequests
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

TRIG_PIN = Pin(2, Pin.OUT)
ECHO_PIN = Pin(3, Pin.IN)

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def display_status(line1, line2=""):
    oled.fill(0)
    oled.text(line1, 0, 16)
    oled.text(line2, 0, 32)
    oled.show()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        display_status("Connecting to", "WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            
    if wlan.isconnected():
        display_status("WiFi Connected!", wlan.ifconfig()[0])
        time.sleep(2)
    else:
        display_status("WiFi Failed!", "Retrying...")
        time.sleep(2)

def measure_distance():
    TRIG_PIN.low()
    time.sleep_us(2)
    TRIG_PIN.high()
    time.sleep_us(10)
    TRIG_PIN.low()

    pulse_start = 0
    pulse_end = 0

    timeout_start = time.ticks_us()
    while ECHO_PIN.value() == 0:
        pulse_start = time.ticks_us()
        if time.ticks_diff(pulse_start, timeout_start) > 30000:
            return None

    timeout_start = time.ticks_us()
    while ECHO_PIN.value() == 1:
        pulse_end = time.ticks_us()
        if time.ticks_diff(pulse_end, timeout_start) > 30000:
            return None

    duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (duration * 0.0343) / 2
    return round(distance, 2)

def send_to_thingspeak(val):
    try:
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={val}"
        response = urequests.get(url)
        response.close()
        return True
    except Exception as err:
        print("Upload error:", err)
        return False

connect_wifi()

last_upload_time = 0
UPLOAD_INTERVAL = 15  

while True:
    dist = measure_distance()

    if dist is not None:
        oled.fill(0)
        oled.text("Distance Monitor", 0, 0)
        oled.text("----------------", 0, 10)
        oled.text(f"Dist: {dist} cm", 0, 28)
        oled.show()
        print(f"Distance: {dist} cm")
        current_time = time.time()
        if current_time - last_upload_time >= UPLOAD_INTERVAL:
            success = send_to_thingspeak(dist)
            oled.text("Sync: OK" if success else "Sync: Fail", 0, 48)
            oled.show()
            last_upload_time = current_time
    else:
        display_status("Sensor Error", "Out of range")

    time.sleep(1)