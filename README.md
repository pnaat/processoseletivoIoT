# 🏭 Sistema de Monitoramento de Segurança Industrial (IIoT Edge)

Este projeto consiste em um sistema de monitoramento ambiental focado em segurança industrial, utilizando um ESP32 e MicroPython para detectar condições críticas de temperatura e umidade.

## 👤 Identificação do Candidato

* **Nome completo:** [Seu Nome Aqui]
* **GitHub:** [Seu Usuário Aqui]

## 1️⃣ Visão Geral da Solução

* **Objetivo:** Monitorar em tempo real as condições climáticas de um ambiente industrial para prevenir danos em maquinários sensíveis.
* **O que o sistema faz:** Realiza a leitura constante de temperatura e umidade. Se os valores excederem os limites de segurança (30°C ou 70% de umidade), o sistema ativa um alarme sonoro e visual.
* **Interação do Usuário:** O usuário acompanha os logs via console e visualiza o status através de LEDs (Verde para OK, Vermelho para Alerta) e um Buzzer.

## 2️⃣ Arquitetura do Sistema Embarcado

A arquitetura lógica é baseada em um **Loop de Controle Infinito** (Super Loop) executado no `main.py`:

1.  **Inicialização:** Configuração dos pinos GPIO para o sensor DHT22, LEDs e Buzzer.
2.  **Leitura:** O sensor DHT22 é consultado a cada 2 segundos.
3.  **Processamento:** O ESP32 compara os valores lidos com as constantes `TEMP_LIMITE` e `UMID_LIMITE`.
4.  **Atuação:** * **Estado Seguro:** LED Verde ligado.
    * **Estado de Alerta:** LED Verde desliga, LED Vermelho liga e o Buzzer emite um sinal intermitente.



## 3️⃣ Componentes Utilizados na Simulação

Os componentes abaixo foram integrados através do arquivo `diagram.json`:

* **Placa:** ESP32 DevKit V1.
* **Sensor DHT22:** Medição de temperatura e umidade.
* **LED Verde:** Indicador visual de operação dentro dos parâmetros normais.
* **LED Vermelho:** Indicador visual de estado crítico/alerta.
* **Buzzer Ativo:** Alarme sonoro intermitente para atrair a atenção do operador.
* **Resistores (220Ω):** Utilizados em série com os LEDs para limitação de corrente e proteção dos componentes.

## 4️⃣ Decisões Técnicas Relevantes

* **Separação de Estados:** A lógica foi dividida de forma que os atuadores (LEDs/Buzzer) respondam imediatamente à mudança de estado do sensor.
* **Resiliência:** Implementação de tratamento de erro (`try-except`) na leitura do sensor DHT22, garantindo que falhas momentâneas de hardware não interrompam a execução do programa.
* **Timing:** O intervalo de leitura foi ajustado para 1.5s - 2s para respeitar as limitações físicas de resposta do sensor DHT22.

## 5️⃣ Resultados Obtidos

* **Funcionalidade:** O sistema opera conforme o esperado no simulador Wokwi.
* **Alerta Sonoro:** O buzzer responde com bipes curtos durante o estado de alerta, facilitando a identificação do problema.
* **Precisão:** A simulação demonstra que o sistema reage instantaneamente assim que os sliders de temperatura/umidade do Wokwi ultrapassam os limites definidos.

## 6️⃣ Comentários Adicionais

* **Dificuldades:** A principal dificuldade foi a organização das conexões de terra (GND) comuns entre todos os componentes no arquivo de configuração JSON.
* **Melhorias Futuras:** Implementação de uma interface de rede para envio de dados via protocolo MQTT para um dashboard remoto (ex: Node-RED).