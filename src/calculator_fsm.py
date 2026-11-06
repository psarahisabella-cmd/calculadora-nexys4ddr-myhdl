from myhdl import block, always_seq, Signal, intbv, enum

States = enum('INPUT_A', 'INPUT_B', 'RESULT')

@block
def calculator_fsm(clk, rst, btn_up, btn_down, btn_add, btn_eq, display_val):
    """
    Máquina de estados principal de la calculadora sumadora:
    - INPUT_A: Ingreso del primer número con BTNU/BTND.
    - Presionar btn_add (BTNR) pasa a INPUT_B.
    - INPUT_B: Ingreso del segundo número con BTNU/BTND.
    - Presionar btn_eq (BTNC) pasa a RESULT (suma ambos).
    - Presionar rst (BTNL) borra todo y regresa a INPUT_A.
    """
    state = Signal(States.INPUT_A)
    operand_a = Signal(intbv(0, min=0, max=100))
    operand_b = Signal(intbv(0, min=0, max=100))
    result = Signal(intbv(0, min=0, max=200))

    @always_seq(clk.posedge, reset=rst)
    def fsm_logic():
        if state == States.INPUT_A:
            display_val.next = operand_a
            if btn_up:
                operand_a.next = 0 if operand_a == 9 else operand_a + 1
            elif btn_down:
                operand_a.next = 9 if operand_a == 0 else operand_a - 1
            elif btn_add:
                state.next = States.INPUT_B

        elif state == States.INPUT_B:
            display_val.next = operand_b
            if btn_up:
                operand_b.next = 0 if operand_b == 9 else operand_b + 1
            elif btn_down:
                operand_b.next = 9 if operand_b == 0 else operand_b - 1
            elif btn_eq:
                result.next = operand_a + operand_b
                state.next = States.RESULT

        elif state == States.RESULT:
            display_val.next = result
            # Espera a que el usuario presione reset (rst) para volver a empezar

    return fsm_logic
