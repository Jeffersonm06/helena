import os
from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    send_file, abort,
    Response
    )
from flask_cors import CORS
import src.Helena as Helena
from functions.update_data import update_json
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, 'documents')
TEMP_DIR = "temp"

# Função para classificar intenções ou buscar definições
@app.route('/h/chat', methods=['POST'])
def helena():
    data = request.json
    print("Requisição recebida:", data)  # Para debugging
    if 'text' not in data or 'user_name' not in data:
        return jsonify({"error": "No text or user_name provided"}), 400

    user_input = data['text']
    user_name = data['user_name']  # Identifica o usuário para gerenciar o contexto

     # Tente obter uma resposta prévia
    pre_response_result = Helena.response(user_input)
    if pre_response_result:  # Se houver uma resposta prévia, retorne-a
        return jsonify(pre_response_result)


@app.route('/h/video/<path:filename>', methods=['GET'])
def serve_video(filename):
    try:
        # Caminho completo do arquivo
        filepath = os.path.join(BASE_DIR, filename)

        # Verificar se o arquivo existe
        if not os.path.isfile(filepath):
            return abort(404, description="Arquivo não encontrado")

        # Implementar suporte a streaming
        range_header = request.headers.get('Range', None)
        if range_header:
            range_match = range_header.replace("bytes=", "").split("-")
            start = int(range_match[0])
            end = int(range_match[1]) if len(range_match) > 1 and range_match[1] else None

            file_size = os.path.getsize(filepath)
            end = end if end is not None else file_size - 1

            if start >= file_size or end >= file_size:
                return abort(416, description="Range inválido")

            chunk_size = end - start + 1
            with open(filepath, "rb") as f:
                f.seek(start)
                data = f.read(chunk_size)

            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(chunk_size),
                "Content-Type": "video/mp4",
            }

            return Response(data, status=206, headers=headers)

        # Retornar o arquivo completo (se não for streaming)
        return send_file(filepath, mimetype="video/mp4")
    
    except Exception as e:
        return str(e), 500
    

@app.route('/h/file/<path:filename>', methods=['GET'])
def serve_files(filename):
    # Defina os diretórios de mídia
    music_dir = os.path.join('media', 'music')
    video_dir = os.path.join('media', 'video')

    # Caminho completo do arquivo nos respectivos diretórios
    music_file_path = os.path.join(music_dir, filename)
    video_file_path = os.path.join(video_dir, filename)

    # Verifique se o arquivo existe no diretório de música
    if os.path.exists(music_file_path):
        print(f"Enviando música: {music_file_path}")
        return send_from_directory(music_dir, filename, as_attachment=True)

    # Verifique se o arquivo existe no diretório de vídeo
    elif os.path.exists(video_file_path):
        print(f"Enviando vídeo: {video_file_path}")
        return send_from_directory(video_dir, filename, as_attachment=True)

    # Se o arquivo não for encontrado
    else:
        print(f"Arquivo não encontrado: {filename}")
        return "Arquivo não encontrado", 404

@app.route('/h/music', methods=['GET'])
def get_music_files():
    try:
        music_folder = 'media/music'
        
        # Verificar se o diretório existe
        if not os.path.exists(music_folder):
            return jsonify({"error": "Diretório de músicas não encontrado"}), 404
        
        # Listar arquivos de música no diretório
        music_files = [f for f in os.listdir(music_folder) if os.path.isfile(os.path.join(music_folder, f))]
        
        if not music_files:
            return jsonify({"message": "Nenhuma música encontrada"}), 404
        
        # Retornar a lista de músicas (nomes ou caminhos relativos)
        return jsonify({"music_files": music_files}), 200
    
    except Exception as e:
        return jsonify({"error": f"Erro ao tentar listar músicas: {str(e)}"}), 500
    
@app.route('/h/video', methods=['GET'])
def get_video_files():
    try:
        video_folder = 'media/video'
        
        # Verificar se o diretório existe
        if not os.path.exists(video_folder):
            return jsonify({"error": "Diretório de músicas não encontrado"}), 404
        
        # Listar arquivos de música no diretório
        video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]
        
        if not video_files:
            return jsonify({"message": "Nenhuma música encontrada"}), 404
        
        # Retornar a lista de músicas (nomes ou caminhos relativos)
        return jsonify({"video_files": video_files}), 200
    
    except Exception as e:
        return jsonify({"error": f"Erro ao tentar listar músicas: {str(e)}"}), 500


@app.route('/update/data', methods=['POST'])
def update_data():
    try:
        # Parse o JSON da requisição
        request_data = request.json
        path = request_data.get("path")
        new_examples = request_data.get("new_examples")
        new_responses = request_data.get("new_responses")

        if not path:
            return jsonify({"error": "O campo 'path' é obrigatório"}), 400
        
        # Atualizar o JSON
        global json_data
        json_data = update_json(json_data, path, new_examples, new_responses)

        # Salvar o JSON atualizado
        with open("h/data/intents.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        return jsonify({"message": "Dados atualizados com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/get/data', methods=['GET'])
def get_data():
    try:
        # Carregar o JSON do arquivo
        with open("h/data/intents.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
        return jsonify(json_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)