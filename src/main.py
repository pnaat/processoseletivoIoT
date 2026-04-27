import machine
import dht
import time

# Configuração dos Pinos
pino_dht = machine.Pin(4)
sensor = dht.DHT22(pino_dht)

led_verde = machine.Pin(18, machine.Pin.OUT)
led_vermelho = machine.Pin(19, machine.Pin.OUT)
buzzer = machine.Pin(21, machine.Pin.OUT)

# Parâmetros de Segurança
TEMP_LIMITE = 30.0
UMID_LIMITE = 70.0

print("Monitoramento Industrial Iniciado (Modo Local)")

while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        u = sensor.humidity()
        
        print(f"Temperatura: {t}°C | Umidade: {u}%")
        
        if t > TEMP_LIMITE or u > UMID_LIMITE:
            # Estado de Alerta
            led_verde.value(0)
            led_vermelho.value(1)
            # Beep intermitente
            buzzer.value(1)
            time.sleep(0.2)
            buzzer.value(0)
            print("!!! ALERTA DE SEGURANÇA !!!")
        else:
            # Estado Normal
            led_vermelho.value(0)
            led_verde.value(1)
            buzzer.value(0)
            
        time.sleep(1.5)
        
    except OSError:
        print("Erro na leitura do sensor.")