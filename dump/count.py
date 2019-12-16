
rom_size = int("0xFFFF", 16)

for i in range(0,rom_size,512):
    # print(i)
    # print(hex(i).zfill(2))
    # print(hex(i)[2:].zfill(2).upper())
    address = '0x' + hex(i)[2:].zfill(2).upper()
    # print(int(address,16))