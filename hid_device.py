import struct

import hid
import time

vid = 0x0c45
# pid = 0x766b
pid = 0x7040

RETURN_KERNEL_0 = 0x5AA555AA
RETURN_KERNEL_1 = 0xCC3300FF

# 013300FF
# 0xAA55A55A
# FF0033CC
# 0x01AA5500
# 0x03AA5500
# 0x05AA5500
# AA42895A
# AA2498A5

def main():
    with hid.Device(vid, pid) as h:
        print(h);
        # print(f'Device manufacturer: {h.manufacturer}')
        # print(f'Product: {h.product}')
        # print(f'Serial Number: {h.serial}')

        data = struct.pack("<II", RETURN_KERNEL_0, RETURN_KERNEL_1)
        print(data)
        print(h.send_feature_report(data))
        # print(h.send_feature_report([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        # print(h.get_feature_report(0,33))

def write(self, data):
    """Writes data to the device.
    Args:
        data: An iterable containing the binary data.
    Raises:
        IOError: Incorrect amount of bytes was written.
    """

    bytes_written = 0

    # Split the data into 64 byte long chunks
    chunks = [bytearray(data[i:i+64]) for i in range(0, len(data), 64)]

    # Write the chunks to the device
    for chunk in chunks:
        buf = bytearray([0]) + chunk  # First byte is the report number
        bytes_written += self.device.write(buf) - 1

    # Windows always writes full pages
    if bytes_written > len(data):
        bytes_written -= 64 - (len(data) % 64)

    # Raise IOerror if the amount sent doesn't match what we wanted
    if bytes_written != len(data):
        raise IOError("HID Write failed.")

if __name__ == "__main__":
    main()