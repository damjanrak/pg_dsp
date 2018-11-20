from pygears import gear
from pygears.typing import Queue, Tuple, Int

TDin = Queue[Tuple[Int['w_data'], Int['w_data']]]

@gear
def mac(din: TDin) -> Int[b'2*w_data']:
    pass
