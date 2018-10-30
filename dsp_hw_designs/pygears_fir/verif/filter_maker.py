# import pickle
import numpy as np
from numpy import sin, pi, arange
# from scipy.io.wavfile import write
from scipy.signal import kaiserord, firwin
from dsp_hw_designs.utils.fixp import Quantizer


def filter_maker():
    sample_rate = 44100
    nsamples = 100000
    # Create signal for demonstration
    t = arange(nsamples) / sample_rate
    x = 0.8*sin(2*pi*100*t) + 0.2*sin(2*pi*1000*t) + 0.2*sin(2*pi*3000*t)

    # ------------------------------------------------
    # Create a FIR filter and apply it to x.
    # ------------------------------------------------

    # The Nyquist rate of the signal.
    nyq_rate = sample_rate / 2.0

    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate. Width[Hz] = 1/50 * nyq_rate
    width = 1 / 50

    # The desired attenuation in the stop band, in dB.
    ripple_db = 60.0

    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)

    # The cutoff frequency of the filter.
    cutoff_hz = 500.0

    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, cutoff_hz / nyq_rate, window=('kaiser', beta))

    # quantizer for hardware input preparation
    q = Quantizer(
        round_mode='round_to_nearest',
        overflow_mode='saturate',
        fix_format=(16, 15))

    # scale input to avoid clipping
    scaled = x/np.max(np.abs(x))

    # prepare input and taps for hardware simulation
    quantized_input = q.quantize(list(scaled))
    quantized_taps = q.quantize(list(taps))

    # with open('hw_taps.pickle', "wb") as tp:
    #     pickle.dump(quantized_taps, tp)
    # with open('hw_input.pickle', "wb") as ip:
    #     pickle.dump(quantized_input, ip)

    # # save original and filtered signal
    # write('input.wav', sample_rate, x)
    # filtered_x = lfilter(taps, 1.0, x)
    # write('output.wav', sample_rate, filtered_x)

    return quantized_input, quantized_taps
