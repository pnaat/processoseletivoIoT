"""
Semáforo com máquina de estados — MicroPython / ESP32
Pinos: LED vermelho = 25, LED amarelo = 26, LED verde = 27
"""
 
"""
Semáforo veicular — ESP32 / MicroPython
Máquina de estados com temporização não-bloqueante via uasyncio.
 
Pinos:
    GPIO 25 → LED Vermelho
    GPIO 26 → LED Amarelo
    GPIO 27 → LED Verde
"""
 
import uasyncio as asyncio
from machine import Pin
 
#  Configuração de hardware 
 
LEDS = {
    "RED":    Pin(25, Pin.OUT),
    "YELLOW": Pin(26, Pin.OUT),
    "GREEN":  Pin(27, Pin.OUT),
}
 
#  Tabela de transições da FSM 
# Cada estado define duração (s) e o próximo estado.
 
FSM = {
    "RED":    {"duration": 5, "next": "GREEN"},
    "GREEN":  {"duration": 4, "next": "YELLOW"},
    "YELLOW": {"duration": 2, "next": "RED"},
}
 
#  Funções de controle dos LEDs 
 
def all_off() -> None:
    """Desliga todos os LEDs."""
    for led in LEDS.values():
        led.off()
 
 
def apply_state(state: str) -> None:
    """Acende apenas o LED correspondente ao estado atual."""
    all_off()
    LEDS[state].on()
 
 
#  Tarefas assíncronas 
 
async def logger(state: str, duration: int) -> None:
    """
    Imprime o progresso do estado atual no monitor serial,
    atualizando a cada segundo sem bloquear o event loop.
    """
    for elapsed in range(1, duration + 1):
        print(f"[{state:6s}] {elapsed:2d}s / {duration}s")
        await asyncio.sleep(1)          # cede controle ao event loop
 
 
async def traffic_light() -> None:
    """Laço principal da máquina de estados do semáforo."""
    current = "RED"
    print("=== Semáforo iniciado ===")
 
    while True:
        config   = FSM[current]
        duration = config["duration"]
 
        apply_state(current)
        await logger(current, duration)  # não-bloqueante
 
        current = config["next"]
 
 
#  Ponto de entrada 
 
async def main() -> None:
    """
    Ponto de entrada assíncrono.
    Estruturado como corrotina para permitir expansão futura
    (ex.: task de leitura de botão de pedestre em paralelo).
    """
    await asyncio.gather(
        traffic_light(),
        # outras tarefas podem ser adicionadas aqui
    )
 
 
asyncio.run(main())

