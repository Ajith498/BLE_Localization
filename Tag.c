// /*
//  * Copyright (c) 2022 Nordic Semiconductor ASA
//  *
//  * SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
//  */

// #include <zephyr/types.h>
// #include <errno.h>
// #include <zephyr/sys/printk.h>
// #include <zephyr/sys/byteorder.h>
// #include <zephyr/kernel.h>

// #include <zephyr/bluetooth/bluetooth.h>
// #include <zephyr/bluetooth/hci.h>
// #include <zephyr/bluetooth/conn.h>
// #include <zephyr/bluetooth/direction.h>

// #define DF_FEAT_ENABLED BIT64(BT_LE_FEAT_BIT_CONN_CTE_RESP)

// static const struct bt_data ad[] = {
// 	BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
// 	BT_DATA_BYTES(BT_DATA_LE_SUPPORTED_FEATURES, BT_LE_SUPP_FEAT_24_ENCODE(DF_FEAT_ENABLED)),
// 	BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
// };

// // static const struct bt_data ad[] = {
// // 	BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
// // 	BT_DATA(BT_DATA_NAME_COMPLETE, "AJITH", 5),
// // };

// /* Latency set to zero, to enforce PDU exchange every connection event */
// #define CONN_LATENCY	 0U
// /* Interval used to run CTE request procedure periodically.
//  * Value is a number of connection events.
//  */
// #define CTE_REQ_INTERVAL (CONN_LATENCY + 10U)
// /* Length of CTE in unit of 8 us */
// #define CTE_LEN		 (0x14U)

// #if defined(CONFIG_BT_DF_CTE_TX_AOD)
// /* Example sequence of antenna switch patterns for antenna matrix designed by
//  * Nordic. For more information about antenna switch patterns see README.rst.
//  */
// static uint8_t ant_patterns[] = {0x2, 0x0, 0x5, 0x6, 0x1, 0x4, 0xC, 0x9, 0xE, 0xD, 0x8, 0xA};
// #endif /* CONFIG_BT_DF_CTE_TX_AOD */

// static void enable_cte_response(struct bt_conn *conn)
// {
// 	int err;

// 	const struct bt_df_conn_cte_tx_param cte_tx_params = {
// #if defined(CONFIG_BT_DF_CTE_TX_AOD)
// 		.cte_types = BT_DF_CTE_TYPE_ALL,
// 		.num_ant_ids = ARRAY_SIZE(ant_patterns),
// 		.ant_ids = ant_patterns,
// #else
// 		.cte_types = BT_DF_CTE_TYPE_AOA,
// #endif /* CONFIG_BT_DF_CTE_TX_AOD */
// 	};

// 	printk("Set CTE transmission params...");
// 	err = bt_df_set_conn_cte_tx_param(conn, &cte_tx_params);
// 	if (err) {
// 		printk("failed (err %d)\n", err);
// 		return;
// 	}
// 	printk("success.\n");

// 	printk("Set CTE response enable...");
// 	err = bt_df_conn_cte_rsp_enable(conn);
// 	if (err) {
// 		printk("failed (err %d).\n", err);
// 		return;
// 	}
// 	printk("success.\n");
// }

// static void connected(struct bt_conn *conn, uint8_t err)
// {
// 	if (err) {
// 		printk("Connection failed, err 0x%02x %s\n", err, bt_hci_err_to_str(err));
// 	} else {
// 		printk("Connected\n");

// 		enable_cte_response(conn);
// 	}
// }

// static void disconnected(struct bt_conn *conn, uint8_t reason)
// {
// 	printk("Disconnected, reason 0x%02x %s\n", reason, bt_hci_err_to_str(reason));
// }

// BT_CONN_CB_DEFINE(conn_callbacks) = {
// 	.connected = connected,
// 	.disconnected = disconnected,
// };

// static void bt_ready(void)
// {
// 	int err;

// 	printk("Bluetooth initialized\n");

// 	err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_2, ad, ARRAY_SIZE(ad), NULL, 0);
// 	if (err) {
// 		printk("Advertising failed to start (err %d)\n", err);
// 		return;
// 	}

// 	printk("Advertising successfully started\n");
// }

// int main(void)
// {
// 	int err;

// 	err = bt_enable(NULL);
// 	if (err) {
// 		printk("Bluetooth init failed (err %d)\n", err);
// 		return 0;
// 	}

// 	bt_ready();

// 	return 0;
// }
/*
 * Simple BLE Peripheral with custom message
 * Ajith – nRF52833 Example
 */
/*
 * Simple BLE Peripheral Advertising "AJITH" with a message
 * Tested with nRF Connect SDK
 */
/*
 * BLE Peripheral with custom message characteristic
 * Shows up in nRF Connect app under Services
 */
/*
 * Peripheral example broadcasting "HELLO AJITH"
 */
// #include <zephyr/kernel.h>
// #include <zephyr/bluetooth/bluetooth.h>
// #include <zephyr/bluetooth/hci.h>
// #include <zephyr/sys/printk.h>

// /* Advertisement content */
// static const uint8_t flags[] = {BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR};
// static const uint8_t name[] = "HELLO AJITH";

// void main(void)
// {
// 	int err;

// 	printk("Starting Broadcaster\n");

// 	err = bt_enable(NULL);
// 	if (err) {
// 		printk("Bluetooth init failed (err %d)\n", err);
// 		return;
// 	}
// 	printk("Bluetooth initialized\n");

// 	/* Correct declaration */
// 	static const struct bt_data ad[] = {
// 		{.type = BT_DATA_FLAGS, .data_len = sizeof(flags), .data = flags},

// 		{.type = BT_DATA_NAME_COMPLETE, .data_len = sizeof(name) - 1, .data = name},
// 	};

// 	err = bt_le_adv_start(BT_LE_ADV_CONN, ad, ARRAY_SIZE(ad), NULL, 0);
// 	if (err) {
// 		printk("Advertising failed to start (err %d)\n", err);
// 		return;
// 	}

// 	printk("Broadcasting message: HELLO AJITH\n");
// }

// ========

#include <zephyr/kernel.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/sys/printk.h>

/* Advertisement content */
static const uint8_t flags[] = {BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR};
static const uint8_t name[] = "nRF52833_Beacon_tag_3";

/* GATT Characteristic Value (initially set to "HELLO AJITH") */
static char gatt_value[20] = "WELCOME To BLE";

/* Read callback */
static ssize_t read_hello(struct bt_conn *conn, const struct bt_gatt_attr *attr, void *buf,
			  uint16_t len, uint16_t offset)
{
	const char *value = (const char *)attr->user_data;
	return bt_gatt_attr_read(conn, attr, buf, len, offset, value, strlen(value));
}

/* Write callback */
static ssize_t write_hello(struct bt_conn *conn, const struct bt_gatt_attr *attr, const void *buf,
			   uint16_t len, uint16_t offset, uint8_t flags)
{
	char *value = (char *)attr->user_data;

	/* Limit write length */
	if (len > sizeof(gatt_value) - 1) {
		return BT_GATT_ERR(BT_ATT_ERR_INVALID_ATTRIBUTE_LEN);
	}

	memcpy(value, buf, len);
	value[len] = '\0'; /* Null-terminate string */

	printk("Value written from phone: %s\n", value);
	return len;
}

/* GATT Service Definition */
BT_GATT_SERVICE_DEFINE(
	hello_svc, BT_GATT_PRIMARY_SERVICE(BT_UUID_DECLARE_16(0x180A)), /* Device Info Service */
	BT_GATT_CHARACTERISTIC(BT_UUID_DECLARE_16(0x2A29),		/* Manufacturer Name */
			       BT_GATT_CHRC_READ | BT_GATT_CHRC_WRITE,
			       BT_GATT_PERM_READ | BT_GATT_PERM_WRITE, read_hello, write_hello,
			       gatt_value), );

void main(void)
{
	int err;

	printk("Starting GATT Broadcaster with Connectable Advertising\n");

	/* Enable Bluetooth */
	err = bt_enable(NULL);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return;
	}
	printk("Bluetooth initialized\n");

	/* Advertising Data */
	static const struct bt_data ad[] = {
		{.type = BT_DATA_FLAGS, .data_len = sizeof(flags), .data = flags},
		{.type = BT_DATA_NAME_COMPLETE, .data_len = sizeof(name) - 1, .data = name},
	};

	/* Start connectable advertising */
	err = bt_le_adv_start(BT_LE_ADV_CONN, ad, ARRAY_SIZE(ad), NULL, 0);
	if (err) {
		printk("Advertising failed to start (err %d)\n", err);
		return;
	}

	printk("Advertising as connectable device: %s\n", name);
}
