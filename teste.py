import cv2
import numpy as np

# Função para ajustar contraste e brilho
def adjust_contrast_brightness(frame, alpha=2.0, beta=50):
    """
    Ajusta o contraste e brilho de uma imagem.
    :param frame: Quadro do vídeo (imagem)
    :param alpha: Fator de contraste (1.0 = sem alteração, >1 aumenta contraste)
    :param beta: Fator de brilho (valor positivo ou negativo)
    :return: Quadro ajustado
    """
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

# Processar o vídeo
def process_video_with_contrast(video_path, output_path, alpha=2.0, beta=50):
    # Abra o vídeo
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Configura o writer para salvar o novo vídeo com contraste ajustado
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec para vídeo
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Sai do loop se o vídeo terminar

        frame_count += 1
        
        # Ajusta contraste e brilho do quadro
        enhanced_frame = adjust_contrast_brightness(frame, alpha=alpha, beta=beta)
        
        # Exibir progresso no console
        print(f"Processando quadro {frame_count}/{total_frames}")
        
        # Escrever o quadro processado no arquivo de saída
        out.write(enhanced_frame)
    
    # Liberar os recursos
    cap.release()
    out.release()
    print("Processamento concluído. Vídeo salvo em:", output_path)

# Caminho do vídeo de entrada e saída
input_video = r"videoplayback.mp4"  # Substitua pelo caminho do vídeo de entrada
output_video = r"videoplayback_contraste.mp4"  # Caminho para salvar o vídeo de saída

# Ajustar o contraste do vídeo
process_video_with_contrast(input_video, output_video, alpha=2.0, beta=50)
