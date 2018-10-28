from scipy.io.wavfile import write

from pygears_fir.fir.parallel_fir import parallel_fir
from pygears import gear
from pygears.sim import sim
from pygears.sim.modules import drv, SimVerilated
from pygears.typing import Int, typeof, Queue
from pygears_fir.verif.filter_maker import filter_maker


def wav_fir_sim(sample_rate=44100,
                cosim=True):
    """Applies fir coefs on a WAV file using Verilator cosimulation
    ifn - quantized input
    coef - quantized fir taps
    ofn - hardware output
    """

    quantized_input, quantized_taps = filter_maker()

    res = mono_fir_sim(
        samples=quantized_input,
        coef=quantized_taps,
        sample_width=16,
        cosim=cosim)

    print(f'Result length: {len(res)}')

    write('fir_output.wav', sample_rate, res)


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


def mono_fir_sim(samples,
                 coef,
                 sample_width,
                 cosim=True):

    result = []
    # TODO: generate real queues
    samples_din = drv(t=Queue[Int[sample_width], 2], seq=samples)
    coef_din = drv(t=Queue[Int[sample_width]], seq=coef)

    samples_din \
        | parallel_fir(coef_din,
                       sim_cls=SimVerilated if cosim else None) \
        | collect(result=result, samples_num=len(samples))

    sim(outdir='./build')

    return result
