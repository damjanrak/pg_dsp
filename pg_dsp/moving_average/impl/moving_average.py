from pygears import gear, Intf
from pygears.typing import Int, Uint, Queue, Tuple, bitw
from pygears.common import fmap, czip, union_collapse, fifo
from pygears.common import ccat, cart, const, decoupler, mul, project
from pygears.cookbook import replicate, priority_mux

TDin = Queue[Uint['W']]
TCfg = Tuple[{'avr_coef': Int['W'],
              'avr_window': Uint['W']}]


@gear
def scale_input(din, *, shamt, W):
    return ((din | mul) >> shamt) | Int[W]


@gear
def delay_sample(din, cfg, *, W, max_filter_ord):
    din_window = din \
        | project \
        | fifo(depth=2**bitw(max_filter_ord))

    initial_load = ccat(cfg, const(val=0, tout=Int[W])) \
        | replicate \
        | project

    delayed_din = (initial_load, din_window) \
        | priority_mux \
        | union_collapse

    return delayed_din


@gear
def window_sum(din, add_op, sub_op, *, W=16):
    return (din + add_op - sub_op) | Int[W]


@gear
def accumulator(din, delayed_din, *, W):
    prev_window_sum = Intf(dtype=Int[W])

    average = din \
        | fmap(f=window_sum(prev_window_sum,
                            delayed_din,
                            W=W),
               lvl=din.dtype.lvl,
               fcat=czip)

    average_reg = average \
        | project \
        | decoupler

    prev_window_sum |= priority_mux(average_reg, const(val=0, tout=Int[W])) \
        | union_collapse

    return average


@gear
def moving_average(cfg: TCfg,
                   din: TDin,
                   *,
                   W=b'W',
                   shamt=15,
                   max_filter_ord=1024):

    # TODO: pg bug with overflow and eot
    din = din \
        | fmap(f=Int[16], lvl=1, fcat=czip)

    scaled_sample = cart(cfg['avr_coef'], din) \
        | fmap(f=scale_input(shamt=shamt, W=W),
               lvl=1,
               fcat=czip)

    delayed_din = delay_sample(
        scaled_sample,
        cfg['avr_window'],
        W=W,
        max_filter_ord=max_filter_ord)

    return accumulator(
        scaled_sample, delayed_din, W=W)
