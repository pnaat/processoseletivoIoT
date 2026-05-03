"""
Central de Alarme — ESP32 + OLED SSD1306
Simulação: Wokwi
"""

from machine import Pin, I2C
import time
import ssd1306      # Display utilizado na simulação

print("Teste")      # Exigido pelos parâmetros do projeto

# ____________________________________________________     HARDWARE    ____________________________________________________

# ---------- OLED (I2C) ----------
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---------- BOTÕES ----------
botao_arm = Pin(26, Pin.IN, Pin.PULL_UP)
botao_mem = Pin(25, Pin.IN, Pin.PULL_UP)

# ---------- LEDS ----------
led_status = Pin(2, Pin.OUT)
led_mem = Pin(4, Pin.OUT)

# ---------- BUZZER ----------
buzzer = Pin(23, Pin.OUT)

# ---------- SENSORES ----------
z1 = Pin(32, Pin.IN, Pin.PULL_UP)       # Botão Pânico Audível
z2 = Pin(33, Pin.IN, Pin.PULL_UP)       # Botão Pânico Silencioso
z3 = Pin(27, Pin.IN)                    # PIR Temporizado
z4 = Pin(14, Pin.IN)                    # PIR Imediato
z5 = Pin(12, Pin.IN)                    # Gás/Fumaça Imediato

# ___________________________________________    CONFIG DA CENTRAL DE ALARME    ___________________________________________

# ---------- ESTADOS DE OPERAÇÃO ----------
DESARMADO = 0
ARMADO = 1
DISPARO = 2

# ---------- INICIALIZAÇÃO DA SIMULAÇÃO ----------
estado = DESARMADO            # A simulação começa com o sistema desarmado
modo_mem = False              # A simulação começa fora do histórico de disparos

mem = []                      # Lista que contém o histórico de disparos

last_arm = 1
last_mem = 1
last_z1 = 1
last_z2 = 1
last_z5 = 0                       

# ---------- TIMERS DE TOGGLE ----------
t_led = 0
t_buzzer = 0
t_display = 0
t_mem_led = 0

# ---------- ESPECIFICAÇÕES DA ZONA TEMPORIZADA ----------
z3_timer = None
z3_ativo = False
temporizacao = 5000           # Variável que guarda o tempo entre a ativação do sensor e a geração de um disparo
last_z3 = 0

# ---------- DISPLAY ----------
display_index = 0

# ---------- BEEPS ----------
_beep_r = 0
_beep_t = 0

# __________________________________________________    PRINCIPAIS FUNÇÕES    __________________________________________________ 

# ---------- HISTÓRICO DE DISPARO ----------
def add_mem(z):
    """
    Adiciona o endereço de uma zona disparada à lista de histórico de disparos uma única vez e na ordem dos eventos.

    Parâmetros:
        Verifica se a zona já não está no histórico em qualquer posição.

    Retorna:
        mem.append(z)
    """
    if z not in mem: 
        mem.append(z)

# ---------- LEITURA DO ESTADO DO PINO ----------
def edge(pin, last):
    """
    Usada par definir que ação do hardware define um disparo.

    Parâmetros:
        Recebe o endereço da zona e o estado do pino.

    Retorna:
        Parâmetro para considerar disparo na zona.
    """
    val = pin.value()
    trig = (last == 1 and val == 0)
    return val, trig

# ---------- OPERAÇÕES DE BIPES QUE NÃO BLOQUEIEM A LEITURA DOS SENSORES ----------
def beep_start(qtd):
    """
    Inicia uma sequência de bipes.

    Parâmetros:
        Quantidades de bipes para led_status e buzzer (1 = arme, 2 = desarme).
    """
    global _beep_r, _beep_t
    _beep_r = qtd * 2 - 1             # Começa ímpar, cada bipe = 1 fase ON + 1 fase OFF
    _beep_t = time.ticks_ms()
    buzzer.on()
    led_status.on()

def beep_tick(now):
    """
    Avança a sequência de bipes.

    Parâmetros:
        (int): Valor atual de time.ticks_ms().
    """
    global _beep_r, _beep_t
    if _beep_r <= 0:
        return
    if time.ticks_diff(now, _beep_t) >= 300:
        _beep_t = now
        _beep_r -= 1
        ligado = (_beep_r % 2 == 1)     # ímpar = fase ON, par = fase OFF
        buzzer.value(ligado)
        led_status.value(ligado)

def beep_ativo():
    """
    Retorna True enquanto uma sequência de bipes estiver em andamento.
    """
    return _beep_r > 0

# ---------- TEMPLATE OLED ----------
def draw(text1="", text2=""):
    """
    Template de exibição do OLED.
    """
    oled.fill(0)                    
    oled.text(text1, 0, 0)          # Texto na primeira linha
    oled.text(text2, 0, 20)         # Texto na segunda linha
    oled.show()                     

# ________________________________________________    LOOP PRINCIPAL    ________________________________________________

while True:
    now = time.ticks_ms()
    beep_tick(now)

    # ---------- BOTÃO ARME/DESARME ----------
    last_arm, trig_arm = edge(botao_arm, last_arm)      
    if trig_arm:
        modo_mem = False                           # Sai do histórico de disparos antes de armar/desarmar
        if estado == DESARMADO:
            estado = ARMADO
            mem.clear()                            # Limpa o histórico de disparo
            beep_start(1)                          # Bipa uma vez indicando ARME
        else:
            estado = DESARMADO
            beep_start(2)                          # Bipa duas vezes indicando DESARME
    
    # ---------- BOTÃO MEM ----------
    last_mem, trig_mem = edge(botao_mem, last_mem)
    if trig_mem and estado == DESARMADO:           # Só pode acessar o histórico de disparo com a Central desarmada
        modo_mem = not modo_mem

    # ---------- ZONA 1 (BOTÃO - PÂNICO AUDÍVEL / IMEDIATA) ----------
    last_z1, trig_z1 = edge(z1, last_z1)
    if trig_z1:             # Opera mesmo no modo DESARMADO, zona 24 HORAS
        add_mem("Z1")
        estado = DISPARO    # gera disparo

    # ---------- ZONA 2 (BOTÃO - PÂNICO SILENCIOSO / IMEDIATA) ----------
    last_z2, trig_z2 = edge(z2, last_z2)
    if trig_z2:             # Opera mesmo no modo DESARMADO, zona 24 HORAS
        add_mem("Z2")
                            # Não muda o estado para DISPARO, apenas adiciona o endereço à memória

    # ---------- ZONA 3 (PIR - AUDÍVEL / TEMPORIZADA) ----------
    z3_val = z3.value()

    # Detecta edge
    if estado != DESARMADO and last_z3 == 0 and z3_val == 1:
        z3_timer = now
        z3_ativo = True

    # Controle do timer
    if z3_ativo:
        if estado == DESARMADO:
            z3_ativo = False
        elif time.ticks_diff(now, z3_timer) > temporizacao:
            add_mem("Z3")
            estado = DISPARO    # gera disparo
            z3_ativo = False
    last_z3 = z3_val

    # ---------- ZONA 4 (PIR - AUDÍVEL / IMEDIATA) ----------
    if estado != DESARMADO and z4.value():
        add_mem("Z4")
        estado = DISPARO        # gera disparo

    # ---------- ZONA 5 (GÁS - EDGE + NÍVEL) ----------
    z5_val = z5.value()

    # Detecta edge
    if last_z5 == 0 and z5_val == 1:
        add_mem("Z5")

    # Mantém disparo até o nível de fumaça ser normalizado
    if z5_val == 1:
        estado = DISPARO        # gera disparo
    last_z5 = z5_val

    # ---------- LED MEM ----------
    if estado == DESARMADO and mem:
        if time.ticks_diff(now, t_mem_led) > 500:
            t_mem_led = now
            led_mem.value(not led_mem.value())
    else:
        led_mem.off()

    # ---------- DISPARO (LED + BUZZER) ----------
    if not beep_ativo():
        if estado == DISPARO:
            if time.ticks_diff(now, t_buzzer) > 100:
                t_buzzer = now
                buzzer.value(not buzzer.value())
            if time.ticks_diff(now, t_led) > 100:
                t_led = now
                led_status.value(not led_status.value())
        else:
            buzzer.off()
            led_status.off()

    # ---------- DISPLAY ----------
    if time.ticks_diff(now, t_display) > 1000:
        t_display = now
        if estado == DESARMADO:
            if modo_mem:
                if mem:
                    zona = mem[display_index % len(mem)]
                    draw("MEM:", zona)
                    display_index += 1
                else:
                    draw("", "SEM DISPAROS")
            else:
                draw("", "DESARMADO")
        elif estado == ARMADO:
            draw("", "ARMADO")
        elif estado == DISPARO:
            if mem:
                zona = mem[display_index % len(mem)]
                draw("DISPARO", zona)
                display_index += 1
    time.sleep(0.01)