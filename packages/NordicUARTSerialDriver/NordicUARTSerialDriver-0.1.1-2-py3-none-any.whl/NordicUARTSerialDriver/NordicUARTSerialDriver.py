import asyncio
from itertools import count, takewhile
import threading
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))


class NordicUARTSerialDriver:
    """
    This class is a handles Nordic UART Service connections just like a serial port.
    """
    def __init__(self, address, uart_uuid=None, rx_uuid=None, tx_uuid=None):
        self.address=address
        
        self.rx_flag=False
        self.device = None
        self.rx_queue = b''
        
        self.UART_SERVICE_UUID = uart_uuid
        self.UART_RX_CHAR_UUID = self.UART_SERVICE_UUID if rx_uuid is None else rx_uuid
        self.UART_TX_CHAR_UUID = self.UART_SERVICE_UUID if tx_uuid is None else tx_uuid
        
        self._bleak_loop = None
        self._bleak_thread = threading.Thread(target=self._run_bleak_loop)
        # Discard thread quietly on exit.
        self._bleak_thread.daemon = True
        self._bleak_thread_ready = threading.Event()
        self._bleak_thread.start()
        # Wait for thread to start.
        self._bleak_thread_ready.wait()

        self.open(self.address)
        
        nus = self.device.services.get_service(self.UART_SERVICE_UUID)
        self.max_write_without_response_size = nus.get_characteristic(self.UART_RX_CHAR_UUID).max_write_without_response_size

    def _run_bleak_loop(self):
        self._bleak_loop = asyncio.new_event_loop()
        # Event loop is now available.
        self._bleak_thread_ready.set()
        self._bleak_loop.run_forever()
    
    def _close_bleak_loop(self, _: BleakClient):
        self._bleak_loop.stop()
        self._bleak_loop.close()

    def await_bleak(self, coro, timeout=None):
        """Call an async routine in the bleak thread from sync code, and await its result."""
        # This is a concurrent.Future.
        future = asyncio.run_coroutine_threadsafe(coro, self._bleak_loop)
        return future.result(timeout)

    def open(self, address=None):
        if address is None:
            raise NotImplemented()
            ble_device = self.await_bleak(BleakScanner.find_device_by_filter(self.match_nus_uuid, timeout=3))
        else:
            ble_device = self.await_bleak(BleakScanner.find_device_by_address(address))

        if ble_device is None:
            raise Exception("No matching device found, you may need to edit match_nus_uuid().")
        self.device = BleakClient(address_or_ble_device=ble_device)
        self.await_bleak(self.device.connect())

        self.await_bleak(self.device.start_notify(self.UART_TX_CHAR_UUID, self.handle_rx))
        self.await_bleak(self.device.set_disconnected_callback(self._close_bleak_loop))

    def close(self):
        self.await_bleak(self.device.disconnect())

    def read(self):
        if not self.rx_flag:
            return
        self.rx_flag=False
        result = self.rx_queue
        self.rx_queue = b''
        return result

    def write(self, data):
        for s in sliced(bytes(data), self.max_write_without_response_size):
            self.await_bleak(self.device.write_gatt_char(self.UART_RX_CHAR_UUID, s, response=False))
    
    def match_nus_uuid(self, device: BLEDevice, adv: AdvertisementData):
        # This assumes that the device includes the UART service UUID in the
        # advertising data. This test may need to be adjusted depending on the
        # actual advertising data supplied by the device.
        return self.UART_SERVICE_UUID.lower() in adv.service_uuids
    
    def handle_rx(self, char: BleakGATTCharacteristic, data: bytearray):
        self.rx_queue += bytes(data)
        self.rx_flag=True
