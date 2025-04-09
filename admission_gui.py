#admission bot
import tkinter as tk
from tkinter import scrolledtext
import numpy as np
import pickle
import random
import threading
import speech_recognition as sr
import pyttsx3
import queue

# Load model
with open('C:\\Users\\hp\\Desktop\\admission_bot\\admission_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Initialize TTS engine and queue
engine = pyttsx3.init()
speech_queue = queue.Queue()

def speech_loop():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

speech_thread = threading.Thread(target=speech_loop, daemon=True)
speech_thread.start()

def speak(text):
    speech_queue.put(text)

# Greeting logic
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = [
    "Hello!", "Hey there!", "Hi!", "Greetings! How can I assist you today?",
    "Hello! Ready to check your admission chances?"
]

FIELDS = [
    "GRE Score (out of 340)",
    "TOEFL Score (out of 120)",
    "University Rating (1-5)",
    "Statement of Purpose (1-5)",
    "Letter of Recommendation (1-5)",
    "CGPA (out of 10)",
    "Research Experience (0: No, 1: Yes)"
]

FIELD_VALIDATIONS = [
    lambda x: 0 <= x <= 340,
    lambda x: 0 <= x <= 120,
    lambda x: 1 <= x <= 5,
    lambda x: 1 <= x <= 5,
    lambda x: 1 <= x <= 5,
    lambda x: 0 <= x <= 10,
    lambda x: x in (0, 1)
]

VALIDATION_MESSAGES = [
    "Please enter a valid GRE score (0-340).",
    "Please enter a valid TOEFL score (0-120).",
    "University Rating should be between 1 and 5.",
    "SOP rating should be between 1 and 5.",
    "LOR rating should be between 1 and 5.",
    "Please enter a valid CGPA (0-10).",
    "Research Experience should be 0 (No) or 1 (Yes)."
]

user_inputs = []
current_field = 0

def reset_bot():
    global user_inputs, current_field
    user_inputs = []
    current_field = 0
    response = "You can start a new admission prediction anytime. Just say hi!"
    chatbox.insert(tk.END, f"\nBot: {response}\n")
    speak(response)

def predict_admission(data):
    input_features = np.array([data])
    prediction = model.predict(input_features)
    return prediction[0]

def suggest_universities(chance):
    if chance >= 0.9:
        return "You can aim for top universities like MIT, Stanford, or Harvard."
    elif chance >= 0.7:
        return "You have good chances at universities like Georgia Tech, UCLA, or University of Michigan."
    elif chance >= 0.5:
        return "Consider applying to SUNY Buffalo, ASU, or University of Illinois Chicago."
    else:
        return "Try safer options like NJIT, University of Texas Arlington, or CSU Long Beach."

def bot_response(msg):
    global current_field, user_inputs

    msg = msg.lower().strip()

    if current_field == 0 and any(word in msg for word in GREETING_INPUTS):
        response = random.choice(GREETING_RESPONSES)
        chatbox.insert(tk.END, f"Bot: {response}\n")
        speak(response)
        prompt = f"Let's begin. Please enter your {FIELDS[current_field]}:"
        chatbox.insert(tk.END, f"Bot: {prompt}\n")
        speak(prompt)
        current_field += 1

    elif 1 <= current_field <= len(FIELDS):
        try:
            value = float(msg) if current_field != len(FIELDS) else int(msg)

            if not FIELD_VALIDATIONS[current_field - 1](value):
                chatbox.insert(tk.END, f"Bot: {VALIDATION_MESSAGES[current_field - 1]}\n")
                speak(VALIDATION_MESSAGES[current_field - 1])
                chatbox.insert(tk.END, f"Bot: Please enter your {FIELDS[current_field - 1]} again:\n")
                speak(f"Please enter your {FIELDS[current_field - 1]} again")
                return

            user_inputs.append(value)

            if current_field < len(FIELDS):
                prompt = f"Please enter your {FIELDS[current_field]}:"
                chatbox.insert(tk.END, f"Bot: {prompt}\n")
                speak(prompt)
                current_field += 1
            else:
                chance = predict_admission(user_inputs)
                chance_percentage = min(chance * 100, 100)
                result = f"Your predicted chance of admission is {chance_percentage:.2f}%"
                suggestion = suggest_universities(chance)
                chatbox.insert(tk.END, f"Bot: {result}\n")
                speak(result)
                chatbox.insert(tk.END, f"Bot: {suggestion}\n")
                speak(suggestion)
                prompt = "Would you like to try again? (yes/no)"
                chatbox.insert(tk.END, f"Bot: {prompt}\n")
                speak(prompt)
                current_field += 1

        except ValueError:
            error_msg = f"Invalid input. Please enter a numeric value for {FIELDS[current_field - 1]}."
            chatbox.insert(tk.END, f"Bot: {error_msg}\n")
            speak(error_msg)
            chatbox.insert(tk.END, f"Bot: Please enter your {FIELDS[current_field - 1]} again:\n")
            speak(f"Please enter your {FIELDS[current_field - 1]} again")

    elif current_field == len(FIELDS) + 1:
        if "yes" in msg:
            user_inputs = []
            current_field = 1
            greeting = "Great! Let's begin again."
            chatbox.insert(tk.END, f"Bot: {greeting}\n")
            speak(greeting)
            prompt = f"Please enter your {FIELDS[0]}:"
            chatbox.insert(tk.END, f"Bot: {prompt}\n")
            speak(prompt)
        elif "no" in msg:
            goodbye = "Okay! Have a great day!"
            chatbox.insert(tk.END, f"Bot: {goodbye}\n")
            speak(goodbye)
            reset_bot()
        else:
            retry_msg = "Please answer with 'yes' or 'no'."
            chatbox.insert(tk.END, f"Bot: {retry_msg}\n")
            speak(retry_msg)

    else:
        default_msg = "I'm here to help with admission prediction. Say 'hi' to start!"
        chatbox.insert(tk.END, f"Bot: {default_msg}\n")
        speak(default_msg)

def send_message():
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return
    chatbox.insert(tk.END, f"You: {user_msg}\n")
    bot_response(user_msg)
    user_input.delete(0, tk.END)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chatbox.insert(tk.END, "🎤 Listening...\n")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            chatbox.insert(tk.END, f"You (via voice): {query}\n")
            user_input.delete(0, tk.END)
            user_input.insert(0, query)
            send_message()
        except sr.WaitTimeoutError:
            msg = "Didn't catch that. Please speak again."
            chatbox.insert(tk.END, f"Bot: {msg}\n")
            speak(msg)
        except sr.UnknownValueError:
            msg = "Sorry, I didn't understand that."
            chatbox.insert(tk.END, f"Bot: {msg}\n")
            speak(msg)

# GUI Setup
root = tk.Tk()
root.title("Admission ChatBot")
root.geometry("580x670")
root.config(padx=10, pady=10)

chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25, font=("Helvetica", 11))
chatbox.pack(pady=10)
welcome = "Hi! I'm your admission assistant bot. Say 'hi' to get started!"
chatbox.insert(tk.END, f"Bot: {welcome}\n")
speak(welcome)

user_input = tk.Entry(root, font=("Helvetica", 13))
user_input.pack(fill=tk.X, pady=5)
user_input.focus()

button_frame = tk.Frame(root)
button_frame.pack()

send_btn = tk.Button(button_frame, text="Send", command=send_message, bg="green", fg="white", padx=10, pady=5)
send_btn.grid(row=0, column=0, padx=5)

exit_btn = tk.Button(button_frame, text="Exit", command=lambda: [speech_queue.put(None), root.destroy()], bg="red", fg="white", padx=10, pady=5)
exit_btn.grid(row=0, column=1, padx=5)

voice_btn = tk.Button(button_frame, text="🎙️ Voice", command=listen, bg="blue", fg="white", padx=10, pady=5)
voice_btn.grid(row=0, column=2, padx=5)

root.bind('<Return>', lambda event: send_message())
root.mainloop()
