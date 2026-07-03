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

import logging

from pymodbus.server import StartTcpServer

try:
    from pymodbus.simulator import DataType, SimData, SimDevice
except ImportError:
    DataType = None
    SimData = None
    SimDevice = None

try:
    from pymodbus.datastore import ModbusServerContext
except ImportError:
    ModbusServerContext = None

try:
    from pymodbus.datastore import ModbusSequentialDataBlock
except ImportError:
    try:
        from pymodbus.datastore.store import ModbusSequentialDataBlock
    except ImportError:
        ModbusSequentialDataBlock = None

try:
    from pymodbus.datastore import ModbusSlaveContext as LegacyModbusDevice
except ImportError:
    try:
        from pymodbus.datastore import ModbusDeviceContext as LegacyModbusDevice
    except ImportError:
        LegacyModbusDevice = None


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1502
SLAVE_ID = 1

REGISTER_ADDRESS = 2001
TEMPERATURE_C = 25.3
SCALE = 10
DATA_BLOCK_START_ADDRESS = 1


def build_sim_context(raw_temperature):
    return [
        SimDevice(
            SLAVE_ID,
            simdata=(
                [SimData(0, values=[False], datatype=DataType.BITS)],
                [SimData(0, values=[False], datatype=DataType.BITS)],
                [SimData(REGISTER_ADDRESS, values=[raw_temperature], datatype=DataType.REGISTERS)],
                [SimData(0, values=[0], datatype=DataType.REGISTERS)],
            ),
        )
    ]


def build_legacy_context(raw_temperature):
    if not all((ModbusServerContext, ModbusSequentialDataBlock, LegacyModbusDevice)):
        raise RuntimeError("Installed pymodbus version does not provide a supported server datastore API")

    holding_registers = [0] * (REGISTER_ADDRESS - DATA_BLOCK_START_ADDRESS + 10)
    holding_registers[REGISTER_ADDRESS - DATA_BLOCK_START_ADDRESS] = raw_temperature

    device = LegacyModbusDevice(
        hr=ModbusSequentialDataBlock(DATA_BLOCK_START_ADDRESS, holding_registers),
    )

    try:
        return ModbusServerContext(slaves={SLAVE_ID: device}, single=False)
    except TypeError:
        return ModbusServerContext(devices={SLAVE_ID: device}, single=False)


def build_context():
    raw_temperature = int(round(TEMPERATURE_C * SCALE))

    if all((DataType, SimData, SimDevice)):
        return build_sim_context(raw_temperature)
    return build_legacy_context(raw_temperature)


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
