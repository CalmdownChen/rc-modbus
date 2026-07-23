"""
集中管理 PLC、Modbus TCP 連線與 Device ID 掃描設定。

未來若要更換 PLC IP、TCP Port、連線逾時、重試次數、Device ID
掃描範圍或探針 Address，只需要修改本檔案，不必更動主要讀取流程。
"""


# PLC 的網路連線設定。
PLC_IP = "192.168.2.190"
MODBUS_TCP_PORT = 502
TIMEOUT = 0.3
RETRIES = 0

# Device ID 掃描設定。
# DEVICE_ID_END 也包含在掃描範圍內，因此目前會依序測試 1 到 255。
DEVICE_ID_START = 1
DEVICE_ID_END = 255

# Address 400 是先前測試時曾有回應的 Holding Register，
# 因此目前以它作為判斷 Device ID 是否有回應的探針。
DEVICE_ID_PROBE_ADDRESS = 400
