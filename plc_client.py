import logging
from pymodbus.client import ModbusTcpClient

# Suppress pymodbus internal error logs for a clean CLI output
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)
REGISTER_MAP = {
    2001: ("T-S1"),
    2017: ("T-S2"),
    2033: ("T-S3"),
    2049: ("T-S4"),
    210: ("T-S2 &T-S3 &T-S3 AVG"),
    2103: ("T-S5"),
    2117: ("T-R1"),
    2133: ("T-R2"),
    2149: ("P-S1"),
    2201: ("P-S2"),
    2217: ("P-R1"),
    2233: ("P-R2"),
    2249: ("P-R3"),
    214: ("P-R2 &P-R3 AVG"),
    2301: ("P-F1"),
    2317: ("P-F2"),
    16: ("FS1"),
    26: ("FS2"),
    2101: ("RH"),
    200: ("Valve"),
    202: ("Pump1"),
    204: ("Pump2"),
}

def get_sensor_name(address):
    return REGISTER_MAP.get(address, None)
def scan_id_and_registers(ip, port, max_address=500):
    # Initialize client with a 0.3s timeout for rapid scanning
    client = ModbusTcpClient(ip, port=port, timeout=0.3, retries=0)

    if not client.connect():
        print(f"[-] Connection failed: {ip}:{port}")
        return

    print(f"[*] Connected to {ip}:{port}. Phase 1: Scanning Device IDs (1-255)...")

    active_id = None
    
    # Phase 1: Sweep Device IDs until the first responsive target is found
    for uid in range(1, 256):
        print(f"Testing Device ID: {uid:3}...", end="\r")
        try:
            # We use address 400 based on your previous valid response history先前測試adress在400時有回應，故把400當探針
            # Any response (Error, Empty array, or Data) means the ID is active
            resp = client.read_holding_registers(address=400, count=1, device_id=uid)
            
            # If no timeout exception was thrown, the device responded
            active_id = uid
            print(f"\n[+] Found active Device ID: {uid}")
            break  # Stop ID scanning and proceed to register scanning
            
        except Exception:
            # Timeout (ModbusIOException) means no target at this ID
            pass

    if not active_id:
        print("\n[-] No active Device IDs found. Aborting.")
        client.close()
        return

    print("-" * 50)
    target_addresses = sorted(addr for addr in REGISTER_MAP if addr <= max_address)
    print(f"[*]phase 2: Reading {len(target_addresses)} mapped registers on Device id {active_id}....")
    
    found_data = False
    
    # Phase 2: Scan both Holding (FC03) and Input (FC04) registers 在不知道實際 Register Map 時，逐一測試哪些 Address 可以被讀取
    for addr in target_addresses:
        sensor_info = get_sensor_name(addr)
        sensor_label = f" | [{sensor_info}]" 
        print(f"Testing Address: {addr:4} (0x{addr:0x}){sensor_label}...", end="\r")
        
        # Test 1: Holding Register (FC 03)
        try:
            hr_resp = client.read_holding_registers(address=addr, count=1, device_id=active_id)
            # Verify response is valid and payload is not empty
            if not hr_resp.isError() and hasattr(hr_resp, 'registers') and hr_resp.registers:#檢查是否有錯誤及是否有值
                print(f"\n[+] HIT | FC03 (Holding) | Address: {addr:<4} (0x{addr:04X}) | Data: {hr_resp.registers}{sensor_label}")
                found_data = True
        except Exception:
            pass

        # Test 2: Input Register (FC 04)
        try:
            ir_resp = client.read_input_registers(address=addr, count=1, device_id=active_id)
            # Verify response is valid and payload is not empty
            if not ir_resp.isError() and hasattr(ir_resp, 'registers') and ir_resp.registers:
                print(f"\n[+] HIT | FC04 (Input)   | Address: {addr:<4} (0x{addr:04X}) | Data: {ir_resp.registers}{sensor_label}")
                found_data = True
        except Exception:
            pass

    print("-" * 50)
    if not found_data:
        print(f"[-] Scan complete. No valid data payloads found for ID {active_id}.")
    else:
        print(f"[*] Scan complete. Valid endpoints logged above.")

    # Gracefully close the TCP connection
    client.close()


if __name__ == "__main__":
    # Target configuration
    TARGET_IP = '192.168.2.190'
    TARGET_PORT = 502
    
    # Define how deep the address scan should go (e.g., 0 to 500)
    MAX_SCAN_ADDRESS = 10000

    scan_id_and_registers(TARGET_IP, TARGET_PORT, MAX_SCAN_ADDRESS)
