"""
Developers: HipMonsters.com
Creation Date: Apr 2 2026
License: MIT

Wearable Robot Monitor Client

Connects to a custom BLE wearable.

"""

import asyncio 
import json   
import time
from bleak import BleakClient, BleakScanner

# Peripheral's characteristic UUID for writing
TARGET_UUID_READ  = "rth1209e-45u1-8724-b7f5-ea07361b19c7"  
TARGET_UUID_WRITE = "rth1209e-45u1-8724-b7f5-ea07361b19c7"   

# Peripheral's name for identification. 
TARGET_NAME       = "MYWEARABLESNAME"

async def main():
    try:
        stimuli = {"MeasureA":9, 
                   "MeasureB":9, 
                   "MeasureC":9, 
                   "MeasureD":9}  
        stimuli["robot" ] = "Squirrel"  
        DATA_TO_SEND = json.dumps(stimuli).encode('utf-8')

        print("Scanning for BLE devices...")
        devices = await BleakScanner.discover(timeout=5.0)

        if not devices:
            print("No BLE devices found. Make sure your peripheral is advertising.")
            return
        target_device = None
        # List found devices
        for i, device in enumerate(devices):

            print(f"[{i}] {device.name} ({device.address})") 
            if device.name == TARGET_NAME:
                 print(f"[{i}] {device.name} ({device.address})")
                 target_device = device  
                 print(f"\nConnecting to: {target_device.name} ({target_device.address})")

                 async with BleakClient(target_device.address) as client: 
                     if not client.is_connected:
                         print("Failed to connect to the device.")
                         return
     
                     print("Connected successfully.")
                     # Write data to the characteristic
                     await client.write_gatt_char(TARGET_UUID_WRITE, DATA_TO_SEND)
                     print(f"Data sent: {DATA_TO_SEND}")   
 
                     value = await client.read_gatt_char(TARGET_UUID_READ)
                     print(f"Value: {value}") 

                     client.disconnect()  

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
  
    s_robot       = "squirrel"  
    for i in range(100000):
        asyncio.run(main())
        time.sleep(10)
 