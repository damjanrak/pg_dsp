class Quantizer:
    def __init__(self,
                 round_mode='floor',
                 overflow_mode='saturate',
                 fix_format=(16, 8)):
        self.round_mode = round_mode
        self.overflow_mode = overflow_mode
        self.fix_len = fix_format[0]
        self.fraction_len = fix_format[1]
        self.fix_range = 2**(fix_format[0] - fix_format[1] - 1)

    def quantize(self, floats):
        if isinstance(floats, list):
            return self.quantize_list(floats)
        else:
            return self.quantize_num(floats)

    def quantize_list(self, float_number_list):
        quant_list = []
        for float_number in float_number_list:
            quant_list.append(self.quantize_num(float_number))
        return quant_list

    def quantize_num(self, float_number):
        if self.overflow_mode == 'saturate':
            if not (-self.fix_range <= float_number <= self.fix_range):
                if float_number > 0:
                    return 2**(self.fix_len - 1)
                else:
                    return -2**self.fix_len

        shifted_float = float_number * (2**self.fraction_len)
        shifted = int(shifted_float)

        if self.round_mode == 'round_to_nearest':
            error = shifted_float - shifted
            if abs(error) > 0.5:
                if error > 0:
                    shifted = shifted + 1
                else:
                    shifted = shifted - 1

        sign_extended = shifted & (2**self.fix_len - 1)

        return sign_extended
