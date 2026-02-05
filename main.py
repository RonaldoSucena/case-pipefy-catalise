# =========================
# IMPORTS
# =========================
import os
import requests
import zipfile
import io
import pandas as pd
from dotenv import load_dotenv

print("🚀 Projeto Pipefy Catálise iniciado com sucesso!")

# =========================
# ENV / CONFIGURAÇÃO

# =========================
load_dotenv()

PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")
if not PIPEFY_TOKEN:
    raise Exception("❌ PIPEFY_TOKEN não encontrado no .env")

print("🔐 Token Pipefy carregado com sucesso")

PIPE_ID = os.getenv("PIPE_ID")
FIELD_RAZAO_SOCIAL = os.getenv("PIPE_FIELD_RAZAO")
FIELD_CNPJ = os.getenv("PIPE_FIELD_CNPJ")
FIELD_PATRIMONIO = os.getenv("PIPE_FIELD_PATRIMONIO")
PIPEFY_API_URL = os.getenv("API_URL", "https://api.pipefy.com/graphql")
ZIP_URL = os.getenv("ZIP_URL", "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/registro_fundo_classe.zip")
CSV_NAME= os.getenv("CSV_NAME", "registro_fundo.csv")

# =========================
# FUNÇÕES
# =========================
def criar_card_pipefy(razao_social, cnpj, patrimonio):

    headers = {
        "Authorization": f"Bearer {PIPEFY_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": """
        mutation ($pipe_id: ID!, $fields: [FieldValueInput!]!) {
          createCard(input: {
            pipe_id: $pipe_id
            fields_attributes: $fields
          }) {
            card { id }
          }
        }
        """,
        "variables": {
            "pipe_id": PIPE_ID,
            "fields": [
                {"field_id": FIELD_RAZAO_SOCIAL, "field_value": razao_social},
                {"field_id": FIELD_CNPJ, "field_value": str(cnpj)},
                {"field_id": FIELD_PATRIMONIO, "field_value": str(patrimonio)}
            ]
        }
    }

    response = requests.post(PIPEFY_API_URL, json=payload, headers=headers)
    return response.json()

# =========================
# ETAPA 1 – DOWNLOAD ZIP
# =========================

print("📦 Indo buscar o arquivo na CVM...")
resposta = requests.get(ZIP_URL)

if resposta.status_code != 200:
    raise Exception("Erro ao baixar arquivo da CVM")

print("✅ ZIP baixado com sucesso")

# =========================
# ETAPA 2 – LER CSV DO ZIP
# =========================
print("📂 Lendo CSV direto do ZIP")

zip_em_memoria = zipfile.ZipFile(io.BytesIO(resposta.content))

with zip_em_memoria.open(CSV_NAME) as arquivo_csv:
    df = pd.read_csv(arquivo_csv, sep=";", encoding="latin1")

print(f"📊 Total de linhas carregadas: {len(df)}")

# =========================
# ETAPA 3 – FILTROS
# =========================
df_filtrado = df[
    (df["Tipo_Fundo"] == "FIDC") &
    (df["Situacao"] == "Em Funcionamento Normal") &
    (df["Gestor"] == "CATÁLISE INVESTIMENTOS LTDA.")
]

print(f"🎯 Total de fundos após filtro: {len(df_filtrado)}")

# =========================
# ETAPA 4 – TESTE 1 CARD
# =========================
#print("\n🧪 TESTE – Criando 1 card no Pipefy")

#linha = df_filtrado.iloc[0]

#resultado = criar_card_pipefy(
#    razao_social=linha["Denominacao_Social"],
#    cnpj=linha["CNPJ_Fundo"],
#    patrimonio=linha["Patrimonio_Liquido"]
#)

#print(resultado)

print("\n🚀 ETAPA 4 – Criando TODOS os cards no Pipefy")

sucesso = 0
erro = 0
detalhes = []

for _, linha in df_filtrado.iterrows():
    resultado = criar_card_pipefy(
        razao_social=linha["Denominacao_Social"],
        cnpj=linha["CNPJ_Fundo"],
        patrimonio=linha["Patrimonio_Liquido"]
    )

    if "errors" in resultado:
        erro += 1
        detalhes.append({
            "fundo": linha["Denominacao_Social"],
            "status": "erro",
            "mensagem": resultado["errors"]
        })
        print("❌ Erro:", linha["Denominacao_Social"])
    else:
        sucesso += 1
        card_id = resultado["data"]["createCard"]["card"]["id"]
        detalhes.append({
            "fundo": linha["Denominacao_Social"],
            "status": "sucesso",
            "card_id": card_id
        })
        print("✅ Card criado:", linha["Denominacao_Social"], "| ID:", card_id)

import json
from datetime import datetime

log_execucao = {
    "data_execucao": datetime.now().isoformat(),
    "total_fundos": len(df_filtrado),
    "cards_criados": sucesso,
    "erros": erro,
    "detalhes": detalhes
}

os.makedirs("logs", exist_ok=True)

with open("logs/run_logs.json", "w", encoding="utf-8") as f:
    json.dump(log_execucao, f, ensure_ascii=False, indent=2)

print("\n📊 RESUMO FINAL")
print(f"Total processados: {len(df_filtrado)}")
print(f"Cards criados: {sucesso}")
print(f"Erros: {erro}")
print("📝 Log salvo em logs/run_logs.json")
