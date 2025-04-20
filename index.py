import cv2
import pytesseract
import os

# Configure o caminho do Tesseract OCR (necessário para Windows)
# Em sistemas Linux/Mac, normalmente não é necessário configurar o caminho manualmente.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Altere conforme necessário

# Função para extrair texto de um quadro de vídeo usando Tesseract
def extract_text_from_frame(frame):
    # Converta o quadro para escala de cinza (melhora a precisão do OCR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Opcional: Aplique limiarização para remover ruídos
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Extraia texto usando Tesseract OCR
    text = pytesseract.image_to_string(thresh, lang="eng")  # Substitua 'eng' pelo idioma desejado
    return text

# Função para processar o vídeo com intervalos de 1 minuto
def process_video(video_path, output_folder, frame_interval):
    # Verifique se a pasta de saída existe, caso contrário, crie-a
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Abra o vídeo
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Obtém a taxa de quadros do vídeo
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Número total de quadros do vídeo
    if total_frames != 0:
        duration = total_frames / frame_rate  # Duração total do vídeo em segundos
    else:
        duration = 0
    print(f"FPS do vídeo: {frame_rate}, Total de quadros: {total_frames}, Duração: {duration:.2f} segundos")

    current_time = 140_40  # Inicializa o tempo atual no vídeo
    frame_count = 1   # Contador de quadros processados
    text = ''
    while current_time < duration:
        # Move para o quadro correspondente ao timestamp atual
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)  # Define o tempo em milissegundos
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler o quadro.")
            break  # Sai do loop se todos os quadros forem processados ou ocorrer um erro
        
        frame_count += 1
        if text != extract_text_from_frame(frame) and 'Answer:' in extract_text_from_frame(frame) or extract_text_from_frame(frame) and 'Answer :' in extract_text_from_frame(frame) or extract_text_from_frame(frame) and 'Answer(s):' in extract_text_from_frame(frame):
        # Extraia texto do quadro


            text = extract_text_from_frame(frame)
            text = text.replace("www.shapingpixel.com", "")
            text = text.replace("www. shapingpixel.com", "")
            text = text.replace("Answer :", "Answer:")
            text = text.replace("Answer(s):", "Answer:")
            # Divida o texto em linhas
            lines = text.split("\n")
            
            # Localize a última linha com "Answer:"
            trimmed_lines = []
            for line in lines:
                trimmed_lines.append(line)
                if "Answer:" in line:
                    break  # Pare de adicionar linhas após encontrar "Answer:"
            
            # Combine novamente as linhas em um único texto formatado
            formatted_text = "\n".join(trimmed_lines)
            print(formatted_text)
            # Salve o texto em um arquivo
            output_file = os.path.join(output_folder, f"frame_{frame_count}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(formatted_text)
            
            print(f"Processado minuto {current_time//60 }: texto salvo em {output_file}")
        
        # Avança o tempo em 1 minuto
        current_time += frame_interval
    
    cap.release()

# Caminho do vídeo e pasta de saída
video_path = r"videoplayback.mp4"  # Substitua pelo caminho do vídeo
output_folder = "output_texts_2"

# Intervalo de tempo (em segundos) entre quadros processados - neste caso, 1 minuto
frame_interval = 30  # 60 segundos

# Execute o processamento do vídeo
process_video(video_path, output_folder, frame_interval)
