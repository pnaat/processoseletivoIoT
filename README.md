# Relatório Técnico: Monitor de Estoque Kanban Inteligente

## Identificação do Candidato
* **Nome completo:** Erick Felipe
* **GitHub:** https://github.com/luccyus/processoseletivoIoT

---

## Visão Geral da Solução
O projeto consiste no firmware para um sistema de balança inteligente projetado para o monitoramento em tempo real de linhas de montagem industriais. 
* **Objetivo:** Prevenir a parada de linhas de produção acompanhando o consumo de peças.
* **Funcionamento:** O sistema afere dinamicamente a variação de peso de uma caixa organizadora, reportando seu status (regular, crítica ou ausente) via comunicação Serial.
* **Interação:** Totalmente autônomo, desenhado para integração direta com esteiras de CI/CD e painéis de telemetria corporativos.

---

## Arquitetura do Sistema Embarcado
O código (`main.py`) foi desenvolvido utilizando o paradigma de Máquina de Estados Finitos (FSM) com arquitetura estritamente **não-bloqueante**.

* **Fluxo Principal:** Um loop infinito de varredura interroga o sensor a uma frequência de 4Hz (a cada 250ms).
* **Estrutura de Estados:**
  1. `STATE_REGULAR`: Carga nominal identificada (acima de 500g).
  2. `STATE_EMPTY`: Limiar de sub-estoque atingido (abaixo de 500g), disparando alerta de reposição.
  3. `STATE_ERROR`: Carga zerada ou negativa detectada, isolando a falha do sensor estrutural.
* **Interação de Componentes:** O driver customizado lê os pinos digitais do sensor através de deslocamento de bits (bit-banging) e converte o sinal bruto usando um fator de escala para extrair o peso em gramas.

---

## Componentes Utilizados na Simulação
O hardware virtual mapeado no `diagram.json` conta com:
* **Microcontrolador:** Placa `board-esp32-devkit-c-v4` (ESP32 DevKit C v4).
* **Sensor de Peso:** Célula de Carga conectada a um amplificador/conversor de 24 bits (mapeado com o ID `hx711`).
* **Pinagem:**
  * DT (Data) no pino 16.
  * SCK (Clock) no pino 4.
  * Alimentação em 3V3 e GND.1.

---

## Decisões Técnicas Relevantes
Para garantir o funcionamento perfeito durante a esteira de testes automatizados (Wokwi CI), as seguintes decisões de engenharia foram aplicadas:

* **Blindagem de Interrupções de Hardware (IRQ):** A leitura do HX711 foi isolada encapsulando a função com `machine.disable_irq()`. Isso impede que o escalonador do sistema operacional do ESP32 pause a execução do código no exato momento em que o pino SCK está em estado ALTO (HIGH), o que forçaria o sensor a entrar em modo "Power Down" e geraria leituras ruidosas de 0 gramas.
* **Driver Customizado Não-Bloqueante:** O uso de bibliotecas de prateleira foi descartado por conterem loops obstrutivos (`time.sleep`). O driver implementado avalia instantaneamente a flag `is_ready()` e, se o pino não estiver pronto, cede o processamento imediatamente.
* **Otimização do Emulador (Fast-forwarding):** Foi definido um atraso não-bloqueante de `time.sleep_ms(250)` no laço principal. Isso permite que a CPU do servidor do GitHub reconheça a ociosidade do chip e acelere o tempo virtual, evitando falhas por esgotamento de limite de tempo (Timeout) no fluxo de CI.

---

## Resultados Obtidos
* **Comportamento Final:** O sistema faz a transição perfeitamente entre os estados de caixa cheia (5000g), esvaziamento parcial (2500g), e caixa crítica (150g).
* **Requisitos:** Todos os requisitos técnicos, arquiteturais e de "Casamento de Strings" foram atendidos com êxito.
* **Simulação:** O fluxo na esteira de integração (GitHub Actions) executou e validou os 3 cenários extremos impostos pela banca sem falsos positivos, completando todos os *jobs* com status de sucesso total (Verde).
