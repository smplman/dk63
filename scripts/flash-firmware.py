#!/usr/bin/env python3
import struct
import sys

import usb.core
import usb.util

import argparse


CMD_BASE = 0x55AA00


def hid_set_feature(dev, report):
    if len(report) > 64:
        raise RuntimeError("report must be less than 64 bytes")
    report += b"\x00" * (64 - len(report))

    dev.ctrl_transfer(
        0x21, # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
        9, # SET_REPORT
        0x300, 0x00,
        report)


def hid_get_feature(dev):
    return dev.ctrl_transfer(
        0xA1, # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_IN
        1, # GET_REPORT
        0x300, 0x00,
        64)


def detach_drivers(dev):
    for cfg in dev:
        print(cfg)
        for intf in cfg:
            dev.reset()
            dev.detach_kernel_driver(intf.bInterfaceNumber)
            dev.set_configuration()

            if dev.is_kernel_driver_active(intf.bInterfaceNumber):
                try:
                    dev.detach_kernel_driver(intf.bInterfaceNumber)
                except usb.core.USBError as e:
                    sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber, str(e)))


def hex_int(x):
    return int(x, 16)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="firmware file to flash")
    parser.add_argument("--vid", type=hex_int, required=True, help="usb device vid")
    parser.add_argument("--pid", type=hex_int, required=True, help="usb device pid")

    args = parser.parse_args()

    with open(args.file, "rb") as inf:
        firmware = inf.read()
    if len(firmware) % 64 != 0:
        raise RuntimeError("firmware size must be divisible by 64")

    dev = usb.core.find(idVendor=args.vid, idProduct=args.pid)
    print(dev)
    if dev is None:
        raise RuntimeError("device not found")

    detach_drivers(dev)

    print("Initialize")
    hid_set_feature(dev, struct.pack("<I", CMD_BASE + 1))
    resp = bytes(hid_get_feature(dev))
    cmd, status = struct.unpack("<II", resp[0:8])
    assert cmd == CMD_BASE + 1
    assert status == 0xFAFAFAFA

    # cmd 3 - write code option - not sure if triggers mass erase - needs more testing, skipping for now

    print("Prepare for flash")
    hid_set_feature(dev, struct.pack("<III", CMD_BASE + 5, 0, len(firmware) // 64))
    resp = bytes(hid_get_feature(dev))
    cmd, status = struct.unpack("<II", resp[0:8])
    assert cmd == CMD_BASE + 5
    assert status == 0xFAFAFAFA

    for addr in range(0, len(firmware), 64):
        chunk = firmware[addr:addr+64]
        hid_set_feature(dev, chunk)

        print("\rFlash [{}/{}]".format(addr + 64, len(firmware)), end="")
    print("")

    print("Reboot")
    hid_set_feature(dev, struct.pack("<I", CMD_BASE + 7))

if __name__ == "__main__":
    main()
