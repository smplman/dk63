import subprocess
import os
import signal
import time

gdb = 'arm-none-eabi-gdb /qmk_firmware/.build/kmove_dk63_default.elf -ex "target remote :3333"'
gdb += ' -ex "set confirm off" '
gdb += ' -ex "set pagination off" '
gdb += ' -ex "load" '
gdb += ' -ex "mon reset halt"'
gdb += ' -ex "set \\$pc=0x1FFF0301"'
gdb += ' -ex "ni 39" '
gdb += ' -ex "q"'

proc = subprocess.Popen(gdb, shell=True)
time.sleep(10)
# os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
# os.kill(proc.pid,signal.CTRL_C_EVENT)
proc.kill()
# proc.terminate()