import numpy as np

from pg_dsp.moving_average.impl.moving_average import TCfg, moving_average
from pg_dsp.utils.py_libs.fixp import Quantizer
from pygears import bind, gear
from pygears.cookbook.delay import delay_rng
from pygears.cookbook.verif import verif
from pygears.sim import sim
from pygears.sim.extens.vcd import VCD
from pygears.sim.modules import SimVerilated, drv
from pygears.typing import Int, Queue, typeof


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


def moving_average_sim(din, cfg, sample_width, cosim=True):

    result = []

    din_drv = drv(t=Queue[Int[sample_width]], seq=[din])
    cfg_drv = drv(t=TCfg[sample_width], seq=[cfg])

    din_drv \
        | moving_average(cfg_drv,
                         sim_cls=SimVerilated if cosim else None) \
        | collect(result=result, samples_num=None)

    bind('svgen/debug_intfs', ['*'])
    sim(outdir='./build', extens=[VCD])

    return result


@gear
async def moving_average_ref(cfg, din) -> b'din':
    prev_data = []

    async with cfg as (coef, window_size):
        async for (data, eot) in din:
            prev_data.append((data + window_size - 1) // window_size)
            dout = sum(prev_data[-window_size:])
            yield (dout, eot)


# @pytest.mark.parametrize('din_delay', [0, 1, 10])
# @pytest.mark.parametrize('cfg_delay', [0, 1, 10])
# @pytest.mark.parametrize('dout_delay', [0, 1, 10])
def test_moving_average(tmpdir='./build',
                        cosim_cls=SimVerilated,
                        din_delay=0,
                        cfg_delay=0,
                        dout_delay=0,
                        nsamples=10,
                        window_size=5,
                        sample_width=16,
                        shamt=15):

    cfg_seq = []
    din_seq = []

    q = Quantizer(
        round_mode='floor', overflow_mode='saturate', fix_format=(16, shamt))

    rand_data = np.random.rand(nsamples)
    quantized_input = q.quantize(list(rand_data))
    din_seq.append(np.asarray(quantized_input, dtype=np.int16))

    cfg_seq.append((q.quantize(1 / window_size), window_size))

    verif(
        drv(t=TCfg[sample_width], seq=cfg_seq)
        | delay_rng(cfg_delay, cfg_delay),
        drv(t=Queue[Int[sample_width]], seq=din_seq)
        | delay_rng(din_delay, din_delay),
        f=moving_average(sim_cls=cosim_cls, shamt=shamt),
        ref=moving_average_ref(name='ref_model'),
        delays=[delay_rng(dout_delay, dout_delay)],
        tolerance=10)

    sim(outdir=tmpdir)


if __name__ == '__main__':
    test_moving_average('/tools/home/tmp', SimVerilated, 0, 0, 0)
