import numpy as np
from numpy import sin, pi, arange
from scipy.signal import kaiserord, firwin
from pg_dsp.utils.py_libs.fixp import Quantizer


def filter_maker(sample_rate_hz=44100,
                 nsamples=1000,
                 input_freqs_hz=[100, 1000, 3000],
                 transition_width=1/50,
                 ripple_db=60.0,
                 cutoff_hz=500.0,
                 fix_format=(16, 15)):

    # Create signal for demonstration
    t = arange(nsamples) / sample_rate_hz
    x = 0.8*sin(2*pi*input_freqs_hz[0]*t) \
        + 0.2*sin(2*pi*input_freqs_hz[1]*t) \
        + 0.2*sin(2*pi*input_freqs_hz[2]*t)

    # The Nyquist rate of the signal.
    nyq_rate = sample_rate_hz / 2.0

    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, transition_width)

    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, cutoff_hz / nyq_rate, window=('kaiser', beta))

    # quantizer for hardware input preparation
    q = Quantizer(
        round_mode='floor',
        overflow_mode='saturate',
        fix_format=(16, 15))

    # scale input to avoid clipping
    scaled = x/np.max(np.abs(x))

    # prepare input and taps for hardware simulation
    quantized_input = q.quantize(list(scaled))
    quantized_taps = q.quantize(list(taps))

    return quantized_input, quantized_taps
