import nltk
import pyttsx3
import speech_recognition as sr
from nltk.chat.util import Chat, reflections

# Download NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Text-to-speech setup

engine = pyttsx3.init(driverName='sapi5')  # Use 'sapi5' for Windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  # Change to voices[1].id for female
engine.setProperty('rate', 150)

def speak(text):
    print(f"Chatbot: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... (say something or press Enter to type instead)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        voice_input = recognizer.recognize_google(audio)
        print(f"You (voice): {voice_input}")
        return voice_input.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that. Please try again.")
        return ""
    except sr.RequestError:
        speak("Sorry, I couldn't connect to the speech service.")
        return ""

# Chatbot pairs
pairs = [
    [r"hi|hello|hey", ["Hello! How can I help you today?", "Hi there!"]],
    [r"my name is (.*)", ["Hello %1! Nice to meet you."]],
    [r"(.*) your name?", ["I'm your chatbot!"]],
    [r"how are you?", ["I'm just a bot, but I'm doing great!"]],
    [r"tell me a joke", ["Why don't skeletons fight each other? They don't have the guts!"]],
    [r"(.*) (help|assist) (.*)", ["Sure! How can I assist you with %3?"]],
    [r"bye|exit", ["Goodbye! Have a great day!"]],
    [r"(.*)", ["I'm not sure I understood. Can you rephrase?"]]
]

# Chatbot class
class RuleBasedChatbot:
    def __init__(self, pairs):
        self.chat = Chat(pairs, reflections)

    def respond(self, user_input):
        return self.chat.respond(user_input)

# Create instance
chatbot = RuleBasedChatbot(pairs)

# Chat loop
def chat_with_bot():
    speak("Hello! You can either speak or type. Press Enter with no text to speak.")
    while True:
        user_input = input("You (type or press Enter to speak): ").strip()
        if user_input == "":
            user_input = listen()

        if user_input.lower() in ['exit', 'bye']:
            speak("Goodbye! Talk to you soon.")
            break

        response = chatbot.respond(user_input)
        if response:
            speak(response)
        else:
            speak("I'm sorry, I didn't understand that. Can you say it another way?")

# Run chatbot
chat_with_bot()
