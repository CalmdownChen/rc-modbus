"""
Modbus TCP client for reading a Fatek-like PLC register with pymodbus.

Run against the simulator:
    python3 modbus_tcp_client.py

For the real PLC later, change PLC_HOST to "192.168.4.3" and PLC_PORT to 502.
"""

from pymodbus.client import ModbusTcpClient


# Simulator default:
PLC_HOST = "127.0.0.1"
PLC_PORT = 1502

# Real device setting for later:
# PLC_HOST = "192.168.4.3"
# PLC_PORT = 502

SLAVE_ID = 1

REGISTER_ADDRESS = 2001
REGISTER_COUNT = 1
SCALE = 10


def read_holding_register(client: ModbusTcpClient, address: int, count: int):
    """Support current pymodbus versions and older versions with unit=."""
    try:
        return client.read_holding_registers(
            address=address,
            count=count,
            slave=SLAVE_ID,
        )
    except TypeError:
        return client.read_holding_registers(
            address=address,
            count=count,
            unit=SLAVE_ID,
        )


def main() -> None:
    client = ModbusTcpClient(host=PLC_HOST, port=PLC_PORT, timeout=3)

    try:
        if not client.connect():
            raise ConnectionError(f"Could not connect to {PLC_HOST}:{PLC_PORT}")

        response = read_holding_register(
            client=client,
            address=REGISTER_ADDRESS,
            count=REGISTER_COUNT,
        )

        if response.isError():
            raise RuntimeError(f"Modbus read error: {response}")

        raw_value = response.registers[0]
        temperature_c = raw_value / SCALE

        print("Read Modbus TCP value successfully")
        print(f"Device: {PLC_HOST}:{PLC_PORT}, slave {SLAVE_ID}")
        print(f"Name: 一次側入水溫")
        print(f"Short name: T-S1")
        print(f"Fatek address: R{REGISTER_ADDRESS}")
        print(f"Raw value: {raw_value}")
        print(f"Temperature: {temperature_c:.1f} degree C")

    finally:
        client.close()


if __name__ == "__main__":
    main()
