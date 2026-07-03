# Python Modbus TCP 範例

這裡有兩支程式：

- `modbus_tcp_server.py`: 用 pymodbus 模擬 PLC / Modbus TCP 設備
- `modbus_tcp_client.py`: 用 pymodbus 讀取 Modbus TCP 資料

## 安裝套件

```bash
python3 -m pip install "pymodbus>=3.6"
```

## 先跑模擬設備

```bash
python3 modbus_tcp_server.py
```

模擬設備預設監聽：

- IP: `127.0.0.1`
- Port: `1502`
- Slave ID: `1`
- Register: `R2001`
- 值: `25.3 degree C`

因為一般電腦使用 `502` port 可能需要管理員權限，所以模擬程式先使用 `1502`。

## 讀取模擬設備

另開一個終端機：

```bash
python3 modbus_tcp_client.py
```

## 改成讀取實體 PLC

在 `modbus_tcp_client.py` 裡改成：

```python
PLC_HOST = "192.168.4.3"
PLC_PORT = 502
```

## 地址提醒

這份範例把 Fatek `R2001` 直接當作 pymodbus 的 holding register address `2001` 讀取。

如果連接實體設備時讀不到或數值錯一格，常見原因是不同設備或文件會有 0-based / 1-based address 差異。那時可以嘗試把 client 的 `REGISTER_ADDRESS` 改成 `2000`。
