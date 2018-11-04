from pygears import gear
from pygears.common import dreg, quenvelope, ccat, cart, project, const
from pygears.cookbook import qlen_cnt, rng


@gear
def coefficient_loader(coefficient,
                       samples):

    coefficient_num = coefficient | qlen_cnt(cnt_lvl=0) | dreg

    new_window_start = samples | quenvelope(lvl=1)

    # TODO: fix tuple collapse
    coefficient_num_sync = cart(new_window_start, coefficient_num) | project

    rng_config = ccat(const(val=0), coefficient_num_sync[1], const(val=1))

    read_address = rng_config | rng(cnt_one_more=True) | project

    return read_address
