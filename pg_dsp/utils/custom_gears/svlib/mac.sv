module mac #(
             parameter W_DATA = 16
              )
   (
    input clk,
    input rst,
    dti.consumer din,
    dti.producer dout
    );

   typedef struct packed
                  {
                     logic eot;
                     logic [W_DATA-1 : 0] mul1;
                     logic [W_DATA-1 : 0] mul0;
                  } din_t;

   din_t din_s;
   logic [2*W_DATA-1 : 0] acc;
   logic [2*W_DATA-1 : 0] add_term;
   logic reg_cleared;
   logic acc_done;
   logic din_handshake;
   logic dout_handshake;

   assign din_s = din.data;
   assign din_handshake = din.valid && din.ready;
   assign dout_handshake = dout.valid && dout.ready;

   always_ff @(posedge clk) begin
     if (rst) begin
        acc <= 0;
     end else if (din_handshake) begin
        acc <= signed'(add_term) + (signed'(din_s.mul0) * signed'(din_s.mul1));
     end
   end

   always_ff @(posedge clk) begin
      if(rst | (din_handshake && din_s.eot))begin
         reg_cleared <= 0;
      end else begin
         reg_cleared <= din_handshake || reg_cleared;
      end
   end

   always_ff @(posedge clk) begin
      if(rst || (acc_done && dout_handshake && !din_handshake)) begin
         acc_done <= 0;
      end else if(din_handshake) begin
         acc_done <= din_s.eot;
      end
   end

   assign add_term = reg_cleared ? acc : 0;

   assign dout.valid = acc_done;
   assign din.ready = (dout.ready || !dout.valid);
   assign dout.data = acc;

 endmodule : mac
