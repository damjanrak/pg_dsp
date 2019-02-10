library ieee;
use ieee.std_logic_1164.all;
use ieee.NUMERIC_STD.all;
use ieee.math_real.all;
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
        din: in std_logic_vector(W downto 0);
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
  signal din_s: std_logic_vector(W downto 0);
  signal dout_valid_s: std_logic;
  signal dout_ready_s: std_logic;
  signal dout_s: signed(W downto 0);
  constant clk_p : time := 10 ns;
  file input_test_vector : text open read_mode is "/tools/home/pg_dsp/pg_dsp/moving_average/comparison/rtl_verif/input_samples.txt";
  file ref_model : text open read_mode is "/tools/home/pg_dsp/pg_dsp/moving_average/comparison/rtl_verif/ref_model.txt";
  file result_vector : text open write_mode is "/tools/home/pg_dsp/pg_dsp/moving_average/comparison/rtl_verif/output_samples.txt";

  function to_std_logic(c: character) return std_logic is
    variable sl: std_logic;
  begin
    case c is
      when 'U' =>
        sl := 'U';
      when 'X' =>
        sl := 'X';
      when '0' =>
        sl := '0';
      when '1' =>
        sl := '1';
      when 'Z' =>
        sl := 'Z';
      when 'W' =>
        sl := 'W';
      when 'L' =>
        sl := 'L';
      when 'H' =>
        sl := 'H';
      when '-' =>
        sl := '-';
      when others =>
        sl := 'X';
    end case;
    return sl;
  end to_std_logic;

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

  function to_string ( a: std_logic_vector) return string is
    variable b : string (1 to a'length) := (others => NUL);
    variable stri : integer := 1;
  begin
    for i in a'range loop
      b(stri) := std_logic'image(a((i)))(2);
      stri := stri+1;
    end loop;
    return b;
  end function;

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
    clk_s <= '0', '1' after clk_p;
    wait for 2*clk_p;
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
    wait;
  end process;

  stim_process:
  process
    variable tv : line;
    variable seed1, seed2: positive;
    variable rand: real;
    variable delay: integer;
  begin
    cfg_valid_s <= '1';
    cfg_s <= x"19990005";
    wait until rst_s = '1';
    wait until rst_s = '0';
    din_s <= (others=>'0');
    wait until falling_edge(clk_s);
    while not endfile(input_test_vector) loop
      din_valid_s <= '0';
      uniform(seed1, seed2, rand);   -- generate a random number
      delay := integer(rand * 10.0);
      for i in 0 to delay loop
        wait until falling_edge(clk_s);
      end loop;
      readline(input_test_vector,tv);
      din_s <= to_std_logic_vector(string(tv));
      din_valid_s <= '1';
      wait until (rising_edge(clk_s) and din_ready_s = '1');
      wait until falling_edge(clk_s);
    end loop;
    din_valid_s <= '0';
    cfg_valid_s <= '0';
    for i in 0 to 200 loop
      wait until falling_edge(clk_s);
    end loop;
    report "verification done!" severity failure;
  end process;

  process
    variable seed1, seed2: positive;
    variable rand: real;
    variable delay: integer;
  begin
    while (True) loop
      uniform(seed1, seed2, rand);   -- generate a random number
      delay := integer(rand * 10.0);
      uniform(seed1, seed2, rand);   -- generate a random number
      for i in 0 to delay loop
        wait until falling_edge(clk_s);
        if rand > 0.5 then
          dout_ready_s <= '1';
        else
          dout_ready_s <= '0';
        end if;
      end loop;
    end loop;
  end process;

  process(clk_s)
    variable tv : line;
    variable ref : line;
    variable tmp : string(1 to 17);
    variable ref_vector : std_logic_vector(W downto 0);
  begin
    if rising_edge(clk_s) then
      if (dout_valid_s and dout_ready_s) = '1' then
        tmp := to_string(std_logic_vector(dout_s));
        readline(ref_model, ref);
        ref_vector := to_std_logic_vector(string(ref));
        if ref_vector /= std_logic_vector(dout_s) then
          report "output failure" severity failure;
        end if;
        write(tv, tmp);
        writeline(result_vector, tv);
      end if;
    end if;
  end process;



end;
