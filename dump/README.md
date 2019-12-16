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