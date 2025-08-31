module Cache_top();

/*verilator public_flat_rw_on*/
  logic  clock;
  logic  reset;
  logic  io_in_req_ready;
  logic  io_in_req_valid;
  logic [31:0] io_in_req_bits_addr;
  logic [2:0] io_in_req_bits_size;
  logic [3:0] io_in_req_bits_cmd;
  logic [7:0] io_in_req_bits_wmask;
  logic [63:0] io_in_req_bits_wdata;
  logic [15:0] io_in_req_bits_user;
  logic  io_in_resp_ready;
  logic  io_in_resp_valid;
  logic [3:0] io_in_resp_bits_cmd;
  logic [63:0] io_in_resp_bits_rdata;
  logic [15:0] io_in_resp_bits_user;
  logic [1:0] io_flush;
  logic  io_out_mem_req_ready;
  logic  io_out_mem_req_valid;
  logic [31:0] io_out_mem_req_bits_addr;
  logic [2:0] io_out_mem_req_bits_size;
  logic [3:0] io_out_mem_req_bits_cmd;
  logic [7:0] io_out_mem_req_bits_wmask;
  logic [63:0] io_out_mem_req_bits_wdata;
  logic  io_out_mem_resp_ready;
  logic  io_out_mem_resp_valid;
  logic [3:0] io_out_mem_resp_bits_cmd;
  logic [63:0] io_out_mem_resp_bits_rdata;
  logic  io_out_coh_req_ready;
  logic  io_out_coh_req_valid;
  logic [31:0] io_out_coh_req_bits_addr;
  logic [2:0] io_out_coh_req_bits_size;
  logic [3:0] io_out_coh_req_bits_cmd;
  logic [7:0] io_out_coh_req_bits_wmask;
  logic [63:0] io_out_coh_req_bits_wdata;
  logic  io_out_coh_resp_ready;
  logic  io_out_coh_resp_valid;
  logic [3:0] io_out_coh_resp_bits_cmd;
  logic [63:0] io_out_coh_resp_bits_rdata;
  logic  io_mmio_req_ready;
  logic  io_mmio_req_valid;
  logic [31:0] io_mmio_req_bits_addr;
  logic [2:0] io_mmio_req_bits_size;
  logic [3:0] io_mmio_req_bits_cmd;
  logic [7:0] io_mmio_req_bits_wmask;
  logic [63:0] io_mmio_req_bits_wdata;
  logic  io_mmio_resp_ready;
  logic  io_mmio_resp_valid;
  logic [3:0] io_mmio_resp_bits_cmd;
  logic [63:0] io_mmio_resp_bits_rdata;
  logic  io_empty;
/*verilator public_off*/


 Cache Cache(
    .clock(clock),
    .reset(reset),
    .io_in_req_ready(io_in_req_ready),
    .io_in_req_valid(io_in_req_valid),
    .io_in_req_bits_addr(io_in_req_bits_addr),
    .io_in_req_bits_size(io_in_req_bits_size),
    .io_in_req_bits_cmd(io_in_req_bits_cmd),
    .io_in_req_bits_wmask(io_in_req_bits_wmask),
    .io_in_req_bits_wdata(io_in_req_bits_wdata),
    .io_in_req_bits_user(io_in_req_bits_user),
    .io_in_resp_ready(io_in_resp_ready),
    .io_in_resp_valid(io_in_resp_valid),
    .io_in_resp_bits_cmd(io_in_resp_bits_cmd),
    .io_in_resp_bits_rdata(io_in_resp_bits_rdata),
    .io_in_resp_bits_user(io_in_resp_bits_user),
    .io_flush(io_flush),
    .io_out_mem_req_ready(io_out_mem_req_ready),
    .io_out_mem_req_valid(io_out_mem_req_valid),
    .io_out_mem_req_bits_addr(io_out_mem_req_bits_addr),
    .io_out_mem_req_bits_size(io_out_mem_req_bits_size),
    .io_out_mem_req_bits_cmd(io_out_mem_req_bits_cmd),
    .io_out_mem_req_bits_wmask(io_out_mem_req_bits_wmask),
    .io_out_mem_req_bits_wdata(io_out_mem_req_bits_wdata),
    .io_out_mem_resp_ready(io_out_mem_resp_ready),
    .io_out_mem_resp_valid(io_out_mem_resp_valid),
    .io_out_mem_resp_bits_cmd(io_out_mem_resp_bits_cmd),
    .io_out_mem_resp_bits_rdata(io_out_mem_resp_bits_rdata),
    .io_out_coh_req_ready(io_out_coh_req_ready),
    .io_out_coh_req_valid(io_out_coh_req_valid),
    .io_out_coh_req_bits_addr(io_out_coh_req_bits_addr),
    .io_out_coh_req_bits_size(io_out_coh_req_bits_size),
    .io_out_coh_req_bits_cmd(io_out_coh_req_bits_cmd),
    .io_out_coh_req_bits_wmask(io_out_coh_req_bits_wmask),
    .io_out_coh_req_bits_wdata(io_out_coh_req_bits_wdata),
    .io_out_coh_resp_ready(io_out_coh_resp_ready),
    .io_out_coh_resp_valid(io_out_coh_resp_valid),
    .io_out_coh_resp_bits_cmd(io_out_coh_resp_bits_cmd),
    .io_out_coh_resp_bits_rdata(io_out_coh_resp_bits_rdata),
    .io_mmio_req_ready(io_mmio_req_ready),
    .io_mmio_req_valid(io_mmio_req_valid),
    .io_mmio_req_bits_addr(io_mmio_req_bits_addr),
    .io_mmio_req_bits_size(io_mmio_req_bits_size),
    .io_mmio_req_bits_cmd(io_mmio_req_bits_cmd),
    .io_mmio_req_bits_wmask(io_mmio_req_bits_wmask),
    .io_mmio_req_bits_wdata(io_mmio_req_bits_wdata),
    .io_mmio_resp_ready(io_mmio_resp_ready),
    .io_mmio_resp_valid(io_mmio_resp_valid),
    .io_mmio_resp_bits_cmd(io_mmio_resp_bits_cmd),
    .io_mmio_resp_bits_rdata(io_mmio_resp_bits_rdata),
    .io_empty(io_empty)
 );


  export "DPI-C" function get_clockxxPfBDHPmU1N4;
  export "DPI-C" function set_clockxxPfBDHPmU1N4;
  export "DPI-C" function get_resetxxPfBDHPmU1N4;
  export "DPI-C" function set_resetxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_validxxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_req_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_bits_addrxxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_req_bits_addrxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_bits_sizexxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_req_bits_sizexxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_req_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_bits_wmaskxxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_req_bits_wmaskxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_bits_wdataxxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_req_bits_wdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_req_bits_userxxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_req_bits_userxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_resp_readyxxPfBDHPmU1N4;
  export "DPI-C" function set_io_in_resp_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_resp_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_resp_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_resp_bits_rdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_in_resp_bits_userxxPfBDHPmU1N4;
  export "DPI-C" function get_io_flushxxPfBDHPmU1N4;
  export "DPI-C" function set_io_flushxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_req_readyxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_mem_req_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_req_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_req_bits_addrxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_req_bits_sizexxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_req_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_req_bits_wmaskxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_req_bits_wdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_resp_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_resp_validxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_mem_resp_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_resp_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_mem_resp_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_mem_resp_bits_rdataxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_mem_resp_bits_rdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_req_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_req_validxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_coh_req_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_req_bits_addrxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_coh_req_bits_addrxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_req_bits_sizexxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_coh_req_bits_sizexxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_req_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_coh_req_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_req_bits_wmaskxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_coh_req_bits_wmaskxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_req_bits_wdataxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_coh_req_bits_wdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_resp_readyxxPfBDHPmU1N4;
  export "DPI-C" function set_io_out_coh_resp_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_resp_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_resp_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_out_coh_resp_bits_rdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_req_readyxxPfBDHPmU1N4;
  export "DPI-C" function set_io_mmio_req_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_req_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_req_bits_addrxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_req_bits_sizexxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_req_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_req_bits_wmaskxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_req_bits_wdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_resp_readyxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_resp_validxxPfBDHPmU1N4;
  export "DPI-C" function set_io_mmio_resp_validxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_resp_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function set_io_mmio_resp_bits_cmdxxPfBDHPmU1N4;
  export "DPI-C" function get_io_mmio_resp_bits_rdataxxPfBDHPmU1N4;
  export "DPI-C" function set_io_mmio_resp_bits_rdataxxPfBDHPmU1N4;
  export "DPI-C" function get_io_emptyxxPfBDHPmU1N4;


  function void get_clockxxPfBDHPmU1N4;
    output logic  value;
    value=clock;
  endfunction

  function void set_clockxxPfBDHPmU1N4;
    input logic  value;
    clock=value;
  endfunction

  function void get_resetxxPfBDHPmU1N4;
    output logic  value;
    value=reset;
  endfunction

  function void set_resetxxPfBDHPmU1N4;
    input logic  value;
    reset=value;
  endfunction

  function void get_io_in_req_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_in_req_ready;
  endfunction

  function void get_io_in_req_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_in_req_valid;
  endfunction

  function void set_io_in_req_validxxPfBDHPmU1N4;
    input logic  value;
    io_in_req_valid=value;
  endfunction

  function void get_io_in_req_bits_addrxxPfBDHPmU1N4;
    output logic [31:0] value;
    value=io_in_req_bits_addr;
  endfunction

  function void set_io_in_req_bits_addrxxPfBDHPmU1N4;
    input logic [31:0] value;
    io_in_req_bits_addr=value;
  endfunction

  function void get_io_in_req_bits_sizexxPfBDHPmU1N4;
    output logic [2:0] value;
    value=io_in_req_bits_size;
  endfunction

  function void set_io_in_req_bits_sizexxPfBDHPmU1N4;
    input logic [2:0] value;
    io_in_req_bits_size=value;
  endfunction

  function void get_io_in_req_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_in_req_bits_cmd;
  endfunction

  function void set_io_in_req_bits_cmdxxPfBDHPmU1N4;
    input logic [3:0] value;
    io_in_req_bits_cmd=value;
  endfunction

  function void get_io_in_req_bits_wmaskxxPfBDHPmU1N4;
    output logic [7:0] value;
    value=io_in_req_bits_wmask;
  endfunction

  function void set_io_in_req_bits_wmaskxxPfBDHPmU1N4;
    input logic [7:0] value;
    io_in_req_bits_wmask=value;
  endfunction

  function void get_io_in_req_bits_wdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_in_req_bits_wdata;
  endfunction

  function void set_io_in_req_bits_wdataxxPfBDHPmU1N4;
    input logic [63:0] value;
    io_in_req_bits_wdata=value;
  endfunction

  function void get_io_in_req_bits_userxxPfBDHPmU1N4;
    output logic [15:0] value;
    value=io_in_req_bits_user;
  endfunction

  function void set_io_in_req_bits_userxxPfBDHPmU1N4;
    input logic [15:0] value;
    io_in_req_bits_user=value;
  endfunction

  function void get_io_in_resp_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_in_resp_ready;
  endfunction

  function void set_io_in_resp_readyxxPfBDHPmU1N4;
    input logic  value;
    io_in_resp_ready=value;
  endfunction

  function void get_io_in_resp_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_in_resp_valid;
  endfunction

  function void get_io_in_resp_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_in_resp_bits_cmd;
  endfunction

  function void get_io_in_resp_bits_rdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_in_resp_bits_rdata;
  endfunction

  function void get_io_in_resp_bits_userxxPfBDHPmU1N4;
    output logic [15:0] value;
    value=io_in_resp_bits_user;
  endfunction

  function void get_io_flushxxPfBDHPmU1N4;
    output logic [1:0] value;
    value=io_flush;
  endfunction

  function void set_io_flushxxPfBDHPmU1N4;
    input logic [1:0] value;
    io_flush=value;
  endfunction

  function void get_io_out_mem_req_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_mem_req_ready;
  endfunction

  function void set_io_out_mem_req_readyxxPfBDHPmU1N4;
    input logic  value;
    io_out_mem_req_ready=value;
  endfunction

  function void get_io_out_mem_req_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_mem_req_valid;
  endfunction

  function void get_io_out_mem_req_bits_addrxxPfBDHPmU1N4;
    output logic [31:0] value;
    value=io_out_mem_req_bits_addr;
  endfunction

  function void get_io_out_mem_req_bits_sizexxPfBDHPmU1N4;
    output logic [2:0] value;
    value=io_out_mem_req_bits_size;
  endfunction

  function void get_io_out_mem_req_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_out_mem_req_bits_cmd;
  endfunction

  function void get_io_out_mem_req_bits_wmaskxxPfBDHPmU1N4;
    output logic [7:0] value;
    value=io_out_mem_req_bits_wmask;
  endfunction

  function void get_io_out_mem_req_bits_wdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_out_mem_req_bits_wdata;
  endfunction

  function void get_io_out_mem_resp_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_mem_resp_ready;
  endfunction

  function void get_io_out_mem_resp_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_mem_resp_valid;
  endfunction

  function void set_io_out_mem_resp_validxxPfBDHPmU1N4;
    input logic  value;
    io_out_mem_resp_valid=value;
  endfunction

  function void get_io_out_mem_resp_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_out_mem_resp_bits_cmd;
  endfunction

  function void set_io_out_mem_resp_bits_cmdxxPfBDHPmU1N4;
    input logic [3:0] value;
    io_out_mem_resp_bits_cmd=value;
  endfunction

  function void get_io_out_mem_resp_bits_rdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_out_mem_resp_bits_rdata;
  endfunction

  function void set_io_out_mem_resp_bits_rdataxxPfBDHPmU1N4;
    input logic [63:0] value;
    io_out_mem_resp_bits_rdata=value;
  endfunction

  function void get_io_out_coh_req_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_coh_req_ready;
  endfunction

  function void get_io_out_coh_req_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_coh_req_valid;
  endfunction

  function void set_io_out_coh_req_validxxPfBDHPmU1N4;
    input logic  value;
    io_out_coh_req_valid=value;
  endfunction

  function void get_io_out_coh_req_bits_addrxxPfBDHPmU1N4;
    output logic [31:0] value;
    value=io_out_coh_req_bits_addr;
  endfunction

  function void set_io_out_coh_req_bits_addrxxPfBDHPmU1N4;
    input logic [31:0] value;
    io_out_coh_req_bits_addr=value;
  endfunction

  function void get_io_out_coh_req_bits_sizexxPfBDHPmU1N4;
    output logic [2:0] value;
    value=io_out_coh_req_bits_size;
  endfunction

  function void set_io_out_coh_req_bits_sizexxPfBDHPmU1N4;
    input logic [2:0] value;
    io_out_coh_req_bits_size=value;
  endfunction

  function void get_io_out_coh_req_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_out_coh_req_bits_cmd;
  endfunction

  function void set_io_out_coh_req_bits_cmdxxPfBDHPmU1N4;
    input logic [3:0] value;
    io_out_coh_req_bits_cmd=value;
  endfunction

  function void get_io_out_coh_req_bits_wmaskxxPfBDHPmU1N4;
    output logic [7:0] value;
    value=io_out_coh_req_bits_wmask;
  endfunction

  function void set_io_out_coh_req_bits_wmaskxxPfBDHPmU1N4;
    input logic [7:0] value;
    io_out_coh_req_bits_wmask=value;
  endfunction

  function void get_io_out_coh_req_bits_wdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_out_coh_req_bits_wdata;
  endfunction

  function void set_io_out_coh_req_bits_wdataxxPfBDHPmU1N4;
    input logic [63:0] value;
    io_out_coh_req_bits_wdata=value;
  endfunction

  function void get_io_out_coh_resp_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_coh_resp_ready;
  endfunction

  function void set_io_out_coh_resp_readyxxPfBDHPmU1N4;
    input logic  value;
    io_out_coh_resp_ready=value;
  endfunction

  function void get_io_out_coh_resp_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_out_coh_resp_valid;
  endfunction

  function void get_io_out_coh_resp_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_out_coh_resp_bits_cmd;
  endfunction

  function void get_io_out_coh_resp_bits_rdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_out_coh_resp_bits_rdata;
  endfunction

  function void get_io_mmio_req_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_mmio_req_ready;
  endfunction

  function void set_io_mmio_req_readyxxPfBDHPmU1N4;
    input logic  value;
    io_mmio_req_ready=value;
  endfunction

  function void get_io_mmio_req_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_mmio_req_valid;
  endfunction

  function void get_io_mmio_req_bits_addrxxPfBDHPmU1N4;
    output logic [31:0] value;
    value=io_mmio_req_bits_addr;
  endfunction

  function void get_io_mmio_req_bits_sizexxPfBDHPmU1N4;
    output logic [2:0] value;
    value=io_mmio_req_bits_size;
  endfunction

  function void get_io_mmio_req_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_mmio_req_bits_cmd;
  endfunction

  function void get_io_mmio_req_bits_wmaskxxPfBDHPmU1N4;
    output logic [7:0] value;
    value=io_mmio_req_bits_wmask;
  endfunction

  function void get_io_mmio_req_bits_wdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_mmio_req_bits_wdata;
  endfunction

  function void get_io_mmio_resp_readyxxPfBDHPmU1N4;
    output logic  value;
    value=io_mmio_resp_ready;
  endfunction

  function void get_io_mmio_resp_validxxPfBDHPmU1N4;
    output logic  value;
    value=io_mmio_resp_valid;
  endfunction

  function void set_io_mmio_resp_validxxPfBDHPmU1N4;
    input logic  value;
    io_mmio_resp_valid=value;
  endfunction

  function void get_io_mmio_resp_bits_cmdxxPfBDHPmU1N4;
    output logic [3:0] value;
    value=io_mmio_resp_bits_cmd;
  endfunction

  function void set_io_mmio_resp_bits_cmdxxPfBDHPmU1N4;
    input logic [3:0] value;
    io_mmio_resp_bits_cmd=value;
  endfunction

  function void get_io_mmio_resp_bits_rdataxxPfBDHPmU1N4;
    output logic [63:0] value;
    value=io_mmio_resp_bits_rdata;
  endfunction

  function void set_io_mmio_resp_bits_rdataxxPfBDHPmU1N4;
    input logic [63:0] value;
    io_mmio_resp_bits_rdata=value;
  endfunction

  function void get_io_emptyxxPfBDHPmU1N4;
    output logic  value;
    value=io_empty;
  endfunction



  initial begin
    $dumpfile("wavout/Cache.fst");
    $dumpvars(0, Cache_top);
  end

  export "DPI-C" function finish_PfBDHPmU1N4;
  function void finish_PfBDHPmU1N4;
    $finish;
  endfunction


endmodule
