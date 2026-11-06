from myhdl import block, always_comb, Signal, intbv

@block
def bcd_to_7seg(bcd_digit, segments):
    """
    Decodificador BCD a 7 segmentos para Nexys 4 DDR.
    Los cátodos son activos en BAJO ('0' enciende el segmento).
    segments = [CA, CB, CC, CD, CE, CF, CG]
    """
    @always_comb
    def dec_logic():
        if bcd_digit == 0:   segments.next = intbv("0000001")[7:]
        elif bcd_digit == 1: segments.next = intbv("1001111")[7:]
        elif bcd_digit == 2: segments.next = intbv("0010010")[7:]
        elif bcd_digit == 3: segments.next = intbv("0000110")[7:]
        elif bcd_digit == 4: segments.next = intbv("1001100")[7:]
        elif bcd_digit == 5: segments.next = intbv("0100100")[7:]
        elif bcd_digit == 6: segments.next = intbv("0100000")[7:]
        elif bcd_digit == 7: segments.next = intbv("0001111")[7:]
        elif bcd_digit == 8: segments.next = intbv("0000000")[7:]
        elif bcd_digit == 9: segments.next = intbv("0000100")[7:]
        else:                segments.next = intbv("1111111")[7:] # Apagado

    return dec_logic
