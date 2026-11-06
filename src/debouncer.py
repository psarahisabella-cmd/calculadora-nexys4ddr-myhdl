from myhdl import block, always_seq, Signal, intbv

@block
def debouncer(clk, rst, btn_in, btn_pulse, CLK_FREQ_HZ=100000000, DEBOUNCE_TIME_MS=20):
    """
    Filtro antirrebote para pulsadores mecánicos de la Nexys 4 DDR.
    Produce un pulso de 1 solo ciclo de reloj cuando la tecla se estabiliza en nivel alto.
    """
    # Límite del contador para esperar 20 ms (2,000,000 ciclos a 100 MHz)
    COUNT_MAX = int((CLK_FREQ_HZ // 1000) * DEBOUNCE_TIME_MS)
    timer = Signal(intbv(0, min=0, max=COUNT_MAX + 1))
    
    btn_sync_0 = Signal(bool(0))
    btn_sync_1 = Signal(bool(0))
    btn_state = Signal(bool(0))

    @always_seq(clk.posedge, reset=rst)
    def logic():
        # Sincronizador de 2 etapas para evitar metaestabilidad
        btn_sync_0.next = btn_in
        btn_sync_1.next = btn_sync_0
        btn_pulse.next = 0

        # Si el botón cambia respecto al estado validado, reinicia temporizador
        if btn_sync_1 != btn_state:
            timer.next = timer + 1
            if timer >= COUNT_MAX:
                btn_state.next = btn_sync_1
                timer.next = 0
                if btn_sync_1 == 1:
                    btn_pulse.next = 1  # Dispara un único pulso de activación
        else:
            timer.next = 0

    return logic
