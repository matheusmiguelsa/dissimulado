import tkinter as tk
from tkinter import messagebox
import os

# Função para ler perguntas de arquivos txt
def load_questions_from_files(folder_path):
    questions = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Dividir o texto em duas partes: antes e depois de "Answer:"
                parts = content.split("Answer:")
                question_part = parts[0].strip() if len(parts) > 1 else content.strip()
                correct_answer = parts[1].strip() if len(parts) > 1 else None
                
                # Dividir pergunta e capturar opções completas
                lines = question_part.split("\n")
                question_text = []
                options = []
                current_option = None  # Armazena o texto da opção atual enquanto está sendo montada

                for line in lines:
                    stripped_line = line.strip()

                    # Detecta início de uma nova opção
                    if stripped_line.startswith(("A.", "B.", "C.", "D.", "E.", "F.")):
                        # Salva a opção anterior antes de começar uma nova
                        if current_option:
                            options.append(current_option)
                        current_option = stripped_line  # Inicia uma nova opção
                    elif current_option:
                        # Continua a adicionar texto à opção atual
                        current_option += " " + stripped_line
                    else:
                        # Texto do enunciado
                        question_text.append(stripped_line)

                # Salvar a última opção, se existir
                if current_option:
                    options.append(current_option)

                # Adicionar validação para evitar perguntas incompletas
                if not correct_answer or not options:
                    print(f"Erro no arquivo {file_name}: Resposta correta ou opções ausentes.")
                    continue

                # Determinar tipo da questão (única ou múltipla escolha)
                answer_set = correct_answer.replace(" ", "").split(",")
                question_type = "multiple" if len(answer_set) > 1 else "single"

                # Criar estrutura da pergunta
                question = {
                    "text": "\n".join(question_text),  # Mantém o formato original do enunciado
                    "options": options, 
                    "answer": set(answer_set), 
                    "type": question_type
                }
                questions.append(question)
    return questions


# Classe do aplicativo de quiz
class QuizApp:
    def __init__(self, root, questions):
        self.root = root
        self.root.title("Quiz Application")
        self.questions = questions
        self.current_question_index = 0
        self.time_left = 120  # Tempo por pergunta em segundos (2 minutos)
        
        # Interface gráfica
        self.question_label = tk.Label(root, text="", wraplength=500, justify="left", font=("Arial", 14))
        self.question_label.pack(pady=20)
        
        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=10)
        
        self.timer_label = tk.Label(root, text=f"Time left: {self.time_left} seconds", font=("Arial", 12))
        self.timer_label.pack(pady=10)
        
        self.next_button = tk.Button(root, text="Next", command=self.next_question, state="disabled", font=("Arial", 12))
        self.next_button.pack(pady=10)
        
        self.load_question()
        self.update_timer()

    def load_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question["text"])
            
            # Limpa as opções anteriores
            for widget in self.options_frame.winfo_children():
                widget.destroy()
            
            # Exibe as opções e habilita o botão ao selecionar
            self.selected_options = {}
            if question["type"] == "multiple":
                # Múltipla escolha (Checkboxes)
                for option in question["options"]:
                    self.selected_options[option] = tk.BooleanVar()
                    cb = tk.Checkbutton(
                        self.options_frame, 
                        text=option, 
                        variable=self.selected_options[option], 
                        font=("Arial", 12),
                        command=self.enable_next_button  # Habilitar o botão ao selecionar
                    )
                    cb.pack(anchor="w")
            else:
                # Única escolha (Radiobuttons)
                self.selected_option = tk.StringVar()
                for option in question["options"]:
                    rb = tk.Radiobutton(
                        self.options_frame, 
                        text=option, 
                        variable=self.selected_option, 
                        value=option, 
                        font=("Arial", 12),
                        command=self.enable_next_button  # Habilitar o botão ao selecionar
                    )
                    rb.pack(anchor="w")
            
            self.time_left = 120  # Reseta o timer para 2 minutos
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.next_button.config(state="disabled")
        else:
            messagebox.showinfo("Quiz Finished", "You have completed the quiz!")
            self.root.destroy()

    def enable_next_button(self):
        # Habilita o botão "Next" quando uma opção é selecionada
        self.next_button.config(state="normal")

    def check_answer(self):
        question = self.questions[self.current_question_index]
        if question["type"] == "multiple":
            # Comparar seleção múltipla
            selected_answers = {option.split(".")[0] for option in self.selected_options if self.selected_options[option].get()}
        else:
            # Comparar única escolha
            selected_answers = {self.selected_option.get().split(".")[0]}
        
        # Verifique se as respostas selecionadas correspondem às respostas corretas
        return selected_answers == question["answer"]

    def save_attempt(self, question, is_correct):
        # Caminho do arquivo para salvar os resultados
        result_file = "quiz_results.txt"
        
        # Estrutura de registro
        result_text = (
            f"Question: {question['text'].split('.')[0]}\n"
            f"Correct Answer: {', '.join(question['answer'])}\n"
            f"Your Answer: {', '.join(self.get_selected_answers(question['type']))}\n"
            f"Result: {'Correct' if is_correct else 'Incorrect'}\n"
            f"{'-'*50}\n"
        )
        
        # Abrir o arquivo no modo append e salvar o registro
        with open(result_file, "a", encoding="utf-8") as f:
            f.write(result_text)

    def get_selected_answers(self, question_type):
        # Obtém as respostas selecionadas pelo usuário
        if question_type == "multiple":
            return {option.split(".")[0] for option in self.selected_options if self.selected_options[option].get()}
        else:  # Única escolha
            return {self.selected_option.get().split(".")[0]}

    def next_question(self):
        if any(var.get() for var in self.selected_options.values()) or self.selected_option.get():
            # Checar se a resposta está correta
            question = self.questions[self.current_question_index]
            is_correct = self.check_answer()
            
            # Salvar a tentativa no arquivo
            self.save_attempt(question, is_correct)
            
            if is_correct:
                messagebox.showinfo("Correct!", "You selected the correct answers!")
            else:
                correct_answer = ", ".join(question["answer"])
                messagebox.showwarning("Incorrect!", f"The correct answers were: {correct_answer}")
            
            # Avançar para a próxima questão
            self.current_question_index += 1
            self.load_question()
        else:
            messagebox.showwarning("No Answer Selected", "Please select at least one answer before proceeding.")

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showwarning("Time's up!", "You ran out of time for this question.")
            self.current_question_index += 1
            self.load_question()

# Função principal
if __name__ == "__main__":
    # Pasta contendo os arquivos de texto
    folder_path = "output_texts"  # Substitua pelo caminho da pasta contendo os arquivos txt
    
    # Carregar perguntas
    questions = load_questions_from_files(folder_path)
    if not questions:
        print("Nenhuma pergunta encontrada na pasta especificada!")
    else:
        # Iniciar o aplicativo de quiz
        root = tk.Tk()
        app = QuizApp(root, questions)
        root.mainloop()
