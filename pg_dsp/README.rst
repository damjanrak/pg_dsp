Hardware accelerators for DSP algorithms
========================================

Here you can find implementation of various (currently only one :-D) hardware modules (accelerators) for common DSP algorithms. Hardware modules are divided by directory organization. Beside accelerator implementation there is **utils** directory which contain implementations of custom gears and python libraries needed for DSP like *Quantizer* for number conversion from floating point to fix point. Custom gears like *mac.py* are necessary to achieve performance on diferent platforms like Xilinx's FPGAs. For example, synthesis algorithms are not capable of mapping multiplication followed by addition to hard DSP block if these two components are written in two different **SystemVerilog** modules which will be the case if we use pure **PyGears** blocks for this purpose. Of course, this limitation of synthesis tools is absent in ASIC design flow. On the other hand, synthesis tools are very powerful in cross optimization between modules that are mapped to LUTs and in that case (which is vast majority) you do not need custom gears.

Projects organization
---------------------

Every project will contain at least three subdirectories:

- project_name
- implementation
- verif
|
**Project_name** directory will contain hardware implementation of accelerator written in **PyGears**.

**Implementation** consist of all scripts needed for synthesizable code generation.

**Verif** folder will contain files needed for simulation (verification)
