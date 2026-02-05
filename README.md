# 📊 Automação de Ingestão de Fundos FIDC – Pipefy

Automação completa para ingestão de dados públicos da CVM e criação automática de cards no Pipefy, facilitando o controle operacional de fundos FIDC.

---

## 🎯 Objetivo

Eliminar o processo manual de cadastro de fundos, garantindo:

- ✅ **Padronização** - Todos os dados seguem o mesmo formato
- ✅ **Rastreabilidade** - Logs detalhados de cada execução
- ✅ **Escalabilidade** - Processa centenas de fundos automaticamente
- ✅ **Confiabilidade** - Integração via GraphQL com tratamento de erros

---

## 📋 O que o Projeto Faz

O script automatiza o seguinte fluxo:

1. 📦 **Download** - Baixa o arquivo ZIP da CVM via HTTPS
2. 📂 **Leitura** - Lê o CSV diretamente em memória (sem salvar em disco)
3. 🔍 **Filtro** - Aplica regras de negócio para seleção de fundos
4. 🚀 **Criação** - Cria cards no Pipefy automáticamente via GraphQL
5. 📊 **Logging** - Gera relatório JSON com sucesso/erro de cada operação

---

## 🔧 Pré-requisitos

Antes de começar, certifique-se que você tem:

- **Python 3.7+** instalado
- **pip** (gerenciador de pacotes Python)
- **Token de autenticação do Pipefy** (disponível em Configurações > Tokens)
- Acesso à internet (para baixar dados da CVM e conectar com Pipefy)

---

## 📥 Instalação

### 1. Clone ou faça download do projeto

```bash
git clone https://github.com/RonaldoSucena/case-pipefy-catalise.git
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Isso instalará:
- `requests` - Para fazer requisições HTTP
- `python-dotenv` - Para gerenciar variáveis de ambiente
- `pandas` - Para processar dados em CSV

---

## ⚙️ Configuração

### 1. Copie o arquivo `.env.example`

```bash
# Windows - Command Prompt
copy .env.example .env

# Windows - PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

### 2. Edite o arquivo `.env` com seu token

Abra o arquivo `.env` que foi criado e substitua o valor de `PIPEFY_TOKEN`:

```bash
# .env (antes)
PIPEFY_TOKEN=seu_token_aqui

# .env (depois)
PIPEFY_TOKEN=seu_token_real_aqui
```

**Como obter seu token**:
1. Acesse a plataforma Pipefy
2. Clique no seu usuário > **Configurações**
3. Procure por **Tokens de API**
4. Gere um novo token (ou reutilize um existente)
5. Copie o token e cole no arquivo `.env`

⚠️ **IMPORTANTE**: Nunca compartilhe seu token ou faça commit do `.env` no git!

### 3. Configure os dados do Pipefy no `.env`

**Esta é uma etapa OBRIGATÓRIA**. Você precisa informar os IDs do seu pipe e dos campos no `.env`:

Abra o arquivo `.env` e preencha:

```bash
# Identificação do Pipefy
PIPEFY_TOKEN=seu_token_real_aqui
PIPE_ID=seu_id_do_pipe_aqui

# IDs dos campos no seu pipe (obtenha na interface do Pipefy)
PIPE_FIELD_RAZAO=raz_o_social
PIPE_FIELD_CNPJ=cnpj
PIPE_FIELD_PATRIMONIO=patrim_nio_l_quido
```

**Configurações opcionais** (têm valores padrão):
```bash
# URLs e nomes (você só precisa alterar se mudar de fonte)
ZIP_URL=https://dados.cvm.gov.br/dados/FI/CAD/DADOS/registro_fundo_classe.zip
CSV_NAME=registro_fundo.csv
API_URL=https://api.pipefy.com/graphql
```

---

## 🚀 Como Executar

Execute o script com:

```bash
python main.py
```

### Andamento da Execução

Durante a execução, você verá mensagens como:

```
🚀 Projeto Pipefy Catálise iniciado com sucesso!
🔐 Token Pipefy carregado com sucesso
📦 Indo buscar o arquivo na CVM...
✅ ZIP baixado com sucesso
📂 Lendo CSV direto do ZIP
📊 Total de linhas carregadas: 1234
🎯 Total de fundos após filtro: 45
🧪 TESTE – Criando 1 card no Pipefy
🚀 ETAPA 4 – Criando TODOS os cards no Pipefy
✅ Card criado: FUNDO A | ID: 123456
✅ Card criado: FUNDO B | ID: 123457
...
📊 RESUMO FINAL
Total processados: 45
Cards criados: 45
Erros: 0
📝 Log salvo em logs/run_logs.json
```

---

## 📁 Estrutura do Projeto

```
Pipefy/
├── main.py                  # Script principal
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
├── .env                    # Variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
└── logs/
    └── run_logs.json      # Relatório de execução em JSON
```

---

## 📝 Logs e Relatórios

Após cada execução, um arquivo JSON é gerado em `logs/run_logs.json`:

```json
{
  "data_execucao": "2026-02-05T14:30:45.123456",
  "total_fundos": 45,
  "cards_criados": 45,
  "erros": 0,
  "detalhes": [
    {
      "fundo": "FUNDO ABC",
      "status": "sucesso",
      "card_id": "123456789"
    },
    {
      "fundo": "FUNDO XYZ",
      "status": "erro",
      "mensagem": "{\n  \"message\": \"Field not found\"\n}"
    }
  ]
}
```

Você pode analisar este arquivo para:
- ✅ Verificar quais fundos foram processados com sucesso
- ❌ Identificar erros que precisam ser corrigidos
- 📊 Gerar relatórios de execução

---

## 📊 Arquitetura

```
┌─────────────────────────────────────────────┐
│     SERVIDOR CVM (Dados Públicos)           │
│  https://dados.cvm.gov.br/...               │
└────────────┬────────────────────────────────┘
             │ (ZIP + CSV)
             ▼
┌─────────────────────────────────────────────┐
│     SCRIPT PYTHON (Processamento)           │
│  • Download ZIP                             │
│  • Leitura CSV em memória                   │
│  • Filtros de negócio                       │
│  • Transformação de dados                   │
└────────────┬────────────────────────────────┘
             │ (GraphQL)
             ▼
┌─────────────────────────────────────────────┐
│    API PIPEFY (Criação de Cards)            │
│  https://api.pipefy.com/graphql             │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│   BANCO DE DADOS PIPEFY                     │
│  Cards com informações de fundos            │
└─────────────────────────────────────────────┘
```