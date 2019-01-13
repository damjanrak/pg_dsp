import numpy as np
# import matplotlib.pyplot as plot
from scipy.io.wavfile import write
from pg_dsp.fir.verif.filter_maker import filter_maker
from pg_dsp.fir.verif.fir_env import fir_sim
from pg_dsp.fir.verif.fir_seqs import audio_seq


def example_synthetic(sample_rate_hz=44100,
                      nsamples=1000,
                      input_freqs_hz=[100, 1000, 3000],
                      transition_width=1 / 50,
                      ripple_db=60.0,
                      cutoff_hz=500.0,
                      fix_format=(16, 15),
                      cosim=True):

    quantized_input, quantized_taps = filter_maker(
        sample_rate_hz=sample_rate_hz,
        nsamples=nsamples,
        input_freqs_hz=input_freqs_hz,
        transition_width=transition_width,
        ripple_db=ripple_db,
        cutoff_hz=cutoff_hz,
        fix_format=fix_format)

    wav_input = np.asarray(quantized_input, dtype=np.int16)
    write('synthetic_test_input.wav', sample_rate_hz, wav_input)

    audio = audio_seq(audio_input=wav_input, filter_ord=len(quantized_taps))

    res = fir_sim(
        samples=audio,
        shamt=fix_format[1],
        coef=quantized_taps,
        sample_width=fix_format[0],
        cosim=cosim)

    wav_res = np.asarray(res, dtype=np.int16)[:, 0]

    print(f'Result length: {len(res)}')

    write('synthetic_test_output.wav', sample_rate_hz, wav_res)


if __name__ == "__main__":
    example_synthetic(nsamples=5000)
