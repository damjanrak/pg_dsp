from pygears import gear
from pygears.common import fmap
from pygears.common import ccat, czip
from pygears.common import dreg
from pygears.common import project
from pygears.cookbook import sdp
from pygears.cookbook import qcnt
from pygears_fir.fir.mac import mac
from pygears_fir.fir.coefficient_loader import coefficient_loader


@gear
def mac_wrap(coefs, samples):
    return czip(samples, coefs) | mac


@gear
def parallel_fir(coefficient,
                 samples):

    write_address = coefficient | qcnt | project

    write_data = coefficient | project(lvl=coefficient.dtype.lvl)

    write_port = ccat(write_address, write_data)

    read_port = coefficient_loader(coefficient, samples)

    coefficient_for_calc = sdp(write_port,
                               read_port,
                               depth=256)

    res = samples | fmap(f=mac_wrap(coefficient_for_calc), lvl=1)

    return res
