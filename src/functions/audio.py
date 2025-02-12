import os
import yt_dlp
import speech_recognition as sr
from pydub import AudioSegment
import re


# Defina o diretório onde as músicas serão salvas
DOWNLOAD_DIR = 'src/media/music/'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


def sanitize_filename(filename):
    """
    Remove ou substitui caracteres inválidos no nome do arquivo.
    """
    sanitized = re.sub(r'[:/\\?%*|"<>]', '', filename)
    return sanitized.strip()


def download_song_from_youtube(song_name):
    """
    Busca e baixa a música do YouTube pelo nome.
    """
    search_query = f"ytsearch:{song_name}"
    
    # Opções para yt-dlp
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': f'{DOWNLOAD_DIR}%(title)s.%(ext)s',  # Define o diretório de download
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(search_query, download=True)  # Faz o download da música
            # Pega o primeiro item da busca (o mais relevante)
            downloaded_file = ydl.prepare_filename(result['entries'][0])  # Nome do arquivo gerado
            sanitized_title = sanitize_filename(f"{song_name}.mp3")
            final_file_path = os.path.join(DOWNLOAD_DIR, sanitized_title)

            # Renomeia para o nome correto, se necessário
            if not os.path.exists(final_file_path):
                os.rename(downloaded_file, final_file_path)
                print(f"Música '{song_name}' baixada com sucesso: {final_file_path}")
            else:
                print(f"A música '{song_name}' já existe no caminho: {final_file_path}")

            # Retorna apenas o nome do arquivo, sem o diretório
            return os.path.basename(final_file_path)  # Retorna o nome do arquivo

        except Exception as e:
            print(f"Erro ao buscar a música no YouTube: {e}")
            return None
        

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    try:
        # Abrir o arquivo de áudio
        with sr.AudioFile(file_path) as source:
            print("Carregando áudio...")
            audio_data = recognizer.record(source)  # Ler o áudio do arquivo

        # Usar Google Speech API para transcrição
        print("Transcrevendo...")
        text = recognizer.recognize_google(audio_data, language="pt-BR")  # Use 'en-US' para inglês
        return text

    except sr.UnknownValueError:
        return "Não foi possível entender o áudio."
    except sr.RequestError as e:
        return f"Erro ao acessar o serviço de reconhecimento: {e}"

def convert_to_wav(input_path, output_path):
    """
    Converte um arquivo de áudio para o formato WAV.
    """
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        print(f"Arquivo convertido com sucesso: {output_path}")
    except Exception as e:
        print(f"Erro ao converter o áudio: {e}")


def transcribe_audio(file_path):
    """
    Transcreve o áudio de um arquivo WAV para texto.
    """
    recognizer = sr.Recognizer()
    try:
        # Carregar o arquivo de áudio
        with sr.AudioFile(file_path) as source:
            print("Carregando áudio para transcrição...")
            audio_data = recognizer.record(source)

        # Transcrever o áudio usando a API do Google
        print("Transcrevendo áudio...")
        text = recognizer.recognize_google(audio_data, language="pt-BR")
        return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio."
    except sr.RequestError as e:
        return f"Erro ao acessar o serviço de reconhecimento: {e}"

""" # Caminhos dos arquivos
input_file = "audio2.ogg"  # Arquivo de entrada
output_file = "audio.wav"  # Arquivo de saída

# Converter para WAV e transcrever
convert_to_wav(input_file, output_file)
transcription = transcribe_audio(output_file)
print("Transcrição:", transcription) """