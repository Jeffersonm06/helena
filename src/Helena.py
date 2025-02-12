from functions.audio import download_song_from_youtube
from functions.video import baixar_video_tiktok
from functions.sendEmail import send_email
from functions.pdf import convert_html_to_pdf, merge_pdfs, process_file_with_ocr_and_save
from process import load_json_file, find_best_match, chatbot_response
from pathlib import Path

class Helena:

    @classmethod
    def response(cls,user_name, user_input, commands_file="commands.json", intents_file="intents.json"):
        commands = load_json_file(commands_file)
        music_commands = commands.get("commands", {}).get("baixar musica", [])
        ttk_commands = commands.get("commands", {}).get("baixar ttk", [])
        email_commands = commands.get("commands", {}).get("email", [])
        text_pdf_commands = commands.get("commands", {}).get("text_pdf", [])
        html_pdf_commands = commands.get("commands",{}).get("html_pdf", [])
        merge_pdf_commands = commands.get("commands",{}).get("merge_pdf", [])

        # Processar comandos de música
        best_music_command = find_best_match(user_input.lower(), music_commands)
        if best_music_command:
            return cls.process_music_command(user_input, best_music_command)

        # Processar comandos TTK
        best_ttk_command = find_best_match(user_input.lower(), ttk_commands)
        if best_ttk_command:
            return cls.process_ttk_command(user_input, best_ttk_command)
        
        best_email_command = find_best_match(user_input.lower(), email_commands)
        best_text_pdf_command = find_best_match(user_input.lower(), text_pdf_commands)
        best_html_pdf_command = find_best_match(user_input.lower(), html_pdf_commands)
        best_merge_pdf_command = find_best_match(user_input.lower(), merge_pdf_commands)

        if best_email_command:
            return cls.process_email_command(best_email_command)
        
        if best_text_pdf_command:
            return cls.process_text_pdf_command(best_text_pdf_command)
        
        if best_html_pdf_command:
            return cls.process_html_pdf_command(best_html_pdf_command)
        
        if best_merge_pdf_command:
            return cls.process_merge_pdf_command(best_merge_pdf_command)
        

        # Se não for um comando conhecido, processa como uma intenção
        intent_response = chatbot_response(user_name,user_input, intents_file=intents_file)
        

        return {
            "type": "response",
            "message": intent_response,
            "status": "success"
        }

    @classmethod
    def process_music_command(cls, user_input, best_music_command):
        """
        Processa os comandos relacionados a músicas.
        """
        song_name = user_input[len(best_music_command):].strip()
        if not song_name:
            return {
                "type": "music",
                "message": "Por favor, especifique o nome da música.",
                "status": "failed"
            }

        song_path = download_song_from_youtube(song_name)
        if not song_path:
            return {
                "type": "response",
                "message": f"Erro ao tentar baixar a música '{song_name}'. Tente novamente.",
                "status": "failed"
            }

        return {
            "type": "music",
            "message": f"Essa é música que gostaria de baixar? {song_path}",
            "url": song_path,
            "status": "success"
        }

    @classmethod
    def process_ttk_command(cls, user_input, best_ttk_command):
        """
        Processa os comandos relacionados a TTK.
        """
        ttk_url = user_input[len(best_ttk_command):].strip()
        if not ttk_url:
            return {
                "type": "response",
                "message": "Por favor, especifique a url do video.",
                "status": "failed"
            }

        ttk = baixar_video_tiktok(ttk_url)
        return {
            "type": "ttk",
            "message": f"Tá na mão paizão.",
            "url": ttk,
            "status": "success"
        }

    @classmethod
    def process_email_command(cls, best_email_command):

        if best_email_command:
            return {
                "type": "form",
                "message": "Escreva seu email.",
                "status": "success"
            }

        return {
            "type": "response",
            "message": "Desculpe, não entendi.",
            "status": "error"
        }
    
    
    @classmethod
    def process_text_pdf_command(cls, best_text_pdf_command):

        if best_text_pdf_command:
            return {
                "type":"text_pdf",
                "message":"Envie o pdf ou imagem",
                "status":"success"
            }
        
        return {
            "type": "response",
            "message": "Desculpe, não entendi.",
            "status": "error"
        }
    

    @classmethod
    def process_html_pdf_command(cls, best_html_pdf_command):

        if best_html_pdf_command:
            return {
                "type":"html_pdf",
                "message":"Envie o arquivo html",
                "status":"success"
            }
        
        return {
            "type": "response",
            "message": "Desculpe, não entendi.",
            "status": "error"
        }
    

    @classmethod
    def process_merge_pdf_command(cls, best_merge_pdf_command):

        if best_merge_pdf_command:
            return {
                "type":"merge_pdf",
                "message":"envie os arquivos pdf",
                "status":"success"
            }
        
        return {
            "type": "response",
            "message": "Desculpe, não entendi.",
            "status": "error"
        }
    

    @classmethod
    def send_email(cls, to_email, subject, body):
        return send_email(to_email, subject, body)

    
    @classmethod
    def convert_html_pdf(cls, html, name):
        return convert_html_to_pdf(html, name)
    

    @classmethod
    def merge_pdfs(cls, pdf_files, output_name):
        return merge_pdfs(pdf_files, output_name)
    
    @classmethod
    def process_file_with_ocr_and_save(cls, pdf):
        return process_file_with_ocr_and_save(pdf)