from myhdl import block, always_seq, always_comb, Signal, intbv
from display_7seg import bcd_to_7seg

@block
def display_mux(clk, rst, val_in, an, seg):
    """
    Controlador multiplexor para los displays de 7 segmentos de la Nexys 4 DDR.
    - Toma un número entero (0 a 199).
    - Lo descompone en Centenas, Decenas y Unidades.
    - Alterna rápidamente entre los primeros 3 displays (AN0, AN1, AN2).
    - Los demás displays (AN3 a AN7) se mantienen apagados ('1').
    """
    # Divisor de frecuencia: a 100 MHz, los bits 17:16 cambian a unos 380 Hz
    refresh_counter = Signal(intbv(0)[18:])
    active_display = Signal(intbv(0)[2:])

    # Dígitos individuales
    d_units = Signal(intbv(0, min=0, max=10))
    d_tens = Signal(intbv(0, min=0, max=10))
    d_hundreds = Signal(intbv(0, min=0, max=10))

    # Dígito actual seleccionado para enviar al decodificador
    current_digit = Signal(intbv(0, min=0, max=10))

    # Instanciamos el decodificador de 7 segmentos que creamos ayer
    decoder_inst = bcd_to_7seg(current_digit, seg)

    @always_seq(clk.posedge, reset=rst)
    def counter_proc():
        refresh_counter.next = refresh_counter + 1
        active_display.next = refresh_counter[18:16] # Usamos los 2 bits más significativos

    @always_comb
    def split_digits():
        # Descomposición en unidades, decenas y centenas
        d_hundreds.next = (val_in // 100) % 10
        d_tens.next = (val_in // 10) % 10
        d_units.next = val_in % 10

    @always_comb
    def mux_logic():
        # Por defecto, todos los ánodos apagados (ánodo activo en bajo = 1)
        an.next = intbv("11111111")[8:]
        current_digit.next = 0

        # Multiplexación de los primeros 3 dígitos
        if active_display == 0:
            an.next = intbv("11111110")[8:] # AN0 encendido (Unidades)
            current_digit.next = d_units
        elif active_display == 1:
            an.next = intbv("11111101")[8:] # AN1 encendido (Decenas)
            current_digit.next = d_tens
        elif active_display == 2:
            an.next = intbv("11111011")[8:] # AN2 encendido (Centenas)
            current_digit.next = d_hundreds
        else:
            an.next = intbv("11111111")[8:] # Apagado

    return counter_proc, split_digits, mux_logic, decoder_inst
