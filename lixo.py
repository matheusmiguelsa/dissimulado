import os

f = open("data.txt", "r", encoding='utf8')
text = f.read()
text = text.split('Question ')

for c in range(0, 40):
    f = open(f"output_texts_3/frame_{c}.txt", "w", encoding='utf8')
    
    f.write(text[c])
    f.close()