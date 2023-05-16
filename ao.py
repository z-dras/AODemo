from gtts import gTTS
import speech_recognition as sr
import json
from pathlib import Path
from playsound import playsound
import sys
import os
from enum import Enum

class Mode(Enum):
    Trivia = 0
    Book = 1

r = sr.Recognizer()

class TriviaPack:
   name = ""
   questions = []
   score = 0
   def __init__(self, n):
      name = n
      id = 0
      while(True):
         try:
            with open(f'{name}/question-{id}.txt', 'r') as f:
               lines = f.readlines()
               question_content = ""
               for line in lines:
                  question_content += " " + line
         except FileNotFoundError:
            break
         # TODO: make sure this allowed to be empty
         try:
            with open(f'{name}/answers-{id}.txt', 'r') as f:
               lines = f.readlines()
               answers = ""
               for line in lines:
                  answers += " " + line
         except FileNotFoundError:
            break

         try:
            with open(f'{name}/correct-{id}.txt', 'r') as f:
               correct = f.readline().strip()
         except FileNotFoundError:
            break

         self.questions.append(TriviaQuestion(id, question_content, answers, correct))
         id += 1

   def play_game(self):
      current_id = 0
      while(current_id < len(self.questions)):
         current = self.questions[current_id]
         playsound(f"{current.mp3_content}")
         playsound(f"{current.mp3_answers}")
         with sr.Microphone() as source:
            # read the audio data from the default microphone
            r.adjust_for_ambient_noise(source)
            audio_data = r.listen(source)
            # TODO make this not crash if empty
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_google(audio_data, language='en', show_all=True)
            print(text)
            answers = text['alternative']
            for ans in answers:
               if str(ans['transcript']) == current.correct_ans:
                  current.got_correct = True
            current_id += 1

      for q in self.questions:
         if q.got_correct:
            self.score += 1

      speech = gTTS(text=f"Your score is {self.score}. Good job!", lang='en', slow=False)
      speech.save(f"{name}/score.mp3")
      playsound(f"{name}/score.mp3")
      os.remove(f"{name}/score.mp3")
      
      
class TriviaQuestion:
   id = -1
   correct_ans = ""
   question_content = ""
   answer_choices = ""
   mp3_content = ""
   mp3_answers = ""
   got_correct = False

   def __init__(self, i, q, a, c):
      self.id = i
      self.question_content = q
      self.answer_choices = a
      self.correct_ans = c
      self.mp3_content = f"{name}/question_{self.id}.mp3" 
      self.mp3_answers = f"{name}/answers_{self.id}.mp3"
      # TODO accept more languages!!!
      if not Path(self.mp3_content).is_file():
        speech = gTTS(text=self.question_content, lang='en', slow=False)
        speech.save(self.mp3_content)
      if not Path(self.mp3_answers).is_file():
        prompt = gTTS(text=self.answer_choices, lang='en', slow=False)
        prompt.save(self.mp3_answers)

class AudioBook:
   name = ""
   segments = []
   
   def __init__(self, n):
      name = n
      id = 0
      while(True):
         try:
            with open(f'{name}/content-{id}.txt', 'r') as f:
               lines = f.readlines()
               content = ""
               for line in lines:
                  content += " " + line
         except FileNotFoundError:
            break
         try:
            with open(f'{name}/mapping-{id}.json', 'r') as f:
               mapping = json.load(f)
         except FileNotFoundError:
            mapping = {}

         try:
            with open(f'{name}/prompt-{id}.txt', 'r') as f:
               lines = f.readlines()
               prompt = ""
               for line in lines:
                  prompt += " " + line
         except FileNotFoundError:
            prompt = ""

         self.segments.append(AudioBookSegment(id, mapping, content, prompt))
         id += 1

   def play_book(self):
      current_id = 0
      while(current_id != -1):
            current = self.segments[current_id]
            playsound(f"{current.mp3_content}")
            found = False
            while(not found):
               if current.next_id_table == {}:
                  break
               playsound(f"{current.mp3_prompt}")
               with sr.Microphone() as source:
                  # read the audio data from the default microphone
                  r.adjust_for_ambient_noise(source)
                  audio_data = r.listen(source)
                  print("Recognizing...")
                  # convert speech to text
                  text = r.recognize_google(audio_data, language='en', show_all=True)
                  print(text)
                  if text != []:
                     for option in text['alternative']:
                        st = option['transcript']
                        if str(st) in current.next_id_table:
                              current_id = int(current.next_id_table[st])
                              found = True
                              break
         
class AudioBookSegment:
   id = -1
   next_id_table = {}
   content = ""
   # TODO set up an option for an exmpty prompt ie end state
   prompt = ""
   mp3_content = ""
   mp3_prompt = ""

   def __init__(self, i, t, c, p):
      self.id = i
      self.next_id_table = t
      self.prompt = p 
      self.content = c
      self.mp3_content = f"{name}/content_{self.id}.mp3" 
      self.mp3_prompt = f"{name}/prompt_{self.id}.mp3"
      # TODO accept more languages!!!
      if not Path(self.mp3_content).is_file():
        speech = gTTS(text=self.content, lang='en', slow=False)
        speech.save(self.mp3_content)
      if not Path(self.mp3_prompt).is_file() and self.prompt != "":
        prompt = gTTS(text=self.prompt, lang='en', slow=False)
        prompt.save(self.mp3_prompt)

# usage ./ao <mode> <name>
# mode = "book" ('b') or "trivia" "t"

mode = ""
try:
   mode = sys.argv[1]
except:
   print("Missing required argument mode. See README for more details")
   exit(1)

name = ""
try:
   name = sys.argv[2]
except:
   print("Missing required argument audio book/trivia pack name. See README for more details")
   exit(1)

if mode == 'b' or mode == "book":
   mode = Mode.Book
else:
   mode = Mode.Trivia

if mode == Mode.Book:
   book = AudioBook(name)
   book.play_book()
else:
   trivia = TriviaPack(name)
   trivia.play_game()