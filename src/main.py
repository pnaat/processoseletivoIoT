import machine
import time

# Driver do sensor
class HX711:
    def __init__(self, dout_pin, pd_sck_pin):
        self.dout = machine.Pin(dout_pin, machine.Pin.IN)
        self.pd_sck = machine.Pin(pd_sck_pin, machine.Pin.OUT)
        self.pd_sck.value(0)
        self.scale = 420.0

    def is_ready(self):
        return self.dout.value() == 0

    def read_weight(self):
        # Se o sensor não estiver pronto, sai da função
        if not self.is_ready():
            return None

        # Desativa as interrupções do ESP32
        irq_state = machine.disable_irq()

        count = 0
        for _ in range(24):
            self.pd_sck.value(1)
            count = count << 1
            self.pd_sck.value(0)
            if self.dout.value():
                count += 1

        self.pd_sck.value(1)
        count = count ^ 0x800000
        self.pd_sck.value(0)

        # Reativa as interrupções do sistema
        machine.enable_irq(irq_state)

        raw_value = count - 0x800000
        return int(raw_value / self.scale)

# Logica principal
def main():
    # Inicializa o sensor nos pinos definidos
    sensor = HX711(dout_pin=16, pd_sck_pin=4)
    # Mensagem 1: Inizialização
    print("Sistema Kanban Inicializado")

    STATE_REGULAR = 1
    STATE_EMPTY = 2
    STATE_ERROR = 3

    current_state = None
    last_printed_weight = None

    while True:
        # Tenta ler o peso. Se retornar None, o loop continua
        weight = sensor.read_weight()

        if weight is not None:
            # Mensagem 5: Anomalia/Falha
            if weight <= 0:
                if current_state != STATE_ERROR:
                    print("ALERTA: Caixa ausente ou erro de calibração no sensor HX711!")
                    current_state = STATE_ERROR

            elif weight < 500:
                # Mensagem 3: Caixa Vazia
                if current_state != STATE_EMPTY:
                    print("Evento de reposição disparado! Caixa vazia detectada.")
                    current_state = STATE_EMPTY

            # Regular
            else:
                # Mensagem 4: Transição de retorno de carga cheia
                if current_state == STATE_EMPTY and weight >= 4900:
                    print("Abastecimento concluído. Caixa cheia.")
                    current_state = STATE_REGULAR
                    print(f"Status: Estoque Regular ({weight}g)")
                    last_printed_weight = weight

                # Configuração inicial ou transição de erro para regular
                elif current_state != STATE_REGULAR:
                    current_state = STATE_REGULAR
                    print(f"Status: Estoque Regular ({weight}g)")
                    last_printed_weight = weight

                # Mensagem 2: Saída
                else:
                    # Filtro
                    if last_printed_weight is None or abs(weight - last_printed_weight) > 5:
                        print(f"Status: Estoque Regular ({weight}g)")
                        last_printed_weight = weight

        time.sleep_ms(10)

if __name__ == '__main__':
    main()
