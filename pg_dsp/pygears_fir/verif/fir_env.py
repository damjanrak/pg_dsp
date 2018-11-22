from pygears import gear
from pygears.sim import sim
from pygears.sim.modules import drv, SimVerilated
from pygears.typing import Int, typeof, Queue
from pg_dsp.pygears_fir.fir.fir import fir
from pygears.sim.extens.vcd import VCD


@gear
async def collect(din, *, result, samples_num):
    async with din as val:
        if len(result) % 10 == 0:
            if samples_num is not None:
                print(
                    f"Calculated {len(result)}/{samples_num} samples",
                    end='\r')
            else:
                print(f"Calculated {len(result)} samples", end='\r')

        if typeof(din.dtype, Int):
            result.append(int(val))
        else:
            result.append((int(val[0]), int(val[1])))


def fir_sim(samples,
            coef,
            shamt,
            sample_width,
            cosim=True):

    result = []
    samples_din = drv(t=Queue[Int[sample_width], 2], seq=[samples])
    coef_din = drv(t=Queue[Int[sample_width]], seq=[coef])

    samples_din \
        | fir(coef_din,
              shamt=shamt,
              sim_cls=SimVerilated if cosim else None) \
        | collect(result=result, samples_num=None)

    sim(outdir='./build', extens=[VCD])

    return result
