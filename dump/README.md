then just run "python3 code.py 0" then "python3 code.py 0x200" 0x400 0x600 and so on
(that's the first script)
then run the second script and it'll join them all into output.bin


'-ex "set \\$pc=0x1FFF0169" -ex "si" -ex "si" -ex "si"'
set $pc=0x1FFF0169
si
si
si
info reg
si
si
info reg

then run dump1.py

# gdb
'arm-none-eabi-gdb.exe -ex "target remote 192.168.1.6:3333" '

# dump-memory.py

python3 dump-memory.py 0x1FFF0000 0x100 test.bin --openocd 192.168.1.6:4444 --ldr-gadget 0x1FFF0420 --reg1 r0 --reg2 r0