import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = 'r10911207@gmail.com'
PASSWORD = 'ycrv uiyn jatp vtbt'

# Configurar o e-mail
def send_email(to_email, subject, body):
    try:
        # Criar o cabeçalho da mensagem
        msg = MIMEMultipart()
        msg['From'] = 'Helena'
        msg['To'] = to_email
        msg['Subject'] = subject

        # Adicionar o corpo do e-mail
        msg.attach(MIMEText(body, 'plain'))

        # Conectar ao servidor SMTP e enviar o e-mail
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Iniciar conexão segura
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")