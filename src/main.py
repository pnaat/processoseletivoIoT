# -*- coding: utf-8 -*-
# ============================================================================
#  Monitor de Estoque Kanban Inteligente  |  ESP32 + HX711 (MicroPython)
#  Processo Seletivo Intensivo Maker | IoT  -  Cenario: WEIGHT
#
#  Le o peso de uma celula de carga (HX711) e classifica o estado do estoque:
#    - Estoque Regular  -> telemetria dinamica do peso
#    - Caixa Vazia      -> dispara alerta unico de reposicao
#    - Reabastecimento  -> confirma retorno a carga cheia
#    - Anomalia (0 g)   -> caixa ausente / falha de calibracao
#
#  Arquitetura NAO-BLOQUEANTE: loop principal sem sleeps longos, temporizacao
#  via time.ticks_ms(), para nao perder a janela em que o Wokwi CI altera o peso.
# ============================================================================

from machine import Pin
import time

# --- Mapeamento de hardware (ver diagram.json) ------------------------------
PIN_DT  = 16   # HX711 DT  (linha de dados)
PIN_SCK = 4    # HX711 SCK (linha de clock)

# --- Calibracao -------------------------------------------------------------
# No HX711 do Wokwi a leitura bruta (raw) e linear com o controle "load":
#   fundo de escala 50 kg  ->  raw = 21000    =>    raw = 420 * carga
# Portanto, para converter a leitura bruta de volta para gramas:
#   gramas = raw / 420
ESCALA_RAW_POR_GRAMA = 420.0

# --- Regras de negocio (limiares em gramas) ---------------------------------
CARGA_CHEIA_G     = 5000   # carga nominal da caixa cheia
LIMIAR_CRITICO_G  = 1000   # <= : caixa vazia / sub-estoque -> reposicao
LIMIAR_REABASTE_G = 4000   # >= (apos alerta) : caixa reabastecida

# --- Temporizacoes ----------------------------------------------------------
INTERVALO_STATUS_MS = 400  # periodicidade do log de estoque regular
GRACA_INICIAL_MS    = 300  # janela p/ o cenario aplicar a carga inicial
PASSO_LOOP_MS       = 20   # passo curto do loop (mantem tudo responsivo)

# --- Estados da maquina de estados ------------------------------------------
ST_REGULAR = 0
ST_VAZIA   = 1


class HX711:
    """Driver bit-bang enxuto e nao-bloqueante para o HX711 do Wokwi."""

    def __init__(self, pino_dt, pino_sck):
        self.dt = Pin(pino_dt, Pin.IN)
        self.sck = Pin(pino_sck, Pin.OUT)
        self.sck.value(0)
        self._ultima_raw = 0

    def _pronto(self):
        # HX711 sinaliza "dado pronto" levando DT a nivel baixo.
        return self.dt.value() == 0

    def ler_raw(self):
        # Espera limitada pelo sinal de pronto: se estourar, reusa a ultima
        # leitura valida em vez de travar o loop (arquitetura nao-bloqueante).
        tentativas = 0
        while not self._pronto():
            tentativas += 1
            if tentativas > 1000:
                return self._ultima_raw
            time.sleep_us(1)

        valor = 0
        for _ in range(24):                # 24 bits, MSB primeiro
            self.sck.value(1)
            time.sleep_us(1)
            valor = (valor << 1) | self.dt.value()
            self.sck.value(0)
            time.sleep_us(1)

        self.sck.value(1)                  # 25o pulso: canal A, ganho 128
        time.sleep_us(1)
        self.sck.value(0)
        time.sleep_us(1)

        if valor & 0x800000:               # complemento de 2 (valores negativos)
            valor -= 0x1000000

        self._ultima_raw = valor
        return valor

    def ler_gramas(self):
        raw = self.ler_raw()
        if raw < 0:
            raw = 0
        return int(round(raw / ESCALA_RAW_POR_GRAMA))


def main():
    sensor = HX711(PIN_DT, PIN_SCK)

    # A) Inicializacao do sistema
    print("Sistema Kanban Inicializado")

    estado = ST_REGULAR
    anomalia_reportada = False
    t_status = time.ticks_ms()
    t_boot = time.ticks_ms()

    while True:
        # Janela de graca: da tempo do cenario aplicar a carga inicial e
        # descarta leituras instaveis do boot antes de decidir qualquer estado.
        if time.ticks_diff(time.ticks_ms(), t_boot) < GRACA_INICIAL_MS:
            sensor.ler_gramas()
            time.sleep_ms(10)
            continue

        peso = sensor.ler_gramas()

        # D) Anomalia: peso exatamente 0 g (abaixo ate da tara fisica) indica
        #    caixa ausente ou erro de calibracao -> log critico, sem reposicao.
        if peso <= 0:
            if not anomalia_reportada:
                print("ALERTA: Caixa ausente ou erro de calibração no sensor HX711!")
                anomalia_reportada = True
            time.sleep_ms(PASSO_LOOP_MS)
            continue
        else:
            anomalia_reportada = False

        # C) Consumo critico: caixa vazia -> alerta unico de reposicao.
        if peso <= LIMIAR_CRITICO_G:
            if estado != ST_VAZIA:
                print("Evento de reposição disparado! Caixa vazia detectada.")
                estado = ST_VAZIA

        # C) Reabastecimento: retorno ao patamar de carga cheia.
        elif estado == ST_VAZIA:
            if peso >= LIMIAR_REABASTE_G:
                print("Abastecimento concluído. Caixa cheia.")
                estado = ST_REGULAR

        # B) Estoque regular: telemetria dinamica periodica do peso atual.
        else:
            agora = time.ticks_ms()
            if time.ticks_diff(agora, t_status) >= INTERVALO_STATUS_MS:
                print("Status: Estoque Regular ({}g)".format(peso))
                t_status = agora

        time.sleep_ms(PASSO_LOOP_MS)


main()
