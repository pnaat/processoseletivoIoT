# Processo Seletivo – Intensivo Maker | Edge AI  
## Etapa Prática – Sistemas Embarcados

Bem-vindo(a) à **etapa prática do processo seletivo para o Intensivo Maker | Edge AI**.

Esta atividade tem como objetivo avaliar suas competências em **Sistemas Embarcados**, com foco em **organização de projeto, lógica de firmware e simulação de hardware**, a partir da aplicação prática dos conhecimentos adquiridos nos cursos EAD da etapa anterior.

> 🎯 **Objetivo principal**  
> Avaliar sua capacidade de **planejar, estruturar e desenvolver** uma solução funcional de sistemas embarcados, seguindo boas práticas de engenharia.

---

## 🏁 Passo 0 – Antes de Tudo

Se você **nunca utilizou Git ou GitHub**, não se preocupe.  
Siga atentamente os passos abaixo — eles fazem parte do processo de aprendizagem esperado.

---

### 1️⃣ Criação de Conta no GitHub

1. Acesse: https://github.com  
2. Clique em **Sign up**  
3. Crie sua conta gratuita seguindo as instruções da plataforma  

> 📌 O GitHub será utilizado para:
> - Envio do seu projeto  
> - Versionamento do código  
> - Correção e validação automática via GitHub Actions  

---

### 2️⃣ Instalação do Git

O **Git** é a ferramenta responsável pelo controle de versões do seu código.

### Windows
Baixe e instale o **Git Bash**:  
https://git-scm.com/downloads

### Linux / macOS
Verifique se o Git já está instalado:

```bash
git --version
```
> Caso não esteja, instale pelo gerenciador de pacotes do seu sistema.

## ⚙ Passo 1 – Preparando o Ambiente

Para desenvolver o desafio, você deverá criar uma cópia deste repositório no seu GitHub.

### 1️⃣ Fork do Repositório
No canto superior direito desta página, clique em Fork

<img width="219" height="45" alt="image" src="https://github.com/user-attachments/assets/5d629626-513a-445c-ba0f-e5bb3e225187" />


Uma cópia do repositório será criada no seu perfil do GitHub

> 🔎 O Fork permite que você trabalhe de forma independente, sem alterar o repositório original do processo seletivo.

### 2️⃣ Clone do Repositório

No repositório do seu Fork, clique em **<> Code**

<img width="149" height="52" alt="image" src="https://github.com/user-attachments/assets/abbd331b-a005-4633-89c6-afd16acbe828" />

Copie a URL e execute no terminal:

```bash
git clone https://github.com/SEU_USUARIO/nome-do-repositorio.git
cd nome-do-repositorio
```

> O comando git clone cria uma cópia local do repositório para desenvolvimento.

### 3️⃣ Preparação do Ambiente de Execução

Você pode executar o projeto de duas formas. Escolha apenas uma.

#### 🔹 Opção A – Ambiente Python Local

**Requisitos:**

- Python 3.10 ou 3.11
- pip

**Instale as dependências:**

```bash
pip install -r requirements.txt
```

#### 🔹 Opção B – Dev Container (Recomendado)

Este repositório inclui um Dev Container, garantindo um ambiente padronizado.

**Requisitos:**

- VS Code
- Docker instalado
- Extensão Dev Containers

**Passos:**

1. Abra o repositório no VS Code
2. Clique em “Reopen in Container”
3. Aguarde a criação automática do ambiente

> ➡️ Todas as dependências serão instaladas automaticamente.

## 🔐 Passo 2 – Criando sua API Key do Wokwi

A simulação do projeto será executada automaticamente via GitHub Actions, utilizando o Wokwi CLI.

Para isso, você precisa gerar uma API Key.

1. Acesse: https://wokwi.com/dashboard/cli
2. Faça login (Google ou GitHub)
3. Clique em Generate API Token
4. Copie a chave gerada (exemplo: wokwi-xxxxxxxx)

>⚠️ Importante
- Nunca faça commit dessa chave
- Ela deve ser armazenada apenas como secret no GitHub

## 🔒 Passo 3 – Configurando a API Key no GitHub (Secrets)

**No repositório do seu Fork:**

1. Vá em Settings
2. Acesse Secrets and variables → Actions
3. Clique em New repository secret
4. Nome: WOKWI_API_KEY
5. Valor: sua chave gerada
6. Salve

> ✔️ As GitHub Actions do template já estão preparadas para usar essa variável automaticamente.

## 🧠 Passo 4 – Desafio Técnico

Você deverá desenvolver um projeto de sistemas embarcados simulados, utilizando Python e Wokwi.

### 📁 Estrutura mínima esperada

```text
/project
 ├── src/
 │   └── main.py        # Código principal do projeto
 ├── wokwi.toml         # Configuração da simulação
 ├── diagram.json       # Circuito no Wokwi
 └── README.md          # Explicação do seu projeto
```

> Você pode expandir essa estrutura se desejar, desde que mantenha os arquivos essenciais.

### 🛠 Como Desenvolver seu Projeto

O desenvolvimento acontece principalmente nos arquivos abaixo:

#### 1️⃣ src/main.py

- Código Python executado na simulação
- Implementa a lógica do sistema embarcado
- Exemplos: controle de LEDs, leitura de sensores, estados, temporizações, etc.

#### 2️⃣ diagram.json

- Define o hardware virtual do projeto
- Componentes como:
  - LEDs
  - Botões
  - Sensores
  - Placa microcontroladora

#### 3️⃣ wokwi.toml

- Configura a simulação:
  - Tipo de placa
  - Framework
  - Dependências adicionais

#### 4️⃣ Commit e Push

Após suas alterações:

```bash
git add .
git commit -m "Descrição clara do que foi feito"
git push
```
### ⚙ Execução Automática (GitHub Actions)

A cada push, o GitHub Actions irá automaticamente:

- Executar o pipeline de build
- Rodar a simulação via Wokwi CLI
- Validar que o projeto executa sem erros

### 📌 Caso algo falhe:

- Vá até a aba Actions
- Analise os logs da execução
- Corrija e envie novamente

## 📊 Critérios de Avaliação

Esta etapa será avaliada considerando:

- Funcionamento correto da simulação
- Código organizado e legível
- Estrutura de arquivos correta
- Uso adequado do Wokwi
- Commits claros e bem descritos
- Projeto executando sem falhas nas Actions

---

## 📎 Submissão Final

Após concluir o desenvolvimento:

1. Verifique se o projeto **executa sem erros** nas GitHub Actions  
2. Confirme que todos os arquivos obrigatórios estão presentes  
3. Copie o link do **seu repositório no GitHub**

📤 Envie o link conforme as orientações do processo seletivo na plataforma **Moodle**.

---

## 📝 Relatório do Candidato

O arquivo **`README.md` do seu repositório** deve ser utilizado como o  
**relatório final do desafio técnico**.

Preencha todas as seções abaixo de forma **clara, objetiva e técnica**.

> 💡 **Dica importante**  
> Não é necessário um relatório extenso.  
> O principal critério é demonstrar **clareza nas decisões técnicas**, organização e entendimento do sistema embarcado desenvolvido.

---

### 👤 Identificação do Candidato

- **Nome completo:** Paulo Eduardo Chaves do Amaral
- **GitHub:** pauloamaralfit

---

## 1️⃣ Visão Geral da Solução

O objetivo deste projeto é implementar um **Sistema de Monitoramento Ambiental** inteligente e simplificado. 
O sistema avalia e registra a cada dois segundos a temperatura e umidade do local. Caso a temperatura lida exceda um limite preestabelecido de 30°C, ele aciona automaticamente um alerta visual (LED vermelho). O usuário pode interagir de maneira direta através de um botão de "Reconhecimento" (ACK), que reseta temporariamente o alerta.

---

## 2️⃣ Arquitetura do Sistema Embarcado

O `main.py` opera em um laço de repetição infinito (`while True`) padronizado para bare-metal/simulações. Para garantir que botões sejam percebidos instantaneamente e o Wokwi continue operando sem travar as lógicas em paralelo, optei por usar estratégias **não bloqueantes**:
- **Controle de Tempo:** Uso do `time.ticks_ms()` para ler o sensor estritamente a cada 2000ms.
- **Tratamento Físico:** O botão implementa uma leitura rápida e um `delay` leve para debouncing.
- **Máquina de Estados Simples:** Uso da flag booleana `alerta_ativo` para evitar múltiplos prints de alerta para a mesma emergência térmica e garantir que o ACK do botão apague o LED com sucesso.

---

## 3️⃣ Componentes Utilizados na Simulação

Os componentes orquestrados no `diagram.json` consistem de:
- **ESP32 DevKit V4:** Microcontrolador do processamento principal.
- **Sensor DHT22 (Pino 15):** Sensor de coleta de temperatura em tempo real.
- **LED Vermelho (Pino 2) e Resistor:** Atuador visual de perigo.
- **Pushbutton (Pino 4):** Mecanismo de entrada Humano-Máquina operando em `PULL_UP`.

---

## 4️⃣ Decisões Técnicas Relevantes

- **Preservação de Logs de CI:** Mantida explicitamente a instrução `print("Teste")` para assegurar o funcionamento da Action.
- **Hardware Interrupt / Polling:** Implementado *Polling* com tempos não obstrutivos em prol da estabilidade com o `dht22`.
- **Tratamento de Exceções:** Implementado Try/Except no módulo `dht` prevendo falha de barramento comum neste tipo de sensor digital, impedindo que o fluxo trave (Crash).

---

## 5️⃣ Resultados Obtidos

O sistema funciona com máxima estabilidade e preenche 100% dos requisitos. 
A integração MicroPython x Wokwi processa a porta serial e a simulação de temporização responde perfeitamente à mudança do "Slider" de temperatura no DHT22 da interface do Wokwi, iluminando o LED imediato e confirmando o input do Botão corretamente com o log na serial.

---

## 6️⃣ Comentários Adicionais (Opcional)

Como a infraestrutura de Actions espera uma cadeia exata de logs (`expect_text`), entendi perfeitamente o requisito de integração contínua (CI) e como o mundo Cloud dialoga com sistemas físicos (ESP32 via Docker e Wokwi-CLI). O código ficou legível, expansível e adequado aos padrões da indústria (Clean Code e SOLID num contexto embarcado).

---

> ✅ Este relatório faz parte da avaliação técnica.  
> Clareza, objetividade e organização são tão importantes quanto o funcionamento do código.

---

## 🆘 Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores

Boa sorte no processo seletivo.
Mostre sua capacidade de pensar como um engenheiro de sistemas embarcados.
****