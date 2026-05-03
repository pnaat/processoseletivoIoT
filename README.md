# Projeto de IoT - Processo Seletivo PNAAT

**- Nome:** Samuel Jackson Mesquita Lima  
**- E-mail:** samuel.jacksonjml@gmail.com  
**- Data da entrega:** 03/05/2026 

## 📌 Resumo do Projeto
> Trata-se de um sistema de segurança que utiliza o conceito de supervisão por acionamento eletrônico. O sistema simula o funcionamento de uma central de alarme ao supervisionar as ferramentas de UP e DOWN do simulador e do ESP32 para supervisão;
> O sistema de segurança opera em três modos: `ARMADO`, `DESARMADO` e `DISPARADO`, de acordo com as interações com a simulação. 
> O usuário pode armar/desarmar a central, verificar quais zonas foram violadas (geraram disparo) desde o último arme, pressionar botões de pânico, interagir com sensores de movimento e alterar detecção de um sensor de fumaça. 
> Todas as interações têm por objetivo simular uma interação com uma central de alarme real, onde o usuário pode observar como esse tipo de equipamento funciona.

## 📲 Como executar
**1.** Instale as dependências: `pip install -r requirements.txt`  
**2.** Acesse o simulador Wokwi  
**3.** Execute o simulador  
**4.** Aguarde a simulação carregar, até que apareça no visor a legenda `DESARMADO`
**5.** Interaja com a Central de Alarme através dos botões e sensores

## 📂 Arquivos
```
ProcessoSeletivoIoT/  
 ├── src/
 │   └── main.py                    # Código principal do projeto
 ├── diagram.json                   # Circuito no Wokwi
 ├── README.md                      # Este arquivo
 ├── requirements.txt               # Pré-requisitos para funcionamento do programa
 ├── ssd1306.py                     # Config recomendadas para uso do board-ssd1306 no Wokwi
 └── wokwi.toml                     # Configuração da simulação

```

## 🧩 Composição do Sistema de Segurança dentro do simulador (Hardware)
**- 1.** 1x microcontrolador ESP32: `wokwi-esp32-devkit-v1`  
**- 2.** 2x botão: `wokwi-pushbutton`  
**- 3.** 2x led: `wokwi-led`  
**- 4.** 1x sirene: `wokwi-buzzer`  
**- 5.** 2x sensor de movimento PIR: `wokwi-pir-motion-sensor`  
**- 6.** 1x sensor de fumaça: `wokwi-gas-sensor`  
**- 7.** 2x resistor de 150 Ohms: `wokwi-resistor`  
**- 8.** 1x visor OLED: `wokwi-board-ssd1306`  

## 📢 Zoneamento e Operações dos equipamentos de segurança
**- Zona 1.** - BOTÃO DE PÂNICO AUDÍVEL 24 HORAS
> A qualquer momento, ao ser pressionado → gera disparo.
**- Zona 2.** - BOTÃO DE PÂNICO SILENCIOSO 24 HORAS
> A qualquer momento, ao ser pressionado → entra na memória de disparo sem acionar sirenes e leds.
**- Zona 3.** - SENSOR DE MOVIMENTO TEMPORIZADO
> Com o sistema `ARMADO`, ao detectar movimento → inicia uma contagem de 5 segundos e se o sistema não for para o estado `DESARMADO` dentro desse intervalo gera disparo.
**- Zona 4.** - SENSOR DE MOVIMENTO IMEDIATO
> Com o sistema `ARMADO`, ao detectar movimento → gera disparo.
**- Zona 5.** - SENSOR DE GÁS/FUMAÇA 24 HORAS
> A qualquer momento, se a leitura do equipamento obtiver registro abaixo de 350 ppm → gera disparo. A leitura deve ser normalizada (acima de 350 ppm) para que o sistema possa ser desarmado.

## 🚨 Respostas visuais
- **O visor identifica o estado atual da Central de Alarme entre `ARMADO`, `DESARMADO` e mostra uma lista de zonas disparadas quando em `DISPARO`**
- **O LED Vermelho e o Buzzer indicam Status:** 
    - 1 bipe          = o sistema foi Armado
    - 2 bipes         = o sistema foi Desarmado
    - bipes contínuos = o sistema foi Violado, disparo
- **O LED Azul pisca se houver algum endereço de zona no histórico de disparos**
- **O Botão ARME/DESARME permite alterar o modo de operação da Central entre `ARMADO` e `DESARMADO` ao ser pressionado**
- **O Botão MEM permite ser mostrado no visor uma lista de zonas disparadas, se houver, ao ser pressionado e enquanto a Central de Alarme estiver no modo `DESARMADO`**
- **O histórico de disparos é uma lista que contém, na ordem em que ocorreram os eventos e apenas uma vez para cada zona, os endereços de zonas que foram acionados desde o último evento de ARME. O histórico é, portanto, limpo na próxima vez que o sistema for armado**

## 💬 Comentários sobre o projeto
- As instruções do Actions, do vídeo e/ou do README inicial não ajudam a resolver o problema da Key do simulador Wokwi, que parece ter instruções erradas para acessar o Secrects do repositório;
- Apesar de seguir todos os passos no README inicial, propostos pelo PNAAT, ainda não é possível passar do `timeout` da CI, acredito que por alguma limitação do simulador ou dos parâmetros do Action;
- Foi necessário adicionar um arquivo `ssd1306.py`, que contém as configurações do hardware utilizado na simulação, não bastando apenas adicionar uma biblioteca através da plataforma de simulação Wokwi.

## 🎯 Considerações finais e uso de IAs
> Foram utilizadas ferramentas de Inteligência Artificial como Claude e ChatGPT com a finalidade de compreender e programar as configurações necessárias para rodar o arquivo `ssd1306.py` citado acima. Nesse caso, tais ferramentas serviram apenas para o propósito de compreensão do que é necessário para o simulador Wokwi rodar corretamente as funções do `board-ssd1306`, não participando, portanto, de nenhuma linha de código na `main.py`ou em qualquer outro arquivo;
> As mesmas IAs citadas acima serviram para pesquisa quanto ao problema comum a essa etapa do processo seletivo, onde eu e outros colegas tivemos dificuldades em passar pelos padrões exigidos pelo pipeline, o que inclui o `print("Teste")` no começo da main como tentativa de superar a falha por 'timeout'.

## 🔍 Link para o repositório original do desafio
[Repositório base PNAT](https://github.com/pnaat/processoseletivoIoT)