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
        if not self.is_ready():
            return None

        # Blindagem
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

        machine.enable_irq(irq_state)

        raw_value = count - 0x800000
        return int(raw_value / self.scale)

# Logica Principal
def main():
    sensor = HX711(dout_pin=16, pd_sck_pin=4)
    print("Sistema Kanban Inicializado")

    STATE_REGULAR = 1
    STATE_EMPTY = 2
    STATE_ERROR = 3

    # Adicionando constantes
    THRESHOLD_EMPTY = 500
    THRESHOLD_FULL = 4900

    current_state = None

    while True:
        weight = sensor.read_weight()

        if weight is not None:
            # Mensagem 5: Falha/Anomalia
            if weight <= 0:
                if current_state != STATE_ERROR:
                    print("ALERTA: Caixa ausente ou erro de calibração no sensor HX711!")
                    current_state = STATE_ERROR

            # Mensagem 3: Caixa Vazia
            elif weight < THRESHOLD_EMPTY:
                if current_state != STATE_EMPTY:
                    print("Evento de reposição disparado! Caixa vazia detectada.")
                    current_state = STATE_EMPTY

            # Mensagem 2 e 4: Estado Regular e Retorno de Carga
            else:
                if current_state == STATE_EMPTY and weight >= THRESHOLD_FULL:
                    print("Abastecimento concluído. Caixa cheia.")

                current_state = STATE_REGULAR

                print(f"Status: Estoque Regular ({weight}g)")

        time.sleep_ms(250)

if __name__ == '__main__':
    main()
