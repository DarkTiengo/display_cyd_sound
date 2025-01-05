# ESP32 Display Radio with MicroPython

This project uses the ESP32-2432S028R module with an ILI9341 display and XPT2046 touchscreen to create a stylish radio interface. It includes a customizable tuner, UART integration, and RGB LED control via PWM. It’s fully compatible with MicroPython.

## **Features**
- **ILI9341 Display** with **XPT2046** touchscreen integration.
- Visual radio tuner with customizable design.
- UART communication for control and data updates.
- RGB LED control via PWM.
- Compatible with MicroPython.

---

## **Requirements**
### **Hardware**
- **ESP32-2432S028R** module.
- Integrated **ILI9341** display.
- Integrated **XPT2046** touchscreen.
- 5V external power supply (recommended).

### **Software**
- [MicroPython](https://micropython.org/) installed on the ESP32.
- File transfer tool like **ampy** or similar.
- IDE or text editor (e.g., **Thonny** or **VS Code** with MicroPython plugin).

---

## Installation
### 1. ESP32 Initial Setup

Install MicroPython firmware on your ESP32:
  Download the latest firmware: MicroPython ESP32.
  Flash the firmware using esptool:

    esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
    esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-x.x.x.bin

Connect to the ESP32 via REPL to confirm the firmware is working:

    screen /dev/ttyUSB0 115200

### 2. Install Required Libraries

  Clone this repository or download the files:

    git clone https://github.com/DarkTiengo/display_cyd_sound.git

Transfer the files to your ESP32:

    ampy --port /dev/ttyUSB0 put boot.py
    ampy --port /dev/ttyUSB0 put main.py
    ampy --port /dev/ttyUSB0 put ili9341.py
    ampy --port /dev/ttyUSB0 put xpt2046.py

Restart the ESP32:

    ampy --port /dev/ttyUSB0 reset

### Update Radio Information via UART

Send commands via UART to update display information:

    Artist: John Doe\n
    Title: Best Song\n
    Album: Amazing Album\n
    Connection: Connected\n
    Music: Playing\n

### Simulate Radio Frequency

The tuner can dynamically update using the draw_tuner function in the code.

### Contributing

Contributions are welcome! Submit issues or pull requests for improvements.

Developed by **DarkTiengo**.
Contact me at: ogneit@hotmail.com

Feel free to open an issue if you need help or have suggestions!
