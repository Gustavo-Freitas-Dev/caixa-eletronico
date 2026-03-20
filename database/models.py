import json
import os

def carregar_dados():
    if not os.path.exists("db.json"):
        with open("db.json", "w", encoding="utf-8") as f:
            json.dump({"usuarios": []}, f, indent=4, ensure_ascii=False)

    with open("db.json", "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(dados):
    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)