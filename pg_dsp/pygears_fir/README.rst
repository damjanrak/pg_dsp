Finite Impulse Response *(FIR)* system - discrete convolution
=============================================================

FIR systems are commonly used for digital signal processing. They can do signal filtration when used as filters or discrete convolution. These are the most popular applications of FIR systems. 

As name says FIR system has impulse response of finite durations, because its respons on discrete delta impulse setls down to zero in finite time. It's output equation is:

|

.. math:: \begin{equation}
              \sum_{x=1}^{n}x^2=1
          \end{equation}

|

will be implemented from scratch using a novel approach for HW design, **PyGears**. Firstly, I will create simple accelerator which will use one multiplier to calculate system response. Beside that, simple test environment written in pure python will be developed. Also, you will find additional libraries like Quantizer in same repo but in directory named utils.

System will be tested in simulation as well as on FPGA.

Test environment will contain tests for audio filtering, reverberation and some simple image processing algorithms.

At the end of FIR implementation I will show how you can benefite from **PyGears** in terms of reusability and scalability. Examples will present parallelization and other interesting stuff for hardware guys.
