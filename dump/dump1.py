import subprocess
import sys

# start = int(sys.argv[1], 16)
# end = start + 0x200

# gdb = 'arm-none-eabi-gdb.exe -ex "target remote 192.168.1.6:3333" '
# gdb += ' -ex "set confirm off" '
# remap bootrom and flash memory
# gdb_si = 'set $pc=0x1FFF0169\r\n si\r\n si\r\n'
# gdb += ' -ex "set $pc=0x1FFF0169" -ex "si" -ex "si" -ex "si" '
# gdb += '-ex "q" '
# subprocess.call(gdb, shell=True)

code = b"\x08\x68\x48\x68\x88\x68\xc8\x68\x08\x69\x48\x69\x88\x69\xc8\x69"
assert len(code) % 4 == 0

# User Rom
# size = int("0xFFFF", 16)
# start = 0;

# bootloader
size = int("0x0BFF", 16)
start = int('0x1FFF0000', 16)

for i in range(0, size, 512):

    gdb = 'arm-none-eabi-gdb.exe -ex "target remote 192.168.1.6:3333"'
    gdb += ' -ex "set confirm off" '

    # address = '0x' + hex(i)[2:].zfill(2).upper()
    # address = int(address, 16)
    address = start + i
    # print(address)

    for x in range(0, len(code) // 4):
        chunk = code[4 * x:4 * (x + 1)]
        cmd = "set *(int*)0x{:X}=0x{:X}".format(0x20000000 + x * 4, int.from_bytes(chunk, byteorder="little"))

        gdb += ' -ex "{}"'.format(cmd)

    end = address + 0x200

    for addr in range(address, end, 32):
        gdb += ' -ex "set \\$pc=0x20000001"'
        gdb += ' -ex "set \\$r1=0x{:X}"'.format(addr)

        for x in range(8):
            gdb += ' -ex "si" '
            gdb += '-ex "p/x \\$r0" '

    gdb += '-ex "q"'

    # print(gdb)

    subprocess.call(gdb + "> ./out/output-0x{:X}-0x{:X}.log".format(address, end), shell=True)
    gdb = ''

# print("")
# print("Next, python3 code.py 0x{:X}".format(end))