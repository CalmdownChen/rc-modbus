import logging
from pymodbus.client import ModbusTcpClient

# Suppress pymodbus internal error logs for a clean CLI output
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)

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
            # We use address 400 based on your previous valid response history
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
    print(f"[*] Phase 2: Deep scanning Registers 0 to {max_address} on Device ID {active_id}...")
    
    found_data = False
    
    # Phase 2: Scan both Holding (FC03) and Input (FC04) registers 在不知道實際 Register Map 時，逐一測試哪些 Address 可以被讀取
    for addr in range(max_address + 1):
        print(f"Testing Address: {addr:4} (0x{addr:04X})...", end="\r")
        
        # Test 1: Holding Register (FC 03)
        try:
            hr_resp = client.read_holding_registers(address=addr, count=1, device_id=active_id)
            # Verify response is valid and payload is not empty
            if not hr_resp.isError() and hasattr(hr_resp, 'registers') and hr_resp.registers:
                print(f"\n[+] HIT | FC03 (Holding) | Address: {addr:<4} (0x{addr:04X}) | Data: {hr_resp.registers}")
                found_data = True
        except Exception:
            pass

        # Test 2: Input Register (FC 04)
        try:
            ir_resp = client.read_input_registers(address=addr, count=1, device_id=active_id)
            # Verify response is valid and payload is not empty
            if not ir_resp.isError() and hasattr(ir_resp, 'registers') and ir_resp.registers:
                print(f"\n[+] HIT | FC04 (Input)   | Address: {addr:<4} (0x{addr:04X}) | Data: {ir_resp.registers}")
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
