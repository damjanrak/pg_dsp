Finite Impulse Response *(FIR)* system - discrete convolution
=============================================================

FIR filter will be implemented from scratch using a novel approach for HW design, **PyGears**. Firstly, I will create simple accelerator which will use one multiplier to calculate system response. Beside that, simple test environment written in pure python will be developed. Also, you will find additional libraries like Quantizer in same repo but in directory named utils.

System will be tested in simulation as well as on FPGA.

Test environment will contain tests for audio filtering, reverberation and some simple image processing algorithms.

At the end of FIR implementation I will show how you can benefite from **PyGears** in terms of reusability and scalability. Examples will present parallelization and other interesting stuf for hardware guys.
