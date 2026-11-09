import sys
import os

# Permitir que el testbench encuentre los módulos de la carpeta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from myhdl import block, Signal, ResetSignal, intbv, delay, instance, StopSimulation
from calculator_fsm import calculator_fsm

@block
def tb_calculator():
    """
    Banco de pruebas (Testbench) para verificar el funcionamiento
    lógico de la FSM de la Calculadora Sumadora.
    """
    clk = Signal(bool(0))
    rst = ResetSignal(0, active=1, isasync=True)
    btn_up = Signal(bool(0))
    btn_down = Signal(bool(0))
    btn_add = Signal(bool(0))
    btn_eq = Signal(bool(0))
    display_val = Signal(intbv(0, min=0, max=200))

    # Instanciamos la unidad bajo prueba (UUT: Unit Under Test)
    uut = calculator_fsm(clk, rst, btn_up, btn_down, btn_add, btn_eq, display_val)

    # Generador de señal de reloj (Período = 10 unidades de tiempo)
    @instance
    def clk_process():
        while True:
            clk.next = not clk
            yield delay(5)

    # Función auxiliar para simular el pulso de un botón sincronizado con reloj
    def press_button(button_sig):
        button_sig.next = 1
        yield delay(10)
        button_sig.next = 0
        yield delay(10)

    # Proceso de estímulos (Escenario de prueba)
    @instance
    def test_sequence():
        print("\n==========================================")
        print("  INICIANDO SIMULACIÓN DE LA CALCULADORA  ")
        print("==========================================")

        # 1. Aplicar Reset inicial
        rst.next = 1
        yield delay(20)
        rst.next = 0
        yield delay(20)
        print(f"[PASO 1] Reset aplicado -> Display: {int(display_val)}")
        assert display_val == 0, "Error: El display debió iniciar en 0"

        # 2. Configurar Operando A = 3 (Pulsar UP 3 veces)
        print("\n[PASO 2] Ingresando Operando A...")
        for _ in range(3):
            yield from press_button(btn_up)
        print(f" -> Operando A fijado en: {int(display_val)}")
        assert display_val == 3, f"Error: Se esperaba 3, se obtuvo {int(display_val)}"

        # 3. Presionar tecla de Suma '+' (BTNR)
        print("\n[PASO 3] Presionando '+' (btn_add)...")
        yield from press_button(btn_add)

        # 4. Configurar Operando B = 5 (Pulsar UP 5 veces)
        print("\n[PASO 4] Ingresando Operando B...")
        for _ in range(5):
            yield from press_button(btn_up)
        print(f" -> Operando B fijado en: {int(display_val)}")
        assert display_val == 5, f"Error: Se esperaba 5, se obtuvo {int(display_val)}"

        # 5. Presionar tecla de Igual '=' (BTNC)
        print("\n[PASO 5] Presionando '=' (btn_eq) para calcular resultado...")
        yield from press_button(btn_eq)
        print(f" -> RESULTADO EN PANTALLA: {int(display_val)}")
        assert display_val == 8, f"Error: Se esperaba 8 (3 + 5), se obtuvo {int(display_val)}"

        # 6. Probar botón de Borrado / Reset (BTNL)
        print("\n[PASO 6] Presionando Reset (btn_rst)...")
        rst.next = 1
        yield delay(15)
        rst.next = 0
        yield delay(15)
        print(f" -> Display tras Reset: {int(display_val)}")
        assert display_val == 0, "Error: No se borró el resultado tras el reset"

        print("\n==========================================")
        print(" ¡TODAS LAS PRUEBAS PASARON CON ÉXITO! ✔ ")
        print("==========================================\n")
        raise StopSimulation

    return uut, clk_process, test_sequence

if __name__ == "__main__":
    tb = tb_calculator()
    tb.sim(1000)
