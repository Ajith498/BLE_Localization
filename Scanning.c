# BLE_Localization
BLE beacon localization and RSSI-based distance estimation in Python
#include <zephyr/kernel.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/sys/printk.h>
#include <math.h>
#include <string.h>

#define TX_POWER_AT_1M (-59) /* Calibrate this value for your beacons */
#define PATH_LOSS_EXP  2.0   /* 2 = free space, 2.7–3.5 indoors */

static char current_name[32]; // Store device name temporarily

/* --- RSSI to Distance conversion function --- */
static float rssi_to_distance(int rssi)
{
	float distance = pow(10.0, ((TX_POWER_AT_1M - rssi) / (10.0 * PATH_LOSS_EXP)));
	return distance;
}

/* --- Parse advertising data for device name --- */
static bool device_found(struct bt_data *data, void *user_data)
{
	memset(current_name, 0, sizeof(current_name));

	if (data->type == BT_DATA_NAME_COMPLETE || data->type == BT_DATA_NAME_SHORTENED) {
		memcpy(current_name, data->data, data->data_len);
		current_name[data->data_len] = '\0';
		return false; // stop parsing after finding the name
	}

	return true;
}

/* --- Callback for each scanned BLE device --- */
static void device_scanned(const bt_addr_le_t *addr, int8_t rssi, uint8_t type,
			   struct net_buf_simple *ad)
{
	bt_data_parse(ad, device_found, NULL);

	/* Only print if device name is found */
	if (strlen(current_name) > 0) {
		float distance = rssi_to_distance(rssi);
		printk("Device: %s | RSSI: %d dBm | Distance: %.2f m\n", current_name, rssi,
		       distance);
	}
}

void main(void)
{
	int err;

	printk("Starting BLE Central (Show Name, RSSI, Distance)\n");

	err = bt_enable(NULL);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return;
	}

	printk("Bluetooth initialized\n");

	/* Scan parameters */
	struct bt_le_scan_param scan_params = {
		.type = BT_HCI_LE_SCAN_ACTIVE,
		.options = BT_LE_SCAN_OPT_NONE,
		.interval = 0x0060,
		.window = 0x0030,
	};

	err = bt_le_scan_start(&scan_params, device_scanned);
	if (err) {
		printk("Scanning failed to start (err %d)\n", err);
		return;
	}

	printk("Scanning started\n");
}
