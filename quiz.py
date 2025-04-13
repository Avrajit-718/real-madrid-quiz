import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import pygame
import os
import random
import webbrowser

# Initialize window
window = tk.Tk()
window.title("Real Madrid Quiz")
window.geometry("800x600")
window.configure(bg="black")
window.minsize(600, 500)

# Play background music
pygame.mixer.init()
if os.path.exists("hala_madrid.mp3"):
    pygame.mixer.music.load("hala_madrid.mp3")
    pygame.mixer.music.play(-1)

# Global constants and variables
LEADERBOARD_FILE = "leaderboard.txt"
QUESTIONS_FILE = "questions.txt"
MAX_QUESTIONS = 10
username = ""
questions = []
score = 0
current_q = 0
leaderboard_entries = []

# Load and resize background
original_bg_image = Image.open("background.jpg")
bg_photo = ImageTk.PhotoImage(original_bg_image.resize((800, 600)))
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Frame containers
home_frame = tk.Frame(window, bg="black")
quiz_frame = tk.Frame(window, bg="black")

# --- Helper Functions ---
def resize_bg(event):
    new_width, new_height = event.width, event.height
    resized = original_bg_image.resize((new_width, new_height))
    new_bg = ImageTk.PhotoImage(resized)
    bg_label.config(image=new_bg)
    bg_label.image = new_bg

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as file:
        lines = file.readlines()
    entries = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 2 and parts[1].isdigit():
            entries.append((parts[0], parts[1]))
    return entries

def save_leaderboard(entries):
    with open(LEADERBOARD_FILE, "w") as file:
        for name, score in entries:
            file.write(f"{name},{score}\n")

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        return []
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
    qs = []
    for block in blocks:
        parts = block.strip().split("\n")
        if len(parts) == 6:
            qs.append({"question": parts[0], "options": parts[1:5], "answer": parts[5]})
    return qs

def save_question_to_file(question_dict):
    with open(QUESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{question_dict['question']}\n")
        for opt in question_dict['options']:
            f.write(f"{opt}\n")
        f.write(f"{question_dict['answer']}\n\n")

def open_news():
    webbrowser.open("https://www.realmadrid.com/en/news")

def show_about():
    messagebox.showinfo("About Real Madrid", "Real Madrid Club de Fútbol is a professional football club based in Madrid, Spain. Founded in 1902, it is widely regarded as one of the greatest football clubs in the world, with a record number of Champions League titles and La Liga victories.")

# --- Home Page ---
def show_home():
    quiz_frame.pack_forget()
    home_frame.pack(expand=True, fill="both")
    leaderboard_box.config(state="normal")
    leaderboard_box.delete("1.0", tk.END)
    leaderboard_box.config(state="disabled")
    result_label.config(text="")

def start_quiz():
    global username, questions, score, current_q, leaderboard_entries
    username = simpledialog.askstring("Username", "Enter your name:") or "Anonymous"
    questions = load_questions()
    random.shuffle(questions)
    questions = questions[:MAX_QUESTIONS]
    score = 0
    current_q = 0
    leaderboard_entries = load_leaderboard()
    home_frame.pack_forget()
    quiz_frame.pack(expand=True, fill="both")
    load_question()

# --- Admin ---
def admin_add_question():
    pw = simpledialog.askstring("Admin Access", "Enter admin password:", show="*")
    if pw == "admin123":
        question = simpledialog.askstring("New Question", "Enter the question:")
        options = [simpledialog.askstring("Option", f"Enter option {i+1}:") for i in range(4)]
        answer = simpledialog.askstring("Answer", "Enter the correct answer exactly:")
        if question and answer and all(options):
            save_question_to_file({"question": question, "options": options, "answer": answer})
            messagebox.showinfo("Added", "New question added! Restart the app to see changes.")

# --- Quiz Functions ---
def load_question():
    global current_q
    if current_q < len(questions):
        q = questions[current_q]
        question_label.config(text=q["question"])
        for i, opt in enumerate(q["options"]):
            option_buttons[i].config(text=opt, command=lambda selected=opt: check_answer(selected))
    else:
        show_result()

def check_answer(selected):
    global score, current_q
    correct = questions[current_q]["answer"]
    if selected == correct:
        score += 1
        result_label.config(text="✅ Correct!")
    else:
        result_label.config(text=f"❌ Wrong! Correct: {correct}")
    score_label.config(text=f"Score: {score}")
    current_q += 1
    window.after(1000, load_question)

def update_leaderboard():
    global leaderboard_entries
    leaderboard_entries.append((username, str(score)))
    leaderboard_entries = sorted(leaderboard_entries, key=lambda x: int(x[1]), reverse=True)[:10]
    save_leaderboard(leaderboard_entries)
    leaderboard_text = "\n".join([f"{i+1}. {name}: {scr}" for i, (name, scr) in enumerate(leaderboard_entries)])
    leaderboard_box.config(state="normal")
    leaderboard_box.delete("1.0", tk.END)
    leaderboard_box.insert(tk.END, leaderboard_text)
    leaderboard_box.config(state="disabled")

def show_result():
    question_label.config(text="Quiz Complete! 💯")
    for btn in option_buttons:
        btn.grid_remove()
    result_label.config(text=f"Final Score: {score}/{len(questions)}")
    leaderboard_label.grid(row=9, column=0, columnspan=2, pady=(10, 5))
    leaderboard_scroll_frame.grid(row=10, column=0, columnspan=2)
    update_leaderboard()
    back_btn.grid(row=11, column=0, columnspan=2, pady=10)

# --- Home Frame UI ---
home_title = tk.Label(home_frame, text="Real Madrid Quiz ⚽", font=("Helvetica", 28, "bold"), fg="gold", bg="black")
home_title.pack(pady=20)

logo_home = Image.open("logo.png").resize((100, 100))
logo_home_photo = ImageTk.PhotoImage(logo_home)
logo_home_label = tk.Label(home_frame, image=logo_home_photo, bg="black")
logo_home_label.pack(pady=5)

start_btn = tk.Button(home_frame, text="Start Quiz", command=start_quiz, font=("Arial", 14), bg="#f7f7f7", width=20)
admin_btn = tk.Button(home_frame, text="Admin Mode", command=admin_add_question, font=("Arial", 14), bg="gray", width=20)
about_btn = tk.Button(home_frame, text="About Real Madrid", command=show_about, font=("Arial", 14), bg="blue", fg="white", width=20)
news_btn = tk.Button(home_frame, text="News Feed", command=open_news, font=("Arial", 14), bg="green", fg="white", width=20)

start_btn.pack(pady=10)
admin_btn.pack(pady=10)
about_btn.pack(pady=10)
news_btn.pack(pady=10)


quiz_frame.columnconfigure(0, weight=1)
quiz_frame.columnconfigure(1, weight=1)

logo_image = Image.open("logo.png").resize((80, 80))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(quiz_frame, image=logo_photo, bg="black")
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

title_label = tk.Label(quiz_frame, text="Real Madrid Quiz ⚽", font=("Arial", 18, "bold"), fg="white", bg="black")
title_label.grid(row=1, column=0, columnspan=2, pady=10)

score_label = tk.Label(quiz_frame, text="Score: 0", font=("Arial", 14), fg="white", bg="black")
score_label.grid(row=2, column=0, columnspan=2, pady=5)

question_frame = tk.Frame(quiz_frame, bg="black")
question_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
question_label = tk.Label(question_frame, text="", wraplength=600, font=("Arial", 13), fg="white", bg="black")
question_label.pack(fill="x")

option_buttons = []
for i in range(4):
    btn = tk.Button(quiz_frame, text="", width=50, font=("Arial", 11), bg="white", fg="black")
    btn.grid(row=4+i, column=0, columnspan=2, pady=5)
    option_buttons.append(btn)

result_label = tk.Label(quiz_frame, text="", font=("Arial", 12), fg="white", bg="black")
result_label.grid(row=8, column=0, columnspan=2, pady=10)

leaderboard_label = tk.Label(quiz_frame, text="Leaderboard:", font=("Arial", 12, "bold"), fg="gold", bg="black")
leaderboard_scroll_frame = tk.Frame(quiz_frame, bg="black")
scrollbar = tk.Scrollbar(leaderboard_scroll_frame, orient="vertical")
leaderboard_box = tk.Text(leaderboard_scroll_frame, height=5, width=50, font=("Arial", 11), fg="white", bg="black", yscrollcommand=scrollbar.set)
scrollbar.config(command=leaderboard_box.yview)
scrollbar.pack(side="right", fill="y")
leaderboard_box.pack(side="left", fill="both")
leaderboard_box.config(state="disabled")

back_btn = tk.Button(quiz_frame, text="Back to Home", command=show_home, font=("Arial", 11), bg="white")


home_frame.pack(expand=True, fill="both")
window.bind('<Configure>', resize_bg)
window.mainloop()
