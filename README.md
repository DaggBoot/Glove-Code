# Glove Mouse

## Overview

This repository contains two projects demonstrating hardware and software integration for computational chemistry and human-computer interaction:

Documentation of the process:
https://docs.google.com/document/d/1xA9Bw5oXs85HT2D1c6V7PJc5jY7L_LD3KcEMkghLs18/edit?usp=sharing

---

## Smart Glove Mouse

### Description

The glove translates **hand movements and finger flexes** into mouse actions, including:

- Cursor movement (pitch and roll of hand)
- Left and right clicks (based on flex sensor thresholds)
- Dragging and scrolling
- Optional calibration for sensor offsets

The project uses:

- **Raspberry Pi / Microcontroller** (RP2040 or similar)
- **MPU6050 IMU** for orientation (pitch, roll, yaw)
- **Flex sensors** for finger detection
- **Python** for data reading and GUI automation (`pyautogui`)
- **UART / Serial communication** to interface glove sensors with the main program

### Features

- Smooth translation of hand motion to mouse cursor
- Click detection using flex sensor thresholds
- Drag and scroll functionality
- Real-time debugging prints for sensor data

### Usage

1. Connect the glove sensors to the microcontroller and ensure proper I2C/UART setup.
2. Install required Python libraries:

```bash
pip install pyserial pyautogui
python glove_mouse.py
```

Move your hand to control the cursor; bend fingers for clicks or drags.
