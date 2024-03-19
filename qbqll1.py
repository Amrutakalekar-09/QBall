import csv
import random
import pyttsx3
import speech_recognition as sr
from difflib import SequenceMatcher

# read the CSV file and extract questions and possible answers into a dictionary
questions = {}
with open('questionball.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        subject = row['subject']
        question = row['question']
        answer = row['answer']
        possible_answers = row['possible_answers'].split(',')
        questions.setdefault(subject, {}).setdefault(question, {'answer': answer, 'possible_answers': possible_answers})

# initialize TTS engine and STT recognizer
engine = pyttsx3.init()
r = sr.Recognizer()

# define TTS function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# define STT function
def listen():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return None

# start the quiz
print("Welcome to the quiz game!")
speak("Welcome to the quiz game!")

# ask questions and keep track of correct answers
correct_answers = 0
total_questions = 0
subjects = list(questions.keys())
print("Which subject do you want to answer questions for? Say 'history', 'science', 'general knowledge' or 'puzzle.")
speak("Which subject do you want to answer questions for? Say 'history', 'science', 'general knowledge' or 'puzzle.")
chosen_subject = None
while chosen_subject not in subjects:
    chosen_subject = listen()
    if chosen_subject is not None:
        chosen_subject = chosen_subject.lower()
        if chosen_subject not in subjects:
            speak("Sorry, I didn't catch that. Please say 'history', 'science', 'general knowledge' or 'puzzle.")
    else:
        speak("Sorry, I didn't catch that. Please say 'history', 'science', 'general knowledge' or 'puzzle.")


print(f"Okay, let's begin with {chosen_subject}.")
speak(f"Okay, let's begin with {chosen_subject}.")
for question in random.sample(list(questions[chosen_subject].keys()), 5):
    answer = questions[chosen_subject][question]['answer']
    possible_answers = questions[chosen_subject][question]['possible_answers']

    # ask the question in audio form
    print(f"Question: {question}")
    speak(f"Question: {question}")

    # capture the user's response in audio form
    response = None
    while response is None:
        speak("Please speak your answer.")
        response = listen()

    # repeat the question if the user said "sorry" or "repeat"
    while "sorry" in response.lower() or "repeat" in response.lower():
        speak(f"Okay, let me repeat the question: {question}")
        response = listen()

    # provide feedback to the user
    if "don't know" in response.lower() or "i don't know" in response.lower() or "donno" in response.lower():
        print("It's OK ")
        speak("It's OK ")
        print(f"Correct answer is {answer}")
        speak(f"Correct answer is {answer}")
    else:
        matches = [SequenceMatcher(None, response.lower(), ans.lower()).ratio() for ans in possible_answers]
        match_percent = max(matches) * 100
        
        if match_percent >= 70:
            print("Correct!")
            speak("Correct!")
            correct_answers += 1
        else:
            print(f"Incorrect. Your response matched {match_percent:.2f}% of the possible answers.")
            speak(f"Incorrect. Your response matched {match_percent:.2f}% of the possible answers.")
            print(f"Correct answer is {answer}")
            speak(f"Correct answer is {answer}")
        
    total_questions += 1

# display the end result
print(f"You answered {correct_answers} out of {total_questions} questions correctly.")
speak(f"You answered {correct_answers} out of {total_questions} questions correctly.")
print("Thank You")
speak("Thank You")