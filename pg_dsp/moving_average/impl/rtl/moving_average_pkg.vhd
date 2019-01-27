library ieee;
use ieee.NUMERIC_STD.all;

package moving_average_pkg is


  function log2c (n : integer) return integer;
  function advance_ptr(ptr : integer; limit : integer) return integer;

end package moving_average_pkg;

package body moving_average_pkg is

  function log2c(n : integer) return integer is
    variable m, p: integer;
  begin
    m := 0;
    p := 1;
    while p < n loop
      m := m + 1;
      p := p * 2;
    end loop;
    return m;
  end function log2c;

  function advance_ptr(ptr : integer; limit : integer) return integer is
    variable adv_ptr: integer;
  begin
    if ptr < limit then
      adv_ptr := ptr + 1;
    else
      adv_ptr := 0;
    end if;
    return adv_ptr;
  end function advance_ptr;

end package body moving_average_pkg;
