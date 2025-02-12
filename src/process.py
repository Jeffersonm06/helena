import json
import re
import random
import datetime
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import logging

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# Carregar modelo de embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Diretório base para os arquivos JSON
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "src/data"
CHAT_LOG_FILE = DATA_DIR / "chat.json"

def load_json_file(filename):
    """Carrega um arquivo JSON."""
    filepath = DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def save_chat_log(user_name, user_input, response, intent):
    """Salva a conversa no chat.json."""
    chat_entry = {
        "user": user_name,
        "text": user_input,
        "response": response,
        "intent": intent,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Carregar histórico existente
    if CHAT_LOG_FILE.exists():
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as file:
            chat_history = json.load(file)
    else:
        chat_history = []

    # Adicionar nova entrada e salvar
    chat_history.append(chat_entry)
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=4)

def clean_input(user_input):
    """Normaliza o texto do usuário."""
    return re.split(r':', user_input, maxsplit=1)[0].strip().lower()

def get_embedding(text):
    """Gera um embedding usando MiniLM."""
    return model.encode(text, convert_to_numpy=True)

def create_intent_embeddings(intents):
    """Cria embeddings para cada exemplo em intenções."""
    intent_embeddings = {}
    for category, subcategories in intents.items():
        for subcat_key, subcat_data in subcategories.items():
            if isinstance(subcat_data, dict) and "examples" in subcat_data:
                intent_embeddings[subcat_key] = [get_embedding(example) for example in subcat_data["examples"]]
    return intent_embeddings

def find_intent(user_input, intent_embeddings, threshold=0.80):
    """Encontra a intenção mais próxima com base na similaridade dos embeddings."""
    user_embedding = get_embedding(user_input)
    best_intent, highest_score = None, 0

    for intent, embeddings in intent_embeddings.items():
        for example_embedding in embeddings:
            score = cosine_similarity([user_embedding], [example_embedding])[0][0]
            if score > highest_score:
                highest_score, best_intent = score, intent

    return best_intent if highest_score >= threshold else None

def get_response(user_input, intents, intent_embeddings):
    """Gera uma resposta com base na intenção detectada."""
    detected_intent = find_intent(user_input, intent_embeddings)
    if detected_intent:
        for category, subcategories in intents.items():
            if detected_intent in subcategories:
                response = random.choice(subcategories[detected_intent]["response"])
                return response, detected_intent
    return "Desculpe, não entendi o que você quis dizer.", None

def chatbot_response(user_name, user_input, intents_file="intents.json"):
    """Carrega intenções e retorna uma resposta baseada em similaridade semântica."""
    intents = load_json_file(intents_file)
    intent_embeddings = create_intent_embeddings(intents)
    response, detected_intent = get_response(user_input, intents, intent_embeddings)

    # Salvar no log
    save_chat_log(user_name, user_input, response, detected_intent)

    return response

def find_best_match(user_input, command_list):
    """Encontra o comando mais semelhante na lista de comandos."""
    user_embedding = get_embedding(user_input)
    best_match, highest_score = None, 0

    for command in command_list:
        command_embedding = get_embedding(command)
        score = cosine_similarity([user_embedding], [command_embedding])[0][0]
        if score > highest_score:
            highest_score, best_match = score, command

    return best_match if highest_score >= 0.8 else None
