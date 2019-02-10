import numpy as np
from random import gauss
from numpy import sin, pi, arange
from pg_dsp.utils.py_libs.fixp import Quantizer
from scipy.io.wavfile import write
from pg_dsp.moving_average.verif.moving_average_env import moving_average_sim


def add_white_gaussian_noise(signal, magnitude):
    with_noise = []
    gaussian_noise = [gauss(0.0, 1.0) for i in range(len(signal))]
    for i, sample in enumerate(signal):
        with_noise.append(sample + magnitude*gaussian_noise[i])

    return with_noise


def example_synthetic(nsamples,
                      sample_rate_hz=44100,
                      window_size=20):

    t = arange(nsamples) / sample_rate_hz

    x = 0.8*sin(2*pi*100*t)
    x = add_white_gaussian_noise(x, 0.2)

    # quantizer for hardware input preparation
    q = Quantizer(
        round_mode='floor',
        overflow_mode='saturate',
        fix_format=(16, 15))

    # scale input to avoid clipping
    scaled = x/np.max(np.abs(x))

    # prepare input and taps for hardware simulation
    quantized_input = q.quantize(list(scaled))

    #OBRISI
    with open('../../pg_dsp/moving_average/comparison/rtl_verif/input_samples.txt', 'w') as f:
        for i, sample in enumerate(quantized_input):
            eot = 0
            if i == len(quantized_input) - 1:
                eot = 1
            f.write(f'{eot}{format(sample, "016b")}\n')
    #OBRISI

    cfg = (q.quantize(1/window_size), window_size)

    wav_input = np.asarray(quantized_input, dtype=np.int16)
    write('moving_average_input.wav', sample_rate_hz, wav_input)

    res = moving_average_sim(din=wav_input,
                             cfg=cfg,
                             sample_width=16)
    #OBRISI
    with open('../../pg_dsp/moving_average/comparison/rtl_verif/ref_model.txt', 'w') as f:
        for sample in res:
            f.write(f'{sample[1]}{format(sample[0], "016b")}\n')
    #OBRISI

    wav_res = np.asarray(res, dtype=np.int16)[:, 0]

    print(f'Result length: {len(res)}')

    write('moving_average_output.wav', sample_rate_hz, wav_res)


if __name__ == "__main__":
    example_synthetic(nsamples=10000, window_size=5)
