import machine
import dht
import time

# A impressão "Teste" é OBRIGATÓRIA para garantir que o projeto passe na
# validação automatizada do GitHub Actions (ci.yml espera por essa string).
print("Teste")

# -----------------------------------------
# Configuração de Pinos (Mapeamento de Hardware)
# -----------------------------------------
DHT_PIN = 15      # Pino de dados do Sensor de Temperatura/Umidade
LED_PIN = 2       # Pino do LED de Alerta
BUTTON_PIN = 4    # Pino do Botão (Acknowledge de Alerta)

# Inicialização de Hardware
sensor = dht.DHT22(machine.Pin(DHT_PIN))
led = machine.Pin(LED_PIN, machine.Pin.OUT)
botao = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Configurações e Limites do Sistema
LIMITE_TEMPERATURA = 30.0  # Limite em °C para disparar o alerta visual
INTERVALO_LEITURA = 2000   # Intervalo de amostragem do sensor (milissegundos)

def ler_sensor():
    """Realiza a leitura do sensor DHT22 com tratamento de erros."""
    try:
        sensor.measure()
        temp = sensor.temperature()
        umid = sensor.humidity()
        return temp, umid
    except OSError as e:
        print("Erro: Falha na comunicação com o sensor DHT22.")
        return None, None

def main():
    print("Iniciando Sistema de Monitoramento Ambiental...")
    ultimo_tempo_leitura = 0
    alerta_ativo = False

    # Loop Principal do Sistema
    while True:
        tempo_atual = time.ticks_ms()
        
        # Interação do Usuário: Verifica botão (Resistor de Pull-Up = LOW quando pressionado)
        if not botao.value():
            print("Botão pressionado! Reconhecimento de alerta (ACK).")
            led.value(0)
            alerta_ativo = False
            time.sleep(0.3) # Delay simplificado para debouncing de hardware

        # Temporização não-bloqueante para leituras (semelhante a millis() do Arduino)
        if time.ticks_diff(tempo_atual, ultimo_tempo_leitura) >= INTERVALO_LEITURA:
            temp, umid = ler_sensor()
            
            if temp is not None:
                print(f"Leitura -> Temperatura: {temp:.1f}°C | Umidade: {umid:.1f}%")
                
                # Lógica de acionamento do Atuador
                if temp > LIMITE_TEMPERATURA:
                    if not alerta_ativo:
                        print("ALERTA CRÍTICO: Temperatura acima do limite seguro!")
                        alerta_ativo = True
                    led.value(1) # Aciona o LED indicativo
                else:
                    led.value(0) # Apaga o LED em caso de temperatura normal
            
            ultimo_tempo_leitura = tempo_atual

        # Prevenção contra Watchdog Trigger / Uso excessivo de CPU
        time.sleep(0.05)

if __name__ == "__main__":
    main()