"""
Modbus TCP simulator for a Fatek-like PLC register.

Run:
    python3 modbus_tcp_server.py

This server exposes one sample value:
    Name: 一次側入水溫
    Short name: T-S1
    Unit: degree C
    Fatek address: R2001
    Modbus type: Holding Register

The value is encoded as temperature * 10, so 25.3 C is stored as 253.
"""

from __future__ import annotations

import logging

from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from pymodbus.server import StartTcpServer


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1502
SLAVE_ID = 1

REGISTER_ADDRESS = 2001
TEMPERATURE_C = 25.3
SCALE = 10


def build_context() -> ModbusServerContext:
    raw_temperature = int(round(TEMPERATURE_C * SCALE))

    # Allocate enough holding registers so address R2001 can be read directly.
    holding_registers = [0] * (REGISTER_ADDRESS + 10)
    holding_registers[REGISTER_ADDRESS] = raw_temperature

    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, holding_registers),
    )
    return ModbusServerContext(slaves={SLAVE_ID: store}, single=False)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    context = build_context()

    print("Modbus TCP simulator is running")
    print(f"Address: {SERVER_HOST}:{SERVER_PORT}")
    print(f"Slave ID: {SLAVE_ID}")
    print(f"R{REGISTER_ADDRESS} / T-S1 = {TEMPERATURE_C:.1f} degree C")
    print("Press Ctrl+C to stop")

    StartTcpServer(
        context=context,
        address=(SERVER_HOST, SERVER_PORT),
    )


if __name__ == "__main__":
    main()
