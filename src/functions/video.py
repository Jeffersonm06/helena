import yt_dlp
import os
import subprocess

download_dir = './media/video/'

def baixar_video_tiktok(url):
    # Certifique-se de que o diretório de download exista
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Opções para baixar o vídeo sem marca d'água
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,  # Não baixar playlists, apenas o vídeo
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Salvar no diretório especificado
        'writethumbnail': True,  # Baixar miniaturas, se possível
        'no_warnings': True,
        'quiet': False,
    }

    # Usar yt-dlp para baixar o vídeo
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info_dict)

    # Definindo o nome do arquivo de saída em MP4
    output_filename = f"{os.path.splitext(video_filename)[0]}.mp4"

    # Converter o vídeo para MP4 usando FFmpeg
    if video_filename != output_filename:
        # Comando FFmpeg para converter o vídeo
        subprocess.run(['ffmpeg', '-i', video_filename, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_filename])

        # Remover o arquivo original (não MP4)
        os.remove(video_filename)

    # Retornar apenas o nome do arquivo sem o diretório
    url = os.path.basename(output_filename)
    print("url: ",url)
    return url
