def audio_window(window_start, filter_ord, audio_input):
    for i in range(filter_ord):
        yield audio_input[window_start+i]


def audio_seq(audio_input, filter_ord):
    for window_start in range(len(audio_input)-filter_ord):
        yield audio_window(window_start, filter_ord, audio_input)
