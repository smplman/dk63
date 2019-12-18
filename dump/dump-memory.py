# example:
# python3 dump-memory.py 0 0x1000 first.bin --openocd 192.168.0.18:4444 --ldr-gadget 0x1FFF02C4 --reg1 r0 --reg2 r0

import argparse
from telnetlib import Telnet

def auto_int(x):
    return int(x, 0)

def divisible_by_4(x):
    x = int(x, 0)
    if x % 4 != 0:
        raise argparse.ArgumentTypeError("The value 0x{:X} is not divisible by 4".format(x))
    return x

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("start", type=divisible_by_4, help="start address to dump")
    parser.add_argument("size", type=divisible_by_4, help="size to dump")
    parser.add_argument("file", help="output file")
    parser.add_argument("--openocd", required=True, help="host:port of openocd telnet")
    parser.add_argument("--ldr-gadget", type=auto_int, required=True, help="address of a gadget of format ldr Reg1, [Reg2]")
    parser.add_argument("--reg1", required=True, help="register for Reg1 (e.g. r0)")
    parser.add_argument("--reg2", required=True, help="register for Reg2 (e.g. r1)")

    args = parser.parse_args()
    host, port = args.openocd.split(":")
    port = int(port)

    # set thumb bit
    args.ldr_gadget |= 1

    outf = open(args.file, "wb")

    with Telnet(host, port) as tn:
        tn.read_until(b"> ")
        tn.write(b"reset halt\n")

        for addr in range(args.start, args.start + args.size, 4):
            tn.read_until(b"> ")
            tn.write("reg pc 0x{:X}\n".format(args.ldr_gadget).encode("ascii"))

            tn.read_until(b"> ")
            tn.write("reg {} 0x{:X}\n".format(args.reg2, addr).encode("ascii"))

            tn.read_until(b"> ")
            tn.write(b"step\n")

            tn.read_until(b"> ")
            tn.write("reg {}\n".format(args.reg1).encode("ascii"))

            tn.read_until(b"\n")
            # b'r0 (/32): 0x200007B0\r\n'
            value = int(tn.read_until(b"\n").decode("ascii").split()[-1], 16)

            outf.write(value.to_bytes(4, byteorder="little"))

            print("\r[{}/{}]".format(addr - args.start + 4, args.size), end="")

        print("")

    outf.close()

if __name__ == "__main__":
    main()