import numpy as np
from scipy.io.wavfile import write

def bin_to_dec(line):
    length = len(line) - 1
    dec = 0
    for pos, c in enumerate(line):
        if pos > 0:
            if c == '1':
                dec += 2 ** (length-pos-1)
    return dec

audio = []
with open('output_samples.txt') as f:
    for line in f:
        audio.append(bin_to_dec(line));

wav_input = np.asarray(audio, dtype=np.int16)
write('moving_average_output.wav', 44100, wav_input)


