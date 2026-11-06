# IoT Distance Monitor with Raspberry Pi Pico W & ThingSpeak

An IoT-based distance monitoring system built with the Raspberry Pi Pico W, an HC-SR04 ultrasonic distance sensor, and an SSD1306 0.96" I2C OLED display. Real-time measurements are rendered locally on the OLED screen and periodically transmitted over Wi-Fi to a ThingSpeak cloud channel for logging and visualization.

![Project Setup](assets/setup1.jpeg)

## Features
- **Real-Time Distance Measurement:** Reads range data via HC-SR04 ultrasonic echo timing.
- **Local Display:** Live distance readings displayed on a 128x64 SSD1306 OLED via I2C.
- **Cloud Dashboard:** Sends timestamped distance readings to ThingSpeak (Field 1) every 15 seconds.
- **Wi-Fi Connectivity:** Automatic association and status reporting via the Pico W's onboard CYW43439 module.


## Hardware Components
- Raspberry Pi Pico W
- HC-SR04 Ultrasonic Sensor
- 0.96" SSD1306 I2C OLED Display (128x64)
- Solderless Breadboard & Jumper Wires
- Micro-USB cable

## Pin Configuration

| Component | Pin | Pico W GPIO | Physical Pin |
| :--- | :--- | :--- | :--- |
| **SSD1306 OLED** | VCC | 3V3(OUT) | Pin 36 |
| | GND | GND | Pin 38 |
| | SDA | GP4 | Pin 6 |
| | SCL | GP5 | Pin 7 |
| **HC-SR04** | VCC | 3V3 / VBUS | Pin 36 / Pin 40 |
| | GND | GND | Pin 3 |
| | Trig | GP2 | Pin 4 |
| | Echo | GP3 | Pin 5 |

## ThingSpeak Cloud Interface
ThingSpeak is used as the IoT cloud telemetry broker to store and graph distance measurements in real time. The Pico W transmits HTTP requests containing the calculated distance value to the configured channel every 15 seconds to adhere to free-tier rate limits
| ThingSpeak Chart | Full System Setup |
| :---: | :---: |
| ![ThingSpeak Chart](assets/setup2.jpeg) | ![Full Setup](assets/setup3.jpeg) |

## Software & Setup
1. Flash your Raspberry Pi Pico W with the latest [MicroPython firmware](https://micropython.org/download/RPI_PICO_W/).
2. Open Thonny IDE and set the interpreter to **MicroPython (Raspberry Pi Pico)**.
3. Upload `src/ssd1306.py` and `src/main.py` to the Pico W.
4. Replace the placeholders in `src/main.py`:
   - `WIFI_SSID`
   - `WIFI_PASSWORD`
   - `THINGSPEAK_API_KEY`
5. Run `main.py` or restart the board to run automatically.