"""
Modbus TCP Register 讀取程式的主要執行流程。

本模組負責建立連線、自動尋找 Device ID、依 Address 排序讀取 Register、
顯示 Holding/Input Register 結果，並確保程式離開時關閉 TCP 連線。連線
設定、Register 資料、Device ID 掃描與實際讀取邏輯分別放在其他模組。
"""

import logging

from pymodbus.client import ModbusTcpClient

# 以下連線與掃描設定皆定義於 device_config.py。
from device_config import (
    DEVICE_ID_END,
    DEVICE_ID_PROBE_ADDRESS,
    DEVICE_ID_START,
    MODBUS_TCP_PORT,
    PLC_IP,
    RETRIES,
    TIMEOUT,
)

# find_active_device_id() 定義於 device_discovery.py。
from device_discovery import find_active_device_id

# 兩種 Register 讀取函式皆定義於 modbus_reader.py。
from modbus_reader import read_holding_register, read_input_register

# REGISTER_MAP 定義於 register_map.py，集中保存 Address 與顯示資訊。
from register_map import REGISTER_MAP


# 沿用原始程式設定，避免 pymodbus 內部錯誤訊息干擾 CLI 讀取結果。
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)


def main():
    """
    執行完整的 Modbus TCP 連線、Device ID 掃描與 Register 讀取流程。

    本函式不接收參數；PLC 與掃描設定取自 device_config.py，Register 清單
    取自 register_map.py。執行成功或可預期失敗時皆不回傳資料（回傳 None），
    結果直接輸出到終端機。

    連線失敗或找不到 Device ID 時會顯示訊息後結束；單一 Register 的失敗
    由 modbus_reader.py 的函式轉成 None。finally 區塊會確保已建立的 client
    執行 close()，避免 TCP 連線未釋放。
    """
    client = None

    try:
        # 所有連線參數皆來自 device_config.py，未來更換設備時只需修改該檔。
        client = ModbusTcpClient(
            PLC_IP,
            port=MODBUS_TCP_PORT,
            timeout=TIMEOUT,
            retries=RETRIES,
        )

        try:
            connected = client.connect()
        except Exception as error:
            print(
                f"[-] Connection failed: {PLC_IP}:{MODBUS_TCP_PORT} "
                f"({error})"
            )
            return

        if not connected:
            print(f"[-] Connection failed: {PLC_IP}:{MODBUS_TCP_PORT}")
            return

        print(f"[*] Connected to {PLC_IP}:{MODBUS_TCP_PORT}.")

        # find_active_device_id() 定義於 device_discovery.py，
        # 負責依序測試 Device ID，並回傳第一個有回應的 ID。
        active_id = find_active_device_id(
            client=client,
            device_id_start=DEVICE_ID_START,
            device_id_end=DEVICE_ID_END,
            probe_address=DEVICE_ID_PROBE_ADDRESS,
        )

        if active_id is None:
            print("[-] Register reading aborted: no active Device ID.")
            return

        print("-" * 80)
        print(
            f"[*] Reading {len(REGISTER_MAP)} configured addresses "
            f"on Device ID {active_id}..."
        )

        found_data = False

        # REGISTER_MAP 定義於 register_map.py。
        # sorted() 確保每次都依 Address 由小到大讀取，方便核對輸出。
        for address in sorted(REGISTER_MAP):
            register_info = REGISTER_MAP[address]
            name = register_info["name"]
            scale = register_info["scale"]
            unit = register_info["unit"]
            count = register_info["count"]
            unit_display = unit if unit else "(未設定)"

            # read_holding_register() 定義於 modbus_reader.py，
            # 負責使用 read_holding_registers() 讀取 Holding Register。
            holding_data = read_holding_register(
                client=client,
                address=address,
                count=count,
                device_id=active_id,
            )

            if holding_data is not None:
                # 目前依需求只取第一個 Register；日後確認資料格式後再擴充解碼。
                raw_value = holding_data[0]
                converted_value = raw_value * scale
                print(
                    f"[+] Holding Register | "
                    f"Address: {address:<4} (0x{address:04X}) | "
                    f"Name: {name} | Raw value: {raw_value} | "
                    f"Value: {converted_value} | Unit: {unit_display}"
                )
                found_data = True
            else:
                print(
                    f"[-] Holding Register | "
                    f"Address: {address:<4} (0x{address:04X}) | "
                    f"Name: {name} | No valid data"
                )

            # read_input_register() 定義於 modbus_reader.py，
            # 負責使用 read_input_registers() 讀取 Input Register。
            input_data = read_input_register(
                client=client,
                address=address,
                count=count,
                device_id=active_id,
            )

            if input_data is not None:
                # 換算方式維持單純的 raw_value * scale，不預先猜測資料編碼。
                raw_value = input_data[0]
                converted_value = raw_value * scale
                print(
                    f"[+] Input Register   | "
                    f"Address: {address:<4} (0x{address:04X}) | "
                    f"Name: {name} | Raw value: {raw_value} | "
                    f"Value: {converted_value} | Unit: {unit_display}"
                )
                found_data = True
            else:
                print(
                    f"[-] Input Register   | "
                    f"Address: {address:<4} (0x{address:04X}) | "
                    f"Name: {name} | No valid data"
                )

        print("-" * 80)
        if found_data:
            print("[*] Register reading complete.")
        else:
            print(
                f"[-] Register reading complete. "
                f"No valid data found for Device ID {active_id}."
            )
    except Exception as error:
        # 攔截初始化或主流程中的非預期錯誤，避免直接顯示未處理 traceback。
        print(f"[-] Modbus reader stopped because of an unexpected error: {error}")
    finally:
        if client is not None:
            try:
                client.close()
            except Exception as error:
                # close() 極少失敗；若發生仍清楚回報，而不遮蔽原本流程結果。
                print(f"[-] Failed to close Modbus TCP connection: {error}")


if __name__ == "__main__":
    main()
