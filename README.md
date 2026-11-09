# Calculadora Sumadora en FPGA Nexys 4 DDR (MyHDL)

Diseño e implementación de una calculadora digital con soporte exclusivo para operaciones de suma, desarrollada en Python mediante **MyHDL** y destinada a la tarjeta FPGA **Nexys 4 DDR (Artix-7)**.

## 1. Asignación de Controles (Pulsadores On-Board)
El sistema prescinde de periféricos externos aprovechando los 5 pulsadores integrados en la tarjeta:
* **BTNU (Up):** Incrementa el dígito en edición (`0 → 9`).
* **BTND (Down):** Decrementa el dígito en edición (`9 → 0`).
* **BTNR (Right):** Operación Suma (`+`). Almacena el primer sumando (Operando A) y habilita la captura del segundo.
* **BTNC (Center):** Operación Igual (`=`). Ejecuta la suma aritmética y visualiza el resultado.
* **BTNL (Left):** Reset general (`CLR`). Reinicia los registros y la máquina de estados.

## 2. Estructura del Repositorio
```text
├── constraints/
│   └── Nexys4DDR_Master.xdc    # Mapeo de pines físicos en Nexys 4 DDR
├── sim/
│   └── tb_calculator.py        # Testbench de verificación automatizada
├── src/
│   ├── calculator_fsm.py       # Máquina de estados finitos (FSM) y lógica ALU
│   ├── convert.py              # Script generador de Verilog (top.v)
│   ├── debouncer.py            # Filtro antirrebote para pulsadores mecánicos
│   ├── display_7seg.py         # Decodificador BCD a 7 segmentos
│   ├── display_mux.py          # Controlador multiplexor para los displays
│   └── top.py                  # Módulo jerárquico superior (Top Module)
└── README.md
