import os

from pygears import Intf
from pygears.svgen import svgen
from pygears.typing import Queue, Uint
from pygears.util.print_hier import print_hier
from dsp_hw_designs.pygears_fir.fir.fir import fir

fir(Intf(Queue[Uint[16]], ), Intf(Queue[Uint[16], 2]))
svgen('/fir', outdir='build/fir', wrapper=True)

print(
    f'Generated SystemVerilog files inside {os.path.abspath("build/fir")}'
)

print()
print_hier()
print()
