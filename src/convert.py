from myhdl import Signal, ResetSignal, intbv
from top import top

def generate_verilog():
    """Genera el código Verilog equivalente a partir del diseño en MyHDL."""
    clk = Signal(bool(0))
    btn_u = Signal(bool(0))
    btn_d = Signal(bool(0))
    btn_r = Signal(bool(0))
    btn_c = Signal(bool(0))
    btn_l = Signal(bool(0))
    an = Signal(intbv(0)[8:])
    seg = Signal(intbv(0)[7:])

    top_inst = top(clk, btn_u, btn_d, btn_r, btn_c, btn_l, an, seg)
    top_inst.convert(hdl='Verilog')
    print("¡Conversión exitosa! Archivo Verilog generado: top.v")

if __name__ == '__main__':
    generate_verilog()
