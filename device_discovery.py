"""
提供 Modbus Device ID 自動掃描功能。

本模組沿用原始 plc_client.py 的策略：以指定的 Holding Register Address
作為探針，從掃描起始值逐一測試到結束值，找到第一個有回應的 Device ID
後立即停止。
"""


def find_active_device_id(
    client,
    device_id_start,
    device_id_end,
    probe_address,
):
    """
    依序掃描並找出第一個有回應的 Modbus Device ID。

    主要參數：
    - client：已連線的 ModbusTcpClient。
    - device_id_start、device_id_end：要測試的 Device ID 起訖值，兩端皆包含。
    - probe_address：用來測試回應的 Holding Register Address。

    回傳值：
    - 找到回應時回傳該 Device ID（整數）。
    - 所有 ID 都因逾時或其他例外而無回應時回傳 None。

    單一 Device ID 測試失敗時會攔截例外並繼續掃描，不會使整個程式中止。
    此處維持原程式的判定方式：只要讀取呼叫正常回傳（即使是 Modbus
    錯誤回應或空資料），就表示該 Device ID 有回應。
    """
    print(
        f"[*] Scanning Device IDs "
        f"({device_id_start}-{device_id_end})..."
    )

    for device_id in range(device_id_start, device_id_end + 1):
        print(f"Testing Device ID: {device_id:3}...", end="\r")

        try:
            # Address 400 等實際探針值由 main.py 從 device_config.py 傳入。
            # 沿用原本語法，不改用其他 Function Code 分派或偵測策略。
            client.read_holding_registers(
                address=probe_address,
                count=1,
                device_id=device_id,
            )

            print(f"\n[+] Found active Device ID: {device_id}")
            return device_id
        except Exception:
            # 常見情況是該 ID 沒有設備而逾時；繼續測試下一個 ID。
            continue

    print("\n[-] No active Device IDs found.")
    return None
