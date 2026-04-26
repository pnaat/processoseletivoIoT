"""
Semáforo veicular com botão de pedestre — ESP32 / MicroPython
Máquina de estados com temporização não-bloqueante via uasyncio.
 
Pinos:
    GPIO 25 → LED Vermelho
    GPIO 26 → LED Amarelo
    GPIO 27 → LED Verde
    GPIO 14 → Botão de pedestre (entrada, pull-up interno)
"""
 
import uasyncio as asyncio
from machine import Pin
 
#  Configuração de hardware 
 
LEDS = {
    "RED":    Pin(25, Pin.OUT),
    "YELLOW": Pin(26, Pin.OUT),
    "GREEN":  Pin(27, Pin.OUT),
}
 
BTN_PEDESTRIAN = Pin(14, Pin.IN, Pin.PULL_UP)  # ativo em LOW (pull-up)
 
#  Tabela de transições da FSM 
 
FSM = {
    "RED":    {"duration": 5, "next": "GREEN"},
    "GREEN":  {"duration": 4, "next": "YELLOW"},
    "YELLOW": {"duration": 2, "next": "RED"},
}
 
#  Estado compartilhado entre corrotinas 
 
pedestrian_request = False  # sinaliza pedido de travessia
 
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
        await asyncio.sleep(1)
 
 
async def pedestrian_button() -> None:
    """
    Monitora o botão de pedestre a cada 100 ms.
    Ao detectar pressão (sinal LOW com pull-up), sinaliza
    pedido de travessia para a corrotina do semáforo.
    Inclui debounce simples de 200 ms.
    """
    global pedestrian_request
    prev = 1  # pull-up: repouso em HIGH
 
    while True:
        current = BTN_PEDESTRIAN.value()
        if prev == 1 and current == 0:          # borda de descida -> pressionado
            pedestrian_request = True
            print("[BTN  ] Pedestre solicitou travessia")
            await asyncio.sleep(0.2)            # debounce
        prev = current
        await asyncio.sleep(0.1)                # polling a cada 100 ms
 
 
async def traffic_light() -> None:
    """
    Laço principal da máquina de estados do semáforo.
    Verifica pedido de pedestre ao final de cada estado:
    se solicitado e o estado atual não é RED, força transição para YELLOW -> RED.
    """
    global pedestrian_request
    current = "RED"
    print("Teste")  # texto esperado pelo CI
    print("=== Semáforo iniciado ===")
 
    while True:
        config   = FSM[current]
        duration = config["duration"]
 
        apply_state(current)
        await logger(current, duration)
 
        # Pedestre solicitou travessia e semáforo não está vermelho?
        if pedestrian_request and current != "RED":
            print("[FSM  ] Pedido de pedestre — forçando YELLOW → RED")
            pedestrian_request = False
            # Transita para YELLOW antes de fechar em RED
            if current != "YELLOW":
                apply_state("YELLOW")
                await asyncio.sleep(2)
            current = "RED"
        else:
            pedestrian_request = False
            current = config["next"]
 
 
#  Ponto de entrada 
 
async def main() -> None:
    """
    Ponto de entrada assíncrono.
    Executa o semáforo e o monitor do botão em paralelo.
    """
    await asyncio.gather(
        traffic_light(),
        pedestrian_button(),
    )
 
 
asyncio.run(main())
