class Quantizer:
    def __init__(self,
                 round_mode='ceil',
                 overflow_mode='saturate',
                 fix_format=(16, 8)):
        self.round_mode=round_mode
        self.overflow_mode=overflow_mode
        self.integer_len=fix_format[0]-fix_format[1]
        self.fraction_len=fix_format[1]

    def quantize(self, float_number):
        integer_part = int(float_number)
        fraction_part = abs(integer_part - float_number)
        return float_number
