from myhdl import block, Signal, ResetSignal, intbv
from debouncer import debouncer
from calculator_fsm import calculator_fsm
from display_mux import display_mux

@block
def top(clk, btn_u, btn_d, btn_r, btn_c, btn_l, an, seg):
    """
    Módulo TOP de la Calculadora Sumadora para Nexys 4 DDR.
    
    Puertos de Entrada (Placa física):
    - clk: Oscilador de 100 MHz (Pin E3)
    - btn_u: Pulsador Arriba (Incrementar)
    - btn_d: Pulsador Abajo (Decrementar)
    - btn_r: Pulsador Derecha (Operación '+')
    - btn_c: Pulsador Centro (Operación '=')
    - btn_l: Pulsador Izquierda (Reset / Borrar)
    
    Puertos de Salida (Displays de 7 segmentos):
    - an: [7:0] Control de Ánodos (activos en bajo)
    - seg: [6:0] Cátodos CA..CG (activos en bajo)
    """
    # El botón izquierdo (btn_l) actúa como señal de Reset general
    rst = ResetSignal(0, active=1, isasync=True)

    # Señales de pulso limpio tras pasar por el antirrebote
    pulse_up = Signal(bool(0))
    pulse_down = Signal(bool(0))
    pulse_add = Signal(bool(0))
    pulse_eq = Signal(bool(0))
    pulse_rst = Signal(bool(0))

    # Valor numérico que se mostrará en pantalla
    display_value = Signal(intbv(0, min=0, max=200))

    # Asignamos el botón izquierdo al reset del sistema
    @block
    def reset_assign():
        from myhdl import always_comb
        @always_comb
        def logic():
            rst.next = btn_l
        return logic

    rst_block = reset_assign()

    # Instanciamos los antirrebotes para los 4 pulsadores de control
    deb_u = debouncer(clk, rst, btn_u, pulse_up)
    deb_d = debouncer(clk, rst, btn_d, pulse_down)
    deb_r = debouncer(clk, rst, btn_r, pulse_add)
    deb_c = debouncer(clk, rst, btn_c, pulse_eq)

    # Instanciamos el cerebro (FSM de la calculadora)
    fsm_inst = calculator_fsm(
        clk=clk,
        rst=rst,
        btn_up=pulse_up,
        btn_down=pulse_down,
        btn_add=pulse_add,
        btn_eq=pulse_eq,
        display_val=display_value
    )

    # Instanciamos el controlador de los displays
    mux_inst = display_mux(
        clk=clk,
        rst=rst,
        val_in=display_value,
        an=an,
        seg=seg
    )

    return rst_block, deb_u, deb_d, deb_r, deb_c, fsm_inst, mux_inst
