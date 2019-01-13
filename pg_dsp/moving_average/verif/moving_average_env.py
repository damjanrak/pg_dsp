from pygears import bind
# from functools import partial
# from pygears_view import PyGearsView
from pygears import gear
from pygears.sim import sim
from pygears.sim.modules import drv, SimVerilated
from pygears.typing import Uint, Int, typeof, Queue
from pg_dsp.moving_average.impl.moving_average import moving_average, TCfg
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


def moving_average_sim(din,
                       cfg,
                       sample_width,
                       cosim=True):

    result = []

    din_drv = drv(t=Queue[Uint[sample_width]], seq=[din])
    cfg_drv = drv(t=TCfg[sample_width], seq=[cfg])

    din_drv \
        | moving_average(cfg_drv,
                         sim_cls=SimVerilated if cosim else None) \
        | collect(result=result, samples_num=None)

    bind('svgen/debug_intfs', ['*'])
    sim(outdir='./build', extens=[VCD]) #, partial(PyGearsView, live=True)

    return result
