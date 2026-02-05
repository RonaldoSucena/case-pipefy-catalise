
# Automação de Ingestão de Fundos FIDC – Pipefy

## Contexto
Projeto de automação para ingestão de dados públicos da CVM e criação automática de cards no Pipefy para controle operacional de fundos FIDC.

## Objetivo
Eliminar o processo manual de cadastro de fundos, garantindo:
- padronização
- rastreabilidade
- escalabilidade

## Arquitetura
- Fonte: Dados públicos da CVM (ZIP + CSV)
- Processamento: Python + Pandas
- Integração: Pipefy API (GraphQL)
- Observabilidade: logs em JSON

## Regras de Negócio
- Tipo de Fundo: FIDC
- Situação: Em Funcionamento Normal
- Gestor: CATÁLISE INVESTIMENTOS LTDA.

## O que o script faz
1. Baixa o arquivo ZIP da CVM via HTTP
2. Lê o CSV diretamente em memória
3. Aplica filtros de negócio
4. Cria cards no Pipefy via GraphQL
5. Gera log detalhado da execução

## Como executar
```bash
pip install -r requirements.txt
python main.py

