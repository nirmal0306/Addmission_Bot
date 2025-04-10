# 🎓 Admission Prediction ChatBot

Welcome to **Admission Prediction Bot**, your smart assistant for estimating your chances of getting admitted into top universities based on your academic profile. This chatbot uses a trained Machine Learning model to make predictions and even talks to you in real time! 🧠💬

---

## ✨ Features

- 🧠 **ML-powered prediction** based on GRE, TOEFL, CGPA, and more
- 💬 **Interactive chatbot UI** with both text and voice support
- 🔊 **Speech recognition** and **text-to-speech** for real-time interaction
- 🏫 **University suggestions** based on predicted chances
- 🔁 Restart-friendly chat with smart prompts
- 💻 Built with Python and Tkinter

---

# 🛠 How to Run

# 1. Clone or Download the Repository
git clone https://github.com/nirmal0306/Addmission_Bot.git

cd admission-bot


# 2 Install Dependencies
Make sure you have Python installed. Then install the required Python libraries:
pip install numpy tkinter pyttsx3 SpeechRecognition

# 3. Train the ML Model
Run this command to train and save the admission prediction model:
python train_model.py

# 4. Start the Chatbot GUI
Once the model is trained, launch the chatbot interface with:
python admission_gui.py

# 🧪 Input Features
The bot will ask for the following details:

GRE Score (out of 340)

TOEFL Score (out of 120)

University Rating (1-5)

Statement of Purpose (1-5)

Letter of Recommendation (1-5)

CGPA (out of 10)

Research Experience (0: No, 1: Yes)

# 🗣 Example Conversation
You: hi
Bot: Hello! Ready to check your admission chances?
Bot: Please enter your GRE score:
...
Bot: Your predicted chance of admission is 78.45%
Bot: You have good chances at universities like Georgia Tech, UCLA, or University of Michigan.

# 📁 Project Structure
admission-bot/

├── train_model.py       # Trains the ML model

├── admission_gui.py     # GUI with chatbot logic

├── admission_model.pkl  # Saved ML model

├── README.md            # This file

# 🙌 Created By
# Nirmal — making learning fun with Python & AI!

# 💡 Tip for Learners
Explore this project to learn how Machine Learning, GUIs, and real-time speech interaction can work together in Python. This is a great beginner-friendly mini project that combines core concepts with hands-on application!
