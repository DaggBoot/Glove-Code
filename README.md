# Glove Mouse & IUPAC Molecule Parser

## Overview

This repository contains two projects demonstrating hardware and software integration for computational chemistry and human-computer interaction:

1. **Smart Glove Mouse** – A wearable glove interfaced with a Raspberry Pi / microcontroller to act as a mouse using **flex sensors** and an **MPU6050 IMU**.
2. **IUPAC Molecule Parser** – A Python program that parses **organic molecular formulas** and represents them as graphs of atoms and bonds, with support for multiple elements and functional groups.

---

## Project 1: Smart Glove Mouse

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
