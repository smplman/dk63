# Upload firmware

# start openocd
openocd:
	# "openocd.exe" "-c" "gdb_port 3333" "-s" "C:\Users\smplman\projects\qmk_firmware-19" "-f" "C:\Users\smplman\projects\dk63\stlink.cfg" "-f" "C:\Users\smplman\projects\dk63\vs11k09a-1.cfg"
	openocd -c "gdb_port 3333" -s /dk63 -f stlink.cfg &

# Put device into bootloader mode
dfu:
	# python3 C:\Users\smplman\projects\qmk_firmware-19\util\dk63\dfu.py
	python3 /dk63/scripts/dfu.py

# run python script to upload the firmware
upload:
	# python3 C:\Users\smplman\projects\qmk_firmware-19\util\dk63\flash-firmware.py C:\Users\smplman\projects\qmk_firmware-19\.build\kmove_dk63_default.bin --vid 0x0c45 --pid 0x7040
	python3 /dk63/scripts/flash-firmware.py /qmk_firmware/.build/kmove_dk63_default.bin --vid 0x0c45 --pid 0x7040

# stop openocd
openocd-stop:
	pkill openocd

# start gdb session
gdb:
	# arm-none-eabi-gdb.exe ./.build/kmove_dk63_default.elf -ex "target remote :3333" -ex "set confirm off" -ex "set pagination off"
	arm-none-eabi-gdb /qmk_firmware/.build/kmove_dk63_default.elf -ex "target remote :3333" -ex "set confirm off" -ex "set pagination off"

# dfu and upload
all: openocd dfu openocd-stop upload