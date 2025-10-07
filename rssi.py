import serial
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
# Serial setup
# -----------------------------
SERIAL_PORT = 'COM16'  # Change if needed
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print("Error opening serial port:", e)
    exit()

# -----------------------------
# Known beacon positions (x, y) in meters
# -----------------------------
beacon_positions = {
    "nRF52833_Beacon_tag": (0, 0),
    "nRF52833_Beacon_tag_2": (1, 0),
    "nRF52833_Beacon_tag_3": (0, 1)
}

# -----------------------------
# RSSI to distance function (simplified path loss)
# -----------------------------
def rssi_to_distance(rssi, tx_power=-59):
    """
    Convert RSSI to distance in meters
    tx_power: RSSI at 1 meter
    """
    return 10 ** ((tx_power - rssi) / (10 * 2))  # n=2 (path-loss exponent)

# -----------------------------
# Data storage
# -----------------------------
distances = {name: [] for name in beacon_positions.keys()}

# -----------------------------
# Matplotlib setup
# -----------------------------
plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ax.set_xlim(-1, 2)
ax.set_ylim(-1, 2)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title("Live Beacon Tracking")

# Plot static beacon positions
for name, (x, y) in beacon_positions.items():
    ax.scatter(x, y, marker='^', label=name)
    ax.text(x+0.02, y+0.02, name)

# Moving tag point
tag_point, = ax.plot([], [], 'ro', markersize=12, label='Estimated Tag')
ax.legend()

# -----------------------------
# Trilateration function
# -----------------------------
def estimate_position(beacon_positions, distances):
    """
    Estimate tag position using simple least squares trilateration
    """
    A = []
    b = []
    for i, (name, pos) in enumerate(beacon_positions.items()):
        if name in distances:
            d = distances[name]
            if d:
                x0, y0 = pos
                A.append([2*(x0 - list(beacon_positions.values())[0][0]),
                          2*(y0 - list(beacon_positions.values())[0][1])])
                b.append(d[0]**2 - list(distances.values())[0][0]**2 +
                         list(beacon_positions.values())[0][0]**2 - x0**2 +
                         list(beacon_positions.values())[0][1]**2 - y0**2)
    if len(A) >= 2:
        A = np.array(A[1:])  # skip first to avoid zero row
        b = np.array(b[1:])
        try:
            pos = np.linalg.lstsq(A, b, rcond=None)[0]
            return pos
        except:
            return [0, 0]
    return [0, 0]

# -----------------------------
# Animation function
# -----------------------------
def update(frame):
    line = ser.readline().decode(errors='ignore').strip()
    if not line:
        return tag_point,
    
    # Example line format: "Device: nRF52833_Beacon_tag | RSSI: -30 dBm | Distance: *float* m"
    match = re.search(r'Device: (\S+) \| RSSI: (-?\d+) dBm', line)
    if match:
        name = match.group(1)
        rssi = int(match.group(2))
        distance = rssi_to_distance(rssi)
        if name in distances:
            distances[name].append(distance)
            # Keep last 5 samples
            if len(distances[name]) > 5:
                distances[name].pop(0)
    
    # Estimate tag position using last distances
    est_pos = estimate_position(beacon_positions, distances)
    tag_point.set_data(est_pos[0], est_pos[1])
    return tag_point,

# -----------------------------
# Run animation
# -----------------------------
ani = FuncAnimation(fig, update, interval=200)
plt.show()
