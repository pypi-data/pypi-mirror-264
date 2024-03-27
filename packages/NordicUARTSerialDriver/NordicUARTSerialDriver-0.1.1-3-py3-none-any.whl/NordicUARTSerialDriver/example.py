import time
from NordicUARTSerialDriver import NordicUARTSerialDriver

UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
mac_address = "88:22:B2:F4:5C:32"

def main():
    x = NordicUARTSerialDriver(mac_address, uart_uuid=UART_SERVICE_UUID, rx_uuid=UART_RX_CHAR_UUID, tx_uuid=UART_TX_CHAR_UUID)
    x.write([0xff, 0x00, 0x12] + [0]*2)
    x.write([0xff, 0x00, 0x12] + [0]*2)
    x.write([0xff, 0x00, 0x12] + [0]*2)

    time.sleep(1)
    print(x.read())

    x.close()

if __name__ == "__main__":
    main()
