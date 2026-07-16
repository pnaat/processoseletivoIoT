# Monitor de Estoque Kanban Inteligente

> Relatório técnico da etapa prática — **Processo Seletivo Intensivo Maker | IoT**
> Cenário escolhido: **WEIGHT** (célula de carga + HX711 no ESP32, firmware em MicroPython).

---

## Identificação do Candidato

- **Nome completo:** José Alberto  <!-- complete com seu nome civil completo -->
- **GitHub:** [@albertosilva007](https://github.com/albertosilva007)

---

## Visão Geral da Solução

O projeto simula um **monitor de estoque Kanban** para almoxarifados e linhas de
montagem. Uma caixa de insumos repousa sobre uma célula de carga lida por um
**HX711**; a partir do peso, o firmware classifica em tempo real o estado do
estoque e emite eventos pela serial, eliminando a inspeção visual manual e
prevenindo parada de linha por falta de componente.

O sistema reconhece quatro situações:

- **Estoque Regular** — peso acima do limite de segurança; publica telemetria dinâmica.
- **Caixa Vazia** — peso cai ao nível crítico; dispara um alerta único de reposição.
- **Reabastecimento** — peso retorna à carga cheia; confirma a normalização.
- **Anomalia** — leitura de exatamente `0 g` (abaixo da tara física); trata como caixa ausente / falha de calibração.

Não há interação por botão: o "usuário" é o próprio fluxo de peso injetado pelo
simulador, e toda a saída é observável na comunicação serial (UART).

---

## Arquitetura do Sistema Embarcado

**Fluxo principal (`src/main.py`):**

1. Instancia o driver `HX711` e imprime `Sistema Kanban Inicializado`.
2. Aplica uma breve **janela de graça** para o cenário estabelecer a carga inicial,
   descartando leituras instáveis de boot.
3. Entra no laço principal, onde a cada iteração lê o peso e avalia a máquina de estados.

**Máquina de estados (2 estados + tratamento de anomalia):**

```
        peso == 0
   ┌──────────────────────────► ANOMALIA (log único)
   │
[REGULAR] ── peso ≤ 1000 g ──► [VAZIA] ── peso ≥ 4000 g ──► [REGULAR]
   │                              (alerta de              (abastecimento
   │ telemetria periódica          reposição único)        concluído)
   └── "Status: Estoque Regular (Xg)"
```

**Temporização não-bloqueante:** todo o controle de tempo usa
`time.ticks_ms()` / `time.ticks_diff()` (janela de graça, cadência do log de
status). O laço avança em passos curtos de 20 ms e a espera pelo sinal de
"dado pronto" do HX711 é **limitada por contador** — se estourar, reusa a
última leitura válida em vez de travar. Isso garante que o firmware nunca perca
a janela em que o Wokwi CI altera o peso.

---

## Componentes Utilizados na Simulação

| Componente | ID no `diagram.json` | Função |
| :--- | :--- | :--- |
| ESP32 DevKit C v4 | `esp` | Microcontrolador; executa o firmware MicroPython e a UART de log. |
| HX711 + célula de carga | `hx711` | Amplificador/ADC de 24 bits; fornece a leitura de peso (controle `load`, tipo `50kg`). |
| Serial Monitor (UART) | `$serialMonitor` | Canal de saída validado pelo Wokwi CI (`wait-serial`). |

**Ligações (MCU ↔ HX711):** `D16 → DT` (dados), `D4 → SCK` (clock),
`5V → VCC`, `GND → GND`.

---

## Decisões Técnicas Relevantes

- **Calibração raw → gramas.** No HX711 do Wokwi a leitura bruta é linear com o
  controle `load` (fundo de escala 50 kg ⇒ raw 21000, isto é `raw = 420 × carga`).
  O firmware converte de volta com `gramas = raw / 420`, o que reproduz
  exatamente os valores dos cenários (5000, 2500, 150, 0). O fator fica isolado
  na constante `ESCALA_RAW_POR_GRAMA`.
- **Driver HX711 próprio (bit-bang).** Implementado em ~30 linhas: leitura de 24
  bits MSB-first, 25º pulso para canal A / ganho 128 e conversão em complemento
  de 2. Sem dependências externas, mantendo o firmware enxuto.
- **Alertas idempotentes por estado.** Reposição e abastecimento disparam apenas
  na *transição* de estado (não a cada leitura), evitando flood na serial e
  disparos prematuros — requisito explícito do Teste 1.
- **Anomalia isolada do fluxo de reposição.** `0 g` é tratado como falha de
  hardware (log próprio) e **não** aciona pedido de reposição, distinguindo
  "caixa vazia" (nível crítico) de "caixa ausente" (leitura inválida).
- **Constantes nomeadas** para todos os limiares e tempos, facilitando ajuste.

### Ajustes de infraestrutura fora do `src/`

Durante a análise identifiquei dois pontos na automação que impediriam a
aprovação e foram corrigidos de forma mínima:

1. **Detecção de cenário no `ci.yml`** procurava `scenarios/WEIGHT.txt` (extensão
   inexistente) e caía no *fallback* `WEIGHT` em maiúsculo — que não casa com a
   pasta `weight` num runner Linux (case-sensitive). Ajustado para detectar o
   `.md` remanescente e emitir o nome da pasta em minúsculo.
2. **Secret do Wokwi:** o workflow referencia `secrets.WOKWI_CLI_TOKEN`; portanto
   o token do Wokwi CI deve ser cadastrado no fork com esse nome exato.

---

## Resultados Obtidos

Com os três cenários oficiais de `scenarios/weight/`:

| Teste | Estímulo (`load`) | Saída serial validada | Resultado |
| :--- | :--- | :--- | :--- |
| **1 — Consumo Parcial** | 5000 → 2500 g | `Status: Estoque Regular (2500g)` | ✅ sem disparo prematuro |
| **2 — Ciclo Completo** | 150 → 5000 g | `Evento de reposição disparado! Caixa vazia detectada.` → `Abastecimento concluído. Caixa cheia.` | ✅ |
| **3 — Anomalia** | 5000 → 0 g | `ALERTA: Caixa ausente ou erro de calibração no sensor HX711!` | ✅ |

Todas as mensagens conferem **byte a byte** (acentuação e pontuação inclusas)
com as strings `wait-serial` dos cenários, atendendo à verificação estrita do CI.

---

## Comentários Adicionais

- **Principal desafio:** descobrir a relação `load → raw` do HX711 simulado, já
  que o valor bruto lido por bit-bang precisa ser calibrado para reproduzir os
  gramas esperados na string de status.
- **Limitação:** a detecção de `0 g` como anomalia assume que a tara física real
  nunca chega a zero; num hardware real, conviria uma faixa de guarda em vez do
  valor exato.
- **Melhorias com mais tempo:** média móvel de leituras para suavizar ruído,
  histerese nos limiares de estado e publicação da telemetria via MQTT.

---

## Como Reproduzir

1. Faça *fork* deste repositório.
2. Em **Settings → Secrets and variables → Actions**, crie o secret
   **`WOKWI_CLI_TOKEN`** com o token gerado em <https://wokwi.com/dashboard/ci>.
3. Qualquer `push` dispara o workflow **ESP32 Filesystem Build**, que compila o
   `fs.bin` (Docker) e roda os 3 cenários de `scenarios/weight/` no Wokwi CI.
