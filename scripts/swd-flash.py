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
    parser.add_argument("file", help="file to flash")
    parser.add_argument("--openocd", required=True, help="host:port of openocd telnet")

    args = parser.parse_args()
    host, port = args.openocd.split(":")
    port = int(port)

    with open(args.file, "rb") as inf:
        data = inf.read()

    if len(data) > 0x8000:
        raise RuntimeError("firmware too large")

    if len(data) % 64 != 0:
        raise RuntimeError("firmware not aligned")

    # data = data[0:0x100]

    with Telnet(host, port) as tn:
        tn.read_until(b"> ")
        tn.write(b"reset halt\n")

        tn.read_until(b"> ")
        tn.write(b"reg xPSR 0xc1000000\n")

        tn.read_until(b"> ")
        tn.write(b"bp 0x1FFF0206 2 hw\n")

        for addr in range(0, len(data), 64):
            chunk = data[addr:addr+64]
            for x in range(64):
                tn.read_until(b"> ")
                tn.write("mwb 0x{:X} 0x{:X}\n".format(0x20000000 + x, chunk[x]).encode("ascii"))

            tn.read_until(b"> ")
            tn.write("reg r0 0x{:X}\n".format(addr).encode("ascii"))

            tn.read_until(b"> ")
            tn.write(b"reg r1 0x40\n")

            tn.read_until(b"> ")
            tn.write(b"reg r2 0x20000000\n")

            tn.read_until(b"> ")
            tn.write(b"reg pc 0x1FFF01CD\n")

            tn.read_until(b"> ")
            tn.write(b"resume\n")
            tn.read_until(b"halted")

            # tn.interact()

            print("\r[{}/{}]".format(addr + 64, len(data)), end="")

        print("")

if __name__ == "__main__":
    main()