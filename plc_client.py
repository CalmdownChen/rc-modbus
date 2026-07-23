"""
保留原本 `python plc_client.py` 執行方式的相容入口。

實際的主要流程集中在 main.py，本檔案只匯入並呼叫 main()，避免兩個檔案
各自維護重複的 Modbus TCP 讀取邏輯。
"""

from main import main


if __name__ == "__main__":
    main()
