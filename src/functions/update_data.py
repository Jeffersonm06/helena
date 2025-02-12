import json

# Função para adicionar ou atualizar o JSON
def update_json(data, path, new_examples=None, new_responses=None):
    keys = path.split('.')
    sub_dict = data
    for key in keys[:-1]:
        sub_dict = sub_dict.setdefault(key, {})
    
    last_key = keys[-1]
    if last_key not in sub_dict:
        sub_dict[last_key] = {
            "examples": [],
            "response": []
        }
    
    if new_examples:
        sub_dict[last_key]["examples"].extend(new_examples)
        sub_dict[last_key]["examples"] = list(set(sub_dict[last_key]["examples"]))  # Remove duplicados
    
    if new_responses:
        sub_dict[last_key]["response"].extend(new_responses)
        sub_dict[last_key]["response"] = list(set(sub_dict[last_key]["response"]))  # Remove duplicados
    
    return data

# Exemplo de uso
json_data = {
    # JSON inicial fornecido aqui
}

# Caminho da categoria/subcategoria a ser atualizada
path = "greeting.evening"

# Novos exemplos e respostas a serem adicionados
new_examples = ["Boa noite", "Oi, boa noite"]
new_responses = ["Boa noite!", "Oi, tudo bem?"]

# Atualizar o JSON
updated_data = update_json(json_data, path, new_examples, new_responses)

# Salvar o JSON atualizado em um arquivo
with open("h/data/intents.json", "w", encoding="utf-8") as f:
    json.dump(updated_data, f, ensure_ascii=False, indent=4)

print("JSON atualizado com sucesso!")
