# Hardware accelerators for DSP algorithms - novel hardware design approach PYGEARS
I will go through hardware implementation of numerous accelerators targeting mostly DSP algorithms. This blog will try to explain power of new hw design methodology incorporated in PYGEARS.

## Finite Impulse Response *(FIR)* system - discrete convolution
FIR filter will be implemented from scratch using a novel approach for HW design, PYGEARS. Firstly, I will create simple accelerator which will use one multiplier to calculate system response. Beside that, simple test environment written in pure python will be developed. Also, you will find additional libraries like Quantizer in same repo.

System will be tested in simulation as well as on FPGA.

Test environment will contain tests for audio filtering, reverberation and some simple image processing algorithms.

At the end of FIR implementation I will show how you can benefite from PYGEARS in terms of reusability and scalability. Example will present parallelization and other interesting stuf for hardware guys.
