import numpy as np
from scipy.io.wavfile import write
from dsp_hw_designs.pygears_fir.verif.filter_maker import filter_maker
from dsp_hw_designs.pygears_fir.verif.fir_env import fir_sim


def audio_window(window_start, filter_ord, audio_input):
    for i in range(filter_ord):
        yield audio_input[window_start+i]


def audio_seq(audio_input, filter_ord):
    for window_start in range(len(audio_input)-filter_ord):
        yield audio_window(window_start, filter_ord, audio_input)


def taps_seq(taps):
    for tap in taps:
        yield tap


def synthetic_test(sample_rate_hz=44100,
                   nsamples=1000,
                   input_freqs_hz=[100, 1000, 3000],
                   transition_width=1/50,
                   ripple_db=60.0,
                   cutoff_hz=500.0,
                   fix_format=(16, 15),
                   cosim=True):

    quantized_input, quantized_taps = filter_maker(sample_rate_hz=sample_rate_hz,
                                                   nsamples=nsamples,
                                                   input_freqs_hz=input_freqs_hz,
                                                   transition_width=transition_width,
                                                   ripple_db=ripple_db,
                                                   cutoff_hz=cutoff_hz,
                                                   fix_format=fix_format)

    wav_input = np.asarray(quantized_input, dtype=np.int16)
    write('synthetic_test_input.wav', sample_rate_hz, wav_input)

    audio = audio_seq(audio_input=quantized_input,
                      filter_ord=len(quantized_taps))

    taps = taps_seq(quantized_taps)

    res = fir_sim(
        samples=audio,
        shamt=fix_format[1],
        coef=taps,
        sample_width=fix_format[0],
        cosim=cosim)

    wav_res = np.asarray(res, dtype=np.int16)[:, 0]

    print(f'Result length: {len(res)}')

    write('synthetic_test_output.wav', sample_rate_hz, wav_res)
