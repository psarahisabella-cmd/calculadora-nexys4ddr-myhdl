# Calculadora Sumadora en FPGA Nexys 4 DDR (MyHDL)

Este repositorio contiene el diseño e implementación de una calculadora digital con soporte exclusivo para operaciones de suma, desarrollada en Python mediante **MyHDL** y destinada a la tarjeta FPGA **Nexys 4 DDR (Artix-7)**.

## 1. Asignación de Controles (Pulsadores)
Para prescindir de periféricos externos, el sistema utiliza los 5 pulsadores integrados en la tarjeta:
* **BTNU (Up):** Incrementa el dígito en edición (`0 → 9`).
* **BTND (Down):** Decrementa el dígito en edición (`9 → 0`).
* **BTNR (Right):** Operación Suma (`+`). Almacena el primer sumando (Operando A) y habilita la captura del segundo.
* **BTNC (Center):** Operación Igual (`=`). Ejecuta la adición y visualiza el resultado.
* **BTNL (Left):** Reset (`CLR`). Reinicia la máquina de estados y registros a cero.

## 2. Arquitectura del Sistema
El diseño se divide en tres bloques jerárquicos:
1. `debouncer.py`: Módulo antirrebote para acondicionar las señales mecánicas de los 5 botones.
2. `calculator_fsm.py`: Máquina de estados finitos (FSM) que orquesta la captura de operandos, la suma aritmética y la limpieza de registros.
3. `display_7seg.py`: Decodificador BCD y multiplexor de tiempo para el control de los displays de 7 segmentos (ánodos y cátodos activos en bajo).

## 3. Máquina de Estados (FSM)
* **ESTADO_A:** Selección del primer número con BTNU/BTND.
* **ESTADO_OP:** Se oprime BTNR (`+`), el operando A pasa al registro interno y se prepara el registro B.
* **ESTADO_B:** Selección del segundo número con BTNU/BTND.
* **ESTADO_RES:** Se oprime BTNC (`=`), la ALU suma `A + B` y congela el resultado en el display hasta pulsar BTNL (`Reset`).
