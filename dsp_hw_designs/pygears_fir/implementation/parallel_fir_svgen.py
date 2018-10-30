import os

from pygears_fir.fir.parallel_fir import parallel_fir
from pygears import Intf
from pygears.svgen import svgen
from pygears.typing import Queue, Uint
from pygears.util.print_hier import print_hier

parallel_fir(Intf(Queue[Uint[16]], ), Intf(Queue[Uint[16], 2]))
svgen('/parallel_fir', outdir='build/parallel_fir', wrapper=True)

print(
    f'Generated SystemVerilog files inside {os.path.abspath("build/parallel_fir")}'
)

print()
print_hier()
print()
