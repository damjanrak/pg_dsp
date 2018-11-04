from pygears import gear
from pygears.typing import Int, Queue
from pygears.common import fmap, ccat, czip, project
from pygears.cookbook import qcnt, sdp
from dsp_hw_designs.utils.custom_gears.mac import mac
from dsp_hw_designs.pygears_fir.fir.coefficient_loader import coefficient_loader


@gear
def mac_wrap(shamt, coefs, samples):
    conv_res = czip(samples, coefs) | mac
    return (conv_res >> shamt | samples.dtype[0])


@gear
def fir(coefficient,
        samples,
        *,
        shamt=15,
        coefficient_depth=2048):

    write_address = coefficient | qcnt | project
    write_data = coefficient | project(lvl=coefficient.dtype.lvl)
    write_port = ccat(write_address, write_data)

    read_port = coefficient_loader(coefficient, samples)
    coefficient_for_calc = sdp(write_port, read_port, depth=coefficient_depth)

    res = samples | fmap(
        f=mac_wrap(shamt, coefficient_for_calc), fcat=czip, lvl=1) \
        | Queue[samples.dtype[0]]

    return res
