#!/usr/bin/env python3
import struct

import usb.core
import usb.util

import argparse


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
        for intf in cfg:
            if dev.is_kernel_driver_active(intf.bInterfaceNumber):
                try:
                    dev.detach_kernel_driver(intf.bInterfaceNumber)
                except usb.core.USBError as e:
                    sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber, str(e)))


def hex_int(x):
    return int(x, 16)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vid", type=hex_int, required=True, help="usb device vid")
    parser.add_argument("--pid", type=hex_int, required=True, help="usb device pid")
    parser.add_argument("--magic1", type=hex_int, help="first magic value", default=0x5AA555AA)
    parser.add_argument("--magic2", type=hex_int, help="second magic value", default=0xCC3300FF)

    args = parser.parse_args()

    dev = usb.core.find(idVendor=args.vid, idProduct=args.pid)
    if dev is None:
        raise RuntimeError("device not found")

    detach_drivers(dev)
    hid_set_feature(dev, struct.pack("<II", args.magic1, args.magic2))

if __name__ == "__main__":
    main()
