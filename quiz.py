import tkinter as tk
from tkinter import messagebox
import random
import os

QUESTIONS = [
    {
        "question": "You start building a space-explorer game and need to store the player's current shield level (100) and their ship's callsign (\"Nova-7\"). Which pair of data types fits best?",
        "choices": [
            "A. Integer and string",
            "B. Boolean and float",
            "C. List and integer",
            "D. String and boolean"
        ],
        "answer": "A"
    },
    {
        "question": "A player picks up a \"25\" shield boost from a crate, where \"25\" was accidentally read as text. You want to add 25 to shield = 100 so it becomes 125, not \"10025\". What operation must happen first?",
        "choices": [
            "A. String slicing",
            "B. Type conversion to integer",
            "C. Rounding to float",
            "D. String reversal"
        ],
        "answer": "B"
    },
    {
        "question": "Next, you code the warp-drive check: a ship can jump to hyperdrive only if fuel > 50 AND engineHealthy == true. Which logical operator requires both conditions to hold?",
        "choices": [
            "A. Logical OR",
            "B. Logical NOT",
            "C. Logical AND",
            "D. Modulo operator"
        ],
        "answer": "C"
    },
    {
        "question": "During a level-up sequence, you want to award 10 bonus points for each of the 5 stars collected in a stage. Which control structure is cleanest for repeating that reward step a known number of times?",
        "choices": [
            "A. A counted for loop",
            "B. An if/else branch",
            "C. A return statement",
            "D. A break statement"
        ],
        "answer": "A"
    },
    {
        "question": "You notice you are writing the exact same damage-calculation formula in enemy lasers, meteor hits, and acid pools. How should you organize that shared logic?",
        "choices": [
            "A. Duplicate it in every file",
            "B. Store it in a comment",
            "C. Extract a reusable function",
            "D. Use a sleep timer"
        ],
        "answer": "C"
    },
    {
        "question": "Your ship's cargo hold stores collected artifacts in order: cargo = [\"Map\", \"Battery\", \"Core\"]. What expression accesses the very first item without removing it?",
        "choices": [
            "A. cargo[1]",
            "B. cargo[0]",
            "C. cargo.last()",
            "D. cargo[-0]"
        ],
        "answer": "B"
    },
    {
        "question": "As the game grows, each upgrade has both a name and a cost (for example, name: \"Thrusters\" and cost: 250). Which data structure best groups named properties together?",
        "choices": [
            "A. An object or dictionary",
            "B. A boolean flag",
            "C. A single character",
            "D. A raw byte"
        ],
        "answer": "A"
    },
    {
        "question": "A player tries to buy an upgrade using a save file that was corrupted on disk. Instead of crashing the whole game, what technique lets you catch the bad data and show a friendly message?",
        "choices": [
            "A. Infinite loop",
            "B. Exception handling",
            "C. Bitwise shift",
            "D. Hardcoding defaults"
        ],
        "answer": "B"
    },
    {
        "question": "In the leaderboard feature, a player enters \"  AcePilot  \" with extra spaces, and you want to store a clean username without leading or trailing whitespace. Which operation does that?",
        "choices": [
            "A. Converting to uppercase",
            "B. Splitting into words",
            "C. Trimming whitespace",
            "D. Padding with zeros"
        ],
        "answer": "C"
    },
    {
        "question": "Finally, you want the player's high score and unlocked ship to still be there after they close and reopen the browser tab. Where should that data be saved?",
        "choices": [
            "A. Temporary local variable",
            "B. Persistent storage",
            "C. CPU register",
            "D. Uninitialized memory"
        ],
        "answer": "B"
    }
]

TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

BG_COLOR = "#111111"
PRIMARY_COLOR = "#3DAAFF"
CORRECT_COLOR = "#2E7D32"
WRONG_COLOR = "#C62828"

root = tk.Tk()
root.title("Advanced Quiz Application")
root.geometry("700x640")
root.resizable(False, False)
root.configure(bg="#111111")

# QUIZ STATE VARIABLES
quiz_questions = []      # shuffled copy of the questions
current_question = 0     # index of the current question
score = 0
time_left = TIME_LIMIT
wrong_answers = []       # details of incorrect answers (for the review)
timer_job = None         # id of the scheduled timer, needed to cancel it
answered = False         # True after the question is submitted
selected_answer = tk.StringVar()   # holds the chosen letter

# Widgets that are updated while the quiz is running
timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=30, pady=20)

# HIGH SCORE FUNCTIONS (file handling)
def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0

def save_high_score(new_score):
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False

def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

def get_choice_text(question, letter):
    """Return the full choice text (for example 'B. def') from a letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"

def start_quiz():
    global quiz_questions, current_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()

def show_start_screen():
    clear_screen()
    tk.Label(main_frame, text="Python Basics Quiz",
             font=("Arial", 28, "bold"),
             bg=BG_COLOR, fg=PRIMARY_COLOR).pack(pady=(60, 10))
    tk.Label(main_frame,
             text=f"{len(QUESTIONS)} questions  |  {TIME_LIMIT} seconds per question",
             font=("Arial", 13), bg=BG_COLOR, fg="white").pack(pady=5)
    tk.Label(main_frame,
             text=f"High Score: {get_high_score()} / {len(QUESTIONS)}",
             font=("Arial", 16, "bold"), bg=BG_COLOR, fg="white").pack(pady=20)
    tk.Button(main_frame, text="Start Quiz", font=("Arial", 16, "bold"),
              bg=PRIMARY_COLOR, fg="white", width=15,
              command=start_quiz).pack(pady=20)

def show_question():
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons

    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]

    # Progress and timer
    top_frame = tk.Frame(main_frame, bg=BG_COLOR)
    top_frame.pack(fill="x")
    tk.Label(
        top_frame,
        text=f"Question {current_question + 1} of {len(quiz_questions)}",
        font=("Arial", 13, "bold"),
        bg=BG_COLOR,
        fg="white"
        ).pack(side="left")

    timer_label = tk.Label(
        top_frame,
        text="",
        font=("Arial", 13, "bold"),
        bg=BG_COLOR,
        fg="white"
    )
    timer_label.pack(side="right")

    tk.Label(
        main_frame,
        text=f"Score: {score}",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg="white"
        ).pack(anchor="w", pady=(5, 0))

    # Question text
    tk.Label(main_frame, text=question["question"],
             font=("Arial", 18, "bold"), wraplength=620, justify="left",
             bg=BG_COLOR, fg="white").pack(pady=25, anchor="w")

    # Answer choices (the value of each button is its letter)
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        button = tk.Radiobutton(
            main_frame,
            text=choice,
            variable=selected_answer,
            value=letter,
            tristatevalue="__unset__",
            font=("Arial", 14),
            bg=BG_COLOR,
            fg="white",
            selectcolor="#222222",
            activebackground=BG_COLOR,
            anchor="w"
        )
        button.pack(fill="x", pady=4)
        choice_buttons.append(button)

    feedback_label = tk.Label(
        main_frame,
        text="",
        font=("Arial", 13, "bold"),
        bg=BG_COLOR,
        fg="white",
        wraplength=620
    )
    feedback_label.pack(pady=15)

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack()
    submit_button = tk.Button(button_frame, text="Submit Answer",
                              font=("Arial", 13, "bold"), bg=PRIMARY_COLOR,
                              fg="white", width=15, command=submit_answer)
    submit_button.pack(side="left", padx=10)

    last_question = current_question == len(quiz_questions) - 1
    next_button = tk.Button(button_frame,
                            text="See Results" if last_question else "Next Question",
                            font=("Arial", 13, "bold"), width=15,
                            state="disabled", command=next_question)
    next_button.pack(side="left", padx=10)

    update_timer()

def update_timer():
    global time_left, timer_job
    if answered:
        return
    timer_label.config(text=f"Time left: {time_left}s")
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)

def stop_timer():
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)   # cancels the scheduled call
        timer_job = None

def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")

def submit_answer():
    global score, answered
    if answered:
        return
    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="Correct!", fg=CORRECT_COLOR)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, question["answer"])
        })
        feedback_label.config(text="Wrong!", fg=WRONG_COLOR)

    next_button.config(state="normal")

def time_up():
    """Called when the timer reaches zero."""
    global answered
    if answered:
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": get_choice_text(question, question["answer"])
    })
    feedback_label.config(
        text="Time is up! Correct answer: "
             + get_choice_text(question, question["answer"]),
        fg=WRONG_COLOR
    )
    next_button.config(state="normal")

def next_question():
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()

def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        message = "Excellent work!"
    elif percentage >= 70:
        message = "Good job!"
    elif percentage >= 50:
        message = "Not bad. Keep practicing!"
    else:
        message = "Review the topic and try again."

    tk.Label(main_frame, text="Quiz Complete!", font=("Arial", 26, "bold"),
             bg=BG_COLOR, fg=PRIMARY_COLOR).pack(pady=(10, 5))
    tk.Label(main_frame, text=f"Score: {score} / {total}  ({percentage:.0f}%)",
             font=("Arial", 18, "bold"), bg=BG_COLOR, fg="white").pack()
    tk.Label(main_frame, text=message, font=("Arial", 14),
             bg=BG_COLOR, fg="white").pack(pady=3)

    record_text = "New high score!" if new_record else f"High Score: {get_high_score()} / {total}"
    tk.Label(main_frame, text=record_text, font=("Arial", 13, "bold"),
             bg=BG_COLOR, fg=CORRECT_COLOR).pack(pady=3)

    tk.Label(main_frame, text="Answer Review (incorrect answers)",
             font=("Arial", 13, "bold"), bg=BG_COLOR, fg="white").pack(pady=(10, 3), anchor="w")

    review_frame = tk.Frame(main_frame, bg=BG_COLOR)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, height=10, wrap="word",
                         font=("Arial", 11), yscrollcommand=scrollbar.set)
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "Perfect! You answered every question correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")
    review_box.config(state="disabled")

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=15)
    tk.Button(button_frame, text="Restart Quiz", font=("Arial", 13, "bold"),
              bg=PRIMARY_COLOR, fg="white", width=15,
              command=restart_quiz).pack(side="left", padx=10)
    tk.Button(button_frame, text="Exit", font=("Arial", 13, "bold"),
              width=15, command=on_close).pack(side="left", padx=10)

def restart_quiz():
    start_quiz()  # reshuffles questions and resets score

def on_close():
    stop_timer()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)   # stop the timer when the window closes
show_start_screen()
root.mainloop()