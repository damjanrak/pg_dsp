library ieee;
use ieee.std_logic_1164.all;
use ieee.NUMERIC_STD.all;
use work.moving_average_pkg.all;

entity moving_average is
  generic(W : natural := 16;
          max_filter_ord : natural := 1024;
          shamt : natural := 15);
  port(	clk: 	in std_logic;
        rst:	in std_logic;
        cfg_valid: in std_logic;
        cfg_ready: out std_logic;
        cfg: in std_logic_vector(2*W-1 downto 0);
        din_valid: in std_logic;
        din_ready: out std_logic;
        din: in std_logic_vector(W downto 0);
        dout_valid: out std_logic;
        dout_ready: in std_logic;
        dout: out signed(W downto 0));
end moving_average;

architecture FSMD of moving_average is

  type state_t is (idle, transition, steady);
  type t2d_array is array (0 to max_filter_ord) of signed(W-1 downto 0);
  signal state_reg, state_next: state_t;
  signal memory: t2d_array;
  attribute ram_style : string;
  attribute ram_style of memory : signal is "bram";
  signal rd_ptr_reg, rd_ptr_next: unsigned(log2c(max_filter_ord) downto 0);
  signal wr_ptr_reg, wr_ptr_next: unsigned(log2c(max_filter_ord) downto 0);
  signal din_handshake: std_logic;
  signal out_of_window: signed(W-1 downto 0);
  signal cfg_test: unsigned(W-1 downto 0);
  signal din_ready_s: std_logic;
  signal scaled_sample: signed(W-1 downto 0);
  signal multiplier: signed(2*W-1 downto 0);
  signal avr_coef: signed(W-1 downto 0);
  signal avr_window: unsigned(W-1 downto 0);
  signal last_din: std_logic;
  signal sample: signed(W-1 downto 0);
  signal accum_next, accum_reg : signed(W-1 downto 0);
  signal reg_ready, reg_empty, valid_reg: std_logic;
  signal dout_reg: signed(W downto 0);
begin

  avr_coef <= signed(cfg(2*W-1 downto W));
  avr_window <= unsigned(cfg(W-1 downto 0));
  last_din <= din(W);
  sample <= signed(din(W-1 downto 0));

  -- CONTROL PATH
  process(clk)
  begin
    if clk'event and clk = '1' then
      if rst = '1' then
        state_reg <= idle;
      else
        state_reg <= state_next;
      end if;
    end if;
  end process;

  process(state_reg, cfg_valid, din_valid, avr_window, wr_ptr_reg, wr_ptr_next, last_din)
  begin
    state_next <= state_reg;
    case (state_reg) is
      when idle =>
        if (cfg_valid and din_valid) = '1' then
          state_next <= transition;
        end if;
      when transition =>
        -- if (wr_ptr_reg >= shift_right(avr_window, 1)) then
        if (wr_ptr_reg >= avr_window) then
          state_next <= steady;
        end if;
      when steady =>
        if last_din = '1' then
          state_next <= idle;
        end if;
      when others =>
    end case;
  end process;

  -- INPUT LOGIC
  process(state_reg, last_din, din_handshake)
  begin
    cfg_ready <= '0';
    if state_reg = steady and last_din = '1' then
      cfg_ready <= din_handshake;
    end if;
  end process;

  din_handshake <= din_valid and din_ready_s;
  din_ready_s <= reg_ready;
  din_ready <= din_ready_s;
  --------------------------
  --       DATA PATH      --
  --------------------------
  -- FIFO LOGIC
  process(clk)
  begin
    if clk'event and clk = '1' then
      if rst = '1' then
        rd_ptr_reg <= (others=>'0');
        wr_ptr_reg <= (others=>'0');
      else
        if (din_handshake = '1') then
          rd_ptr_reg <= rd_ptr_next;
          wr_ptr_reg <= wr_ptr_next;
        end if;
      end if;
    end if;
  end process;

  multiplier <= shift_right((sample * signed(cfg(2*W-1 downto W))), shamt);
  scaled_sample <= multiplier(W-1 downto 0);

  --FIFO LOGIC
  process(state_reg, wr_ptr_reg, rd_ptr_reg, state_next)
  begin
    wr_ptr_next <= wr_ptr_reg;
    rd_ptr_next <= rd_ptr_reg;
    case (state_reg) is
      when idle =>
        rd_ptr_next <= (others=>'0');
        wr_ptr_next <= ((0)=>'1', others=>'0');
      when transition =>
        wr_ptr_next <= wr_ptr_reg + 1;
      when steady =>
        wr_ptr_next <= wr_ptr_reg + 1;
        rd_ptr_next <= rd_ptr_reg + 1;
      when others=>
    end case;
  end process;

  process(clk)
  begin
    if clk'event and clk = '1' then
      if rst = '1' then
        out_of_window <= (others=>'0');
      else
        if state_next /= steady then
          out_of_window <= (others=>'0');
        else
          out_of_window <= memory(to_integer(rd_ptr_reg(log2c(max_filter_ord)-1 downto 0)));
        end if;
      end if;
    end if;
  end process;

  process(clk)
  begin
    if clk='1' and clk'event then
      if (din_handshake = '1') then
        memory(to_integer(wr_ptr_reg(log2c(max_filter_ord)-1 downto 0))) <= scaled_sample;
      end if;
    end if;
  end process;

  -- ACCUMULATOR LOGIC
  process(clk)
  begin
    if clk'event and clk = '1' then
      if rst = '1' then
        accum_reg <= (others=>'0');
      else
        if (din_handshake='1') then
          accum_reg <= accum_next;
        end if;
      end if;
    end if;
  end process;

  accum_next <= accum_reg + scaled_sample - out_of_window;

  -- OUTPUT LOGIC
  reg_ready <= reg_empty or dout_ready;
  reg_empty <= not valid_reg;

  process(clk)
  begin
    if clk'event and clk='1' then
      if rst = '1' then
        valid_reg <= '0';
      elsif reg_ready = '1' then
        if ((state_next = transition) or (state_reg /= idle)) then
          valid_reg <= din_valid;
        else
          valid_reg <= '0';
        end if;
        dout_reg <= last_din & accum_next;
      end if;
    end if;
  end process;

  dout <= dout_reg;
  dout_valid <= valid_reg;



end;
