module wrap_moving_average
  (
   input               clk,
   input               rst,
   output logic        cfg_ready,
   input logic         cfg_valid,
   input logic [31:0]  cfg_data,
   output logic        din_ready,
   input logic         din_valid,
   input logic [16:0]  din_data,
   input logic         dout_ready,
   output logic        dout_valid,
   output logic [16:0] dout_data

   );

   moving_average moving_average(
                                 .ap_clk(clk),
                                 .ap_rst(rst),

                                 .din_V(din_data),
                                 .din_V_ap_vld(din_valid),
                                 .din_V_ap_ack(din_ready),
                                 .cfg_V(cfg_data),
                                 .cfg_V_ap_vld(cfg_valid),
                                 .cfg_V_ap_ack(cfg_ready),
                                 .dout_V_V(dout_data),
                                 .dout_V_V_ap_vld(dout_valid),
                                 .dout_V_V_ap_ack(dout_ready)
                                 );

endmodule
