# BLE_Localization

This project implements **BLE beacon localization** using RSSI values from multiple nRF52833 beacons. It calculates approximate distances and estimates the 2D position of each beacon in real-time using Python.

## Features
- Reads BLE RSSI data from multiple beacons via serial port.
- Converts RSSI to distance using a simple propagation model.
- Estimates 2D positions using trilateration.
- Optional: live 2D visualization of beacon positions on a graph.

## Hardware Requirements
- nRF52833 boards as BLE beacons.
- A PC with Python installed.
- USB connection to read serial data from beacons.

## Python Dependencies
```bash
pip install pyserial matplotlib numpy
