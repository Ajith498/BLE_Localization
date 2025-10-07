import re
import numpy as np

# -----------------------
# 1. Sample RSSI log
# Replace this with reading from a file or serial port
log_data = """
Device: nRF52833_Beacon_tag | RSSI: -59 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -27 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -26 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -59 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -58 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -57 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -56 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -50 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -60 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -60 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -50 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -48 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -31 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -29 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -27 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -26 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -59 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -58 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -57 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -56 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -50 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -46 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -61 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -60 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -52 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -51 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -45 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -27 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -26 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -59 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -58 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -57 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -56 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -50 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -52 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -51 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -60 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -57 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -27 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -26 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -59 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -58 dBm | Distance: *float* m
Device: Pro 4 Alpha_0ACE | RSSI: -80 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -50 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -48 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -47 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -57 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -56 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -31 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -29 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -60 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -60 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -61 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -59 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -53 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -52 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -48 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -27 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -26 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -57 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -56 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -50 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -48 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -58 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -51 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -31 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -29 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -27 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -26 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -65 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -58 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -57 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag | RSSI: -56 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -50 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -49 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_2 | RSSI: -48 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -25 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -31 dBm | Distance: *float* m
Device: nRF52833_Beacon_tag_3 | RSSI: -29 dBm | Distance: *float* m"""  # truncated for brevity

# -----------------------
# 2. Extract device names and RSSI
pattern = r"Device: (\S+) \| RSSI: (-?\d+) dBm"
matches = re.findall(pattern, log_data)

# Organize data by device
devices = {}
for name, rssi in matches:
    devices.setdefault(name, []).append(int(rssi))

# -----------------------
# 3. Convert RSSI to distance
# Using log-distance path loss model
def rssi_to_distance(rssi, tx_power=-59, n=2.5):
    return 10 ** ((tx_power - rssi) / (10 * n))

device_distances = {}
for name, rssi_list in devices.items():
    distances = [rssi_to_distance(r) for r in rssi_list]
    device_distances[name] = distances

# Print distances
for name, dist_list in device_distances.items():
    avg_dist = np.mean(dist_list)
    print(f"{name} => Avg distance: {avg_dist:.2f} m, Samples: {len(dist_list)}")

# -----------------------
# 4. Trilateration (requires 3 anchors with known positions)
# Example anchor positions (x, y)
anchors = {
    "A1": (0, 0),
    "A2": (2, 0),
    "A3": (0, 2)
}

# Example: distances from anchors for a single beacon
# Replace with real distances from your boards
# Here we take the first three distances of one device
beacon = "nRF52833_Beacon_tag_2"
distances = device_distances[beacon][:3]  # first 3 samples

# Prepare for least squares
A = []
b = []
anchor_keys = list(anchors.keys())
for i in range(1, 3):
    x0, y0 = anchors[anchor_keys[0]]
    xi, yi = anchors[anchor_keys[i]]
    di, d0 = distances[i], distances[0]
    A.append([2*(xi - x0), 2*(yi - y0)])
    b.append([d0**2 - di**2 - x0**2 + xi**2 - y0**2 + yi**2])

A = np.array(A)
b = np.array(b)

# Solve for (x, y)
position, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
print(f"Estimated position of {beacon}: {position.flatten()}")
