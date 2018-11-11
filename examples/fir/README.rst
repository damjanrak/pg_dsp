FIR example
===========

Finite impulese response system is used as filter and tested on synthetic sound. If you run script in this directory it will execute function which will create low-pass filter with cut-off frequency set by default at 500Hz. Then, it will generate synthetic sound which consists of three different sine waves (100Hz, 1000Hz and 3000Hz). Both, generated input and filter coefficients will pass through Quantizer which prepare signals for real hardware (quantizes them to fix-point representation). After preparation input signal is saved as .wav file named *synthetic_test_input.wav* and pass to hardware simulator. After simulation, hardware output is saved as .wav file in file named *synthetic_test_output.wav*.

To hear difference between input and output signals just play created .wav files. In *synthetic_test_input.wav* you should hear all three frequencies unlike in *synthetic_test_output.wav* where you should hear only lowest one. If you are more visual person see image below which visualize input and output of filter.

To play with example you can change filter type, input frequences, number format etc.

**NOTE**: To hear something meanful run function with at least 5000 samples (duration > 0.1s) which will create sound long enough to be captured by human.

.. image:: example_fir_synthetic.png
   :align: center
