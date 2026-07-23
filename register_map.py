"""
集中定義主程式需要讀取的 Modbus Register。

每個 Address 都保留原始 plc_client.py 中的名稱，並提供 scale、unit 與
count。由於目前尚未確認真實比例與工程單位，先使用保守預設值；也因為
尚未確認 Register 類型，本表不指定 Holding Register 或 Input Register。
"""


# REGISTER_MAP 會由 main.py 匯入並依 Address 排序讀取。
# 每個 Address 都會分別嘗試 Holding Register 與 Input Register。
REGISTER_MAP = {
    2001: {
        "name": "T-S1",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2017: {
        "name": "T-S2",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2033: {
        "name": "T-S3",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2049: {
        "name": "T-S4",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    210: {
        "name": "T-S2 &T-S3 &T-S3 AVG",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2103: {
        "name": "T-S5",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2117: {
        "name": "T-R1",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2133: {
        "name": "T-R2",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2149: {
        "name": "P-S1",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2201: {
        "name": "P-S2",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2217: {
        "name": "P-R1",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2233: {
        "name": "P-R2",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2249: {
        "name": "P-R3",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    214: {
        "name": "P-R2 &P-R3 AVG",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2301: {
        "name": "P-F1",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2317: {
        "name": "P-F2",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    16: {
        "name": "FS1",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    26: {
        "name": "FS2",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    2101: {
        "name": "RH",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    200: {
        "name": "Valve",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    202: {
        "name": "Pump1",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
    204: {
        "name": "Pump2",
        "scale": 1.0,
        "unit": "",
        "count": 1,
    },
}
