library ieee;
use ieee.std_logic_1164.all;
use ieee.NUMERIC_STD.all;
use std.textio.all;
use work.moving_average_pkg.all;

entity moving_average_tb is
end moving_average_tb;

architecture behavioral of moving_average_tb is

  constant W: natural := 16;

  component moving_average is
  generic(W : natural := 16;
          max_filter_ord : natural := 1024);
  port(	clk: 	in std_logic;
        rst:	in std_logic;
        cfg_valid: in std_logic;
        cfg_ready: out std_logic;
        cfg: in std_logic_vector(2*W-1 downto 0);
        din_valid: in std_logic;
        din_ready: out std_logic;
        din: in signed(W downto 0);
        dout_valid: out std_logic;
        dout_ready: in std_logic;
        dout: out signed(W downto 0));
  end component;

  signal clk_s: std_logic;
  signal rst_s:	std_logic;
  signal cfg_valid_s: std_logic;
  signal cfg_ready_s: std_logic;
  signal cfg_s: std_logic_vector(2*W-1 downto 0);
  signal din_valid_s: std_logic;
  signal din_ready_s: std_logic;
  signal din_s: signed(W downto 0);
  signal dout_valid_s: std_logic;
  signal dout_ready_s: std_logic;
  signal dout_s: signed(W downto 0);
  file input_test_vector : text open read_mode is "input_samples.txt";

  function to_std_logic_vector(s: string) return std_logic_vector is
    variable slv: std_logic_vector(s'high-s'low downto 0);
    variable k: integer;
  begin
    k := s'high-s'low;
    for i in s'range loop
      slv(k) := to_std_logic(s(i));
      k      := k - 1;
    end loop;
    return slv;
  end to_std_logic_vector;

begin

  dut: moving_average
    generic map(W=>W)
    port map(clk=>clk_s,
             rst=>rst_s,
             cfg_valid=>cfg_valid_s,
             cfg_ready=>cfg_ready_s,
             cfg=>cfg_s,
             din_valid=>din_valid_s,
             din_ready=>din_ready_s,
             din=>din_s,
             dout_valid=>dout_valid_s,
             dout_ready=>dout_ready_s,
             dout=>dout_s);
  process
  begin
    clk_s <= '0', '1' after 10 ns;
    wait for 20 ns;
  end process;

  process
  begin
    rst_s <= '1';
    wait for 50 ns;
    rst_s <= '0';
    wait;
  end process;

  process
  begin
    cfg_valid_s <= '1';
    cfg_s <= x"10000008";
    wait;
  end process;

  stim_process:
  process
    variable tv : line;
  begin
    uut_input_s <= (others=>'0');
    wait until falling_edge(clk_s);
    --ulaz za filtriranje
    while not endfile(input_test_vector) loop
      readline(input_test_vector,tv);
      uut_input_s <= to_std_logic_vector(string(tv));
      wait until falling_edge(clk_s);
    end loop;
    report "verification done!" severity failure;
  end process;

  process
  begin
    dout_ready_s <= '1';
    wait;
  end process;




end;
