import os

def format_txt_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            
            formatted_lines = []
            combining = False
            for line in lines:
                stripped_line = line.strip()
                
                if stripped_line.startswith("Answer:"):
                    # Adiciona a linha da resposta e para o processamento
                    formatted_lines.append(line)
                    combining = False
                    break
                
                # Detecta linhas que começam com as letras "A-F"
                if stripped_line.startswith(("A.", "B.", "C.", "D.", "E.", "F.")):
                    if combining:
                        # Junta linhas subsequentes na mesma linha
                        formatted_lines[-1] = formatted_lines[-1].strip() + " " + stripped_line
                    else:
                        formatted_lines.append(line)
                        combining = True
                else:
                    # Linha fora do padrão "A-F" ou parte do enunciado
                    formatted_lines.append(line)
                    combining = False

            # Sobrescreve o arquivo com o conteúdo formatado
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(formatted_lines)

            print(f"Arquivo formatado: {file_name}")

# Caminho da pasta contendo os arquivos .txt
folder_path = "output_texts"  # Substitua pelo caminho da sua pasta
format_txt_files(folder_path)
