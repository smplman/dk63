# Upload firware

# Put device into bootloader mode
openocd:
	openocd -f stlink.cfg &

openocd-stop:
	pkill openocd

dfu:
	python3 ./scripts/dfu.py

# run python script to upload the firmware
upload:
	python3 ./scripts/flash-firmware-hid.py ../qmk_firmware-9/.build/kmove_dk63_default.bin --vid 0x0c45 --pid 0x7040

gdb:
	arm-none-eabi-gdb ../qmk_firmware-9/.build/kmove_dk63_default.elf -ex "target remote :3333" -ex "set confirm off"