from machine import Pin
import time

# Primeiro, vamos habilitar os pinos a serem utilizados
botao = Pin(26, Pin.IN, Pin.PULL_UP)
led = Pin(22, Pin.OUT)
buzzer = Pin(23, Pin.OUT)
pir = Pin(14, Pin.IN)
gas = Pin(12, Pin.IN)

# Definiremos três estados para nossa Central de Alarme
DESARMADO = 0
ARMADO = 1
DISPARADO = 2

# Por padrão, a simulação se inicia com o sistema DESARMADO
estado = DESARMADO
zona_disparo = None # guarda último registro de disparo

# Defini-se uma função para que o usuário tenha uma confirmação visual da aplicação
def piscar_led(vezes, tempo=0.2):
    for _ in range(vezes):
        led.on()
        time.sleep(tempo)
        led.off()
        time.sleep(tempo)

# Gerando um loop, verifica estado do botão
while True:
    if botao.value() == 0:  # pressionado
        time.sleep(0.25)  
        if estado == DESARMADO:
            estado = ARMADO
            zona_disparo = None
            piscar_led(1)
        else:
            estado = DESARMADO
            zona_disparo = None
            piscar_led(2)
            buzzer.off()

        # espera soltar botão
        while botao.value() == 0:
            pass

    # Definição da lógica do sistema
    if estado == ARMADO:
        led.off()

        # Zona 1 - PIR
        if pir.value() == 1:
            estado = DISPARADO
            zona_disparo = "ZONA 1 - MOVIMENTO"

        # Zona 2 - GÁS
        elif gas.value() == 1:
            estado = DISPARADO
            zona_disparo = "ZONA 2 - GÁS/FUMAÇA"

    elif estado == DISPARADO:
        # LED piscando rápido
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
        buzzer.on() # sirene contínua
        continue
    else:
        led.off()
        buzzer.off() # desativa sirene
    time.sleep(0.05)
