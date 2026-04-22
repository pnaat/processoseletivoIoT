import machine
import time

# Configuração de Pinos
SENSOR_PIN = 15  # Slide switch simulando o sensor de vazamento
LED_GREEN_PIN = 13  # LED Verde (Sem vazamento)
LED_RED_PIN = 14  # LED Vermelho (Vazamento detectado)
BUZZER_PIN = 12  # Buzzer (Alarme sonoro)

# Inicialização
sensor = machine.Pin(SENSOR_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_green = machine.Pin(LED_GREEN_PIN, machine.Pin.OUT)
led_red = machine.Pin(LED_RED_PIN, machine.Pin.OUT)
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)

print("Teste")
print("Iniciando Verificador de Vazamento")

while True:
    estado_sensor = sensor.value()
    
    if estado_sensor == 1:
        # Vazamento detectado
        print("ALERTA: Vazamento Detectado no Telhado!")
        led_green.value(0)
        
        # Alarme intermitente (pisca LED vermelho e toca Buzzer)
        led_red.value(1)
        buzzer.value(1)
        time.sleep(0.3)
        
        led_red.value(0)
        buzzer.value(0)
        time.sleep(0.3)
        
    else:
        # Tudo seco, nenhum vazamento
        print("Status: Seco. Sem vazamentos.")
        led_green.value(1)
        led_red.value(0)
        buzzer.value(0)
        time.sleep(1)