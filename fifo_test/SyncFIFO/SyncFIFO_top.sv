module SyncFIFO_top();

/*verilator public_flat_rw_on*/
  logic  clk;
  logic  rst_n;
  logic  we_i;
  logic  re_i;
  logic [31:0] data_i;
  logic [31:0] data_o;
  logic  full_o;
  logic  empty_o;
/*verilator public_off*/


 SyncFIFO SyncFIFO(
    .clk(clk),
    .rst_n(rst_n),
    .we_i(we_i),
    .re_i(re_i),
    .data_i(data_i),
    .data_o(data_o),
    .full_o(full_o),
    .empty_o(empty_o)
 );


  export "DPI-C" function get_clkxxHjREhgDlWaW;
  export "DPI-C" function set_clkxxHjREhgDlWaW;
  export "DPI-C" function get_rst_nxxHjREhgDlWaW;
  export "DPI-C" function set_rst_nxxHjREhgDlWaW;
  export "DPI-C" function get_we_ixxHjREhgDlWaW;
  export "DPI-C" function set_we_ixxHjREhgDlWaW;
  export "DPI-C" function get_re_ixxHjREhgDlWaW;
  export "DPI-C" function set_re_ixxHjREhgDlWaW;
  export "DPI-C" function get_data_ixxHjREhgDlWaW;
  export "DPI-C" function set_data_ixxHjREhgDlWaW;
  export "DPI-C" function get_data_oxxHjREhgDlWaW;
  export "DPI-C" function get_full_oxxHjREhgDlWaW;
  export "DPI-C" function get_empty_oxxHjREhgDlWaW;
  export "DPI-C" function get_SyncFIFO_wptrxxHjREhgDlWaW;
  export "DPI-C" function get_SyncFIFO_counterxxHjREhgDlWaW;
  export "DPI-C" function get_SyncFIFO_rptrxxHjREhgDlWaW;


  function void get_clkxxHjREhgDlWaW;
    output logic  value;
    value=clk;
  endfunction

  function void set_clkxxHjREhgDlWaW;
    input logic  value;
    clk=value;
  endfunction

  function void get_rst_nxxHjREhgDlWaW;
    output logic  value;
    value=rst_n;
  endfunction

  function void set_rst_nxxHjREhgDlWaW;
    input logic  value;
    rst_n=value;
  endfunction

  function void get_we_ixxHjREhgDlWaW;
    output logic  value;
    value=we_i;
  endfunction

  function void set_we_ixxHjREhgDlWaW;
    input logic  value;
    we_i=value;
  endfunction

  function void get_re_ixxHjREhgDlWaW;
    output logic  value;
    value=re_i;
  endfunction

  function void set_re_ixxHjREhgDlWaW;
    input logic  value;
    re_i=value;
  endfunction

  function void get_data_ixxHjREhgDlWaW;
    output logic [31:0] value;
    value=data_i;
  endfunction

  function void set_data_ixxHjREhgDlWaW;
    input logic [31:0] value;
    data_i=value;
  endfunction

  function void get_data_oxxHjREhgDlWaW;
    output logic [31:0] value;
    value=data_o;
  endfunction

  function void get_full_oxxHjREhgDlWaW;
    output logic  value;
    value=full_o;
  endfunction

  function void get_empty_oxxHjREhgDlWaW;
    output logic  value;
    value=empty_o;
  endfunction

  function void get_SyncFIFO_wptrxxHjREhgDlWaW;
    output logic [3:0] value;
    value=SyncFIFO.wptr;
  endfunction

  function void get_SyncFIFO_counterxxHjREhgDlWaW;
    output logic [4:0] value;
    value=SyncFIFO.counter;
  endfunction

  function void get_SyncFIFO_rptrxxHjREhgDlWaW;
    output logic [3:0] value;
    value=SyncFIFO.rptr;
  endfunction



  initial begin
    $dumpfile("out/SyncFIFO.fst");
    $dumpvars(0, SyncFIFO_top);
  end

  export "DPI-C" function finish_HjREhgDlWaW;
  function void finish_HjREhgDlWaW;
    $finish;
  endfunction


endmodule
