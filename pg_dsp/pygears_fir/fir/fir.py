from pygears import gear
from pygears.typing import Queue
from pygears.common import fmap, ccat, cart, czip, project, quenvelope
from pygears.common import const, dreg
from pygears.cookbook import qcnt, sdp, qlen_cnt, rng
from pg_dsp.utils.custom_gears.mac import mac


@gear
def mac_wrap(shamt, coefs, samples):
    conv_res = czip(samples, coefs) | mac
    return (conv_res >> shamt | samples.dtype[0])


@gear
def fir(coefs,
        samples,
        *,
        shamt=15,
        coefficient_depth=2048):

    write_address = coefs \
                    | qcnt \
                    | project

    write_data = coefs | project(lvl=coefs.dtype.lvl)
    write_port = ccat(write_address, write_data)

    coefs_num = coefs \
        | qlen_cnt(cnt_lvl=0) \
        | dreg

    new_window = samples | quenvelope(lvl=1)
    dot_product_len = cart(new_window, coefs_num) | project

    rng_config = ccat(const(val=0), dot_product_len[1], const(val=1))
    read_port = rng_config \
        | rng(cnt_one_more=True) \
        | project

    coefficient_for_calc = sdp(write_port, read_port, depth=coefficient_depth)

    res = samples \
        | fmap(
            f=mac_wrap(shamt, coefficient_for_calc), fcat=czip, lvl=1) \
        | Queue[samples.dtype[0]]

    return res
