from pygears import gear
from pygears.common import ccat
from pygears.common import dreg
from pygears.common import project
from pygears.cookbook import sdp
from pygears.cookbook import mac
from pygears.cookbook import qcnt
from coefficient_loader import coefficient_loader


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

    return ccat(samples | dreg, coefficient_for_calc) | mac
