import os
# import shutil

from parallel_fir import parallel_fir
from pygears import Intf
# from pygears.definitions import COMMON_SVLIB_DIR
from pygears.svgen import svgen
from pygears.typing import Queue, Uint
from pygears.util.print_hier import print_hier

parallel_fir(Intf(Queue[Uint[16]], ), Intf(Queue[Uint[16], 2]))
svgen('/parallel_fir', outdir='build/parallel_fir', wrapper=True)

print(f'Generated SystemVerilog files inside {os.path.abspath("build/parallel_fir")}')

print()
print_hier()
print()

# print(f'Creating Vivado project inside {os.path.abspath("build/echo/vivado")}')

# shutil.rmtree('build/echo/vivado', ignore_errors=True)

# viv_cmd = (f'vivado -mode batch -source echo_synth.tcl -nolog -nojournal'
#            f' -tclargs {COMMON_SVLIB_DIR}')

# if os.system(viv_cmd) == 0:
#     with open('build/echo/echo_utilization.txt') as f:
#         print(f.read())
