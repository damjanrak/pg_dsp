from pygears import gear
from pygears.typing import Uint
from pygears.common import dreg
from pygears.common import quenvelope
from pygears.common import cart, ccat
from pygears.common import project
from pygears.common import const
from pygears.cookbook import qlen_cnt
from pygears.cookbook import rng


@gear
def coefficient_loader(coefficient,
                       samples):

    window_pulse = samples | quenvelope(lvl=1)

    coefficien_num = coefficient | qlen_cnt | dreg

    # TODO: remove type cast
    coefficient_num_sync = cart(window_pulse, coefficien_num) | Uint[16]

    rng_config = ccat(const(val=0), coefficient_num_sync, const(val=1))

    read_address = rng_config | rng | project

    return read_address
