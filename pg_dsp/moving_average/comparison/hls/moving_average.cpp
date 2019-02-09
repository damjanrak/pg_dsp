// #include "/tools/Xilinx/Vivado/2018.3/include/gmp.h"
// Proposed solution to Vivado HLS gmp bug

#include "ap_int.h"
#include "moving_average.h"

void moving_average(hls::stream<din_t> &din,  hls::stream<cfg_t> &cfg, hls::stream<din_t> &dout) {
#pragma HLS interface ap_ctrl_none port=return
#pragma HLS data_pack variable=din
#pragma HLS data_pack variable=cfg
#pragma HLS data_pack variable=dout
#pragma HLS INTERFACE ap_hs port=cfg
#pragma HLS INTERFACE ap_hs port=din
#pragma HLS INTERFACE ap_hs port=dout

  data_t shift_reg[MAX_SIZE];
  ap_uint<16> window;
  data_t coef;
  cfg_t cfg_s;
  din_t din_s;
  din_t dout_s;

  data_t tmp;
  data_t accum = 0;

  data_t data;
  ap_uint<1> eot;

  cfg.read(cfg_s);

  window = cfg_s.average_window;
  coef = cfg_s.average_coef;

  do {
    din.read(din_s);
    data = din_s.data;
    eot = din_s.eot;

    tmp = coef * data;
    accum = 0;
  accum_loop: for (int i = window-1; i >= 0; i--) {
#pragma HLS PIPELINE rewind
#pragma HLS dependence variable=shift_reg inter false
      if (i == 0) {
        accum += tmp;
        shift_reg[i] = tmp;
      } else {
        accum += shift_reg[i-1];
        shift_reg[i] = shift_reg[i-1];
      }
    }
    dout_s.data = accum;
    dout_s.eot = eot;
    dout.write(dout_s);
  } while (! eot);
}
