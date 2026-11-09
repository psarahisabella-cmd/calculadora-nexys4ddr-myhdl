# Calculadora Sumadora en FPGA Nexys 4 DDR (MyHDL)

Diseño e implementación de una calculadora digital con soporte exclusivo para operaciones de suma, desarrollada en Python mediante **MyHDL** y destinada a la tarjeta FPGA **Nexys 4 DDR (Artix-7)**.

## 1. Asignación de Controles (Pulsadores On-Board)
El sistema prescinde de periféricos externos aprovechando los 5 pulsadores integrados en la tarjeta:
* **BTNU (Up):** Incrementa el dígito en edición (`0 → 9`).
* **BTND (Down):** Decrementa el dígito en edición (`9 → 0`).
* **BTNR (Right):** Operación Suma (`+`). Almacena el primer sumando (Operando A) y habilita la captura del segundo.
* **BTNC (Center):** Operación Igual (`=`). Ejecuta la suma aritmética y visualiza el resultado.
* **BTNL (Left):** Reset (`CLR`). Reinicia los registros y la máquina de estados.

## 2. Estructura Jerárquica del Código (`/src`)
* `debouncer.py`: Filtro antirrebote y sincronizador de 2 etapas para los pulsadores mecánicos (evita lecturas espurias y metaestabilidad).
* `calculator_fsm.py`: Máquina de estados finitos (FSM) que orquesta la captura de operandos, la suma aritmética y la limpieza de datos.
* `display_7seg.py`: Decodificador BCD a 7 segmentos (cátodos activos en bajo).
* `display_mux.py`: Controlador multiplexor para los displays de la tarjeta. Realiza la descomposición decimal (centenas, decenas, unidades) y refresca secuencialmente a una tasa imperceptible al ojo humano (~380 Hz).
* `top.py`: Módulo jerárquico superior (Top Module) que interconecta entradas de reloj, botones, FSM, lógica de multiplexación y salidas a la FPGA.
* `convert.py`: Script para sintetizar el diseño de Python MyHDL a código Verilog estándar (`top.v`).

## 3. Máquina de Estados (FSM)
* **ESTADO_A:** Selección del primer número con BTNU/BTND.
* **ESTADO_B:** Al oprimir BTNR (`+`), el operando A se almacena y se pasa a ingresar el operando B.
* **ESTADO_RES:** Al oprimir BTNC (`=`), la unidad de cálculo realiza `A + B` y congela el resultado en los displays hasta pulsar BTNL (`Reset`).

## 4. Flujo de Implementación
1. Modelado y lógica en **Python / MyHDL**.
2. Conversión a **Verilog** mediante `python src/convert.py`.
3. Síntesis, mapeo de pines (`.xdc`) y generación de Bitstream en **Xilinx Vivado**.
