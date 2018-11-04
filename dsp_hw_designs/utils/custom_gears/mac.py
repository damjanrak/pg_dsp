from pygears import gear
from pygears.typing import Queue, Tuple, Int


@gear
def mac(din: Queue[Tuple[Int['w_data'], Int['w_data']]]) -> Int[b'2*w_data']:
    pass

