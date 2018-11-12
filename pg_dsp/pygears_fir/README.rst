FIR systems are commonly used for digital signal processing. They can do
signal filtration when used as filters or discrete convolution. These
are the most popular applications of FIR systems.

As name says FIR system has impulse response of finite durations. That
means if we drive discrete delta impulse at FIR input its respons will
setls down to zero in finite time. Discrete delta impuls can be written
as in equation:

.. math::

   \begin{aligned}
       \delta(n) = 
       \left\{
           \begin{array}{ll}
               1 & \mbox{if } x = 0 \\
               0 & \mbox{if } x \neq 0
           \end{array}
       \right.     \end{aligned}

It’s output equation is:

.. math::

   \begin{aligned}
   y(n) = \sum_{i=0}^{n}{b_{i} \cdot u(n-i)}\end{aligned}
