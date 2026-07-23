"""
提供單一 Modbus Register 的安全讀取函式。

Holding Register 與 Input Register 使用兩個明確分開的函式，讓呼叫端可以
依序嘗試兩種 Register 類型。任一 Address 讀取失敗都只會回傳 None，不會
中止後續 Address 的讀取。
"""


def read_holding_register(client, address, count, device_id):
    """
    使用 read_holding_registers() 讀取指定的 Holding Register。

    主要參數：
    - client：已連線的 ModbusTcpClient。
    - address：要讀取的 Register Address。
    - count：從該 Address 起要讀取的 Register 數量。
    - device_id：已由自動掃描找到的 Modbus Device ID。

    回傳值：
    - 成功且 registers 不為空時，回傳 registers。
    - Modbus 錯誤回應、缺少 registers、空資料或發生例外時回傳 None。

    函式會攔截單次讀取例外，避免一個 Address 失敗造成整個程式中止。
    """
    try:
        response = client.read_holding_registers(
            address=address,
            count=count,
            device_id=device_id,
        )

        if response.isError():
            return None

        if not hasattr(response, "registers"):
            return None

        if not response.registers:
            return None

        return response.registers
    except Exception:
        return None


def read_input_register(client, address, count, device_id):
    """
    使用 read_input_registers() 讀取指定的 Input Register。

    主要參數：
    - client：已連線的 ModbusTcpClient。
    - address：要讀取的 Register Address。
    - count：從該 Address 起要讀取的 Register 數量。
    - device_id：已由自動掃描找到的 Modbus Device ID。

    回傳值：
    - 成功且 registers 不為空時，回傳 registers。
    - Modbus 錯誤回應、缺少 registers、空資料或發生例外時回傳 None。

    函式會攔截單次讀取例外，避免一個 Address 失敗造成整個程式中止。
    """
    try:
        response = client.read_input_registers(
            address=address,
            count=count,
            device_id=device_id,
        )

        if response.isError():
            return None

        if not hasattr(response, "registers"):
            return None

        if not response.registers:
            return None

        return response.registers
    except Exception:
        return None
