from gtts import gTTS
import speech_recognition as sr
import json
from pathlib import Path
from playsound import playsound
import sys
import os


r = sr.Recognizer()
class AudioBook:
   start_segment = 0 
   name = ""
   segments = {}
   def __init__(self, n, st, segs):
      self.name = n
      self.start_segment = st
      self.segments = segs
    
   def play_book(self):
      current_id = self.start_segment
      while(current_id != -1):
         current = self.segments[current_id]
         playsound(f"{current.mp3_content}")
         while(True):
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
                    found = False
                    for option in text['alternative']:
                     text = option['transcript']
                     if text in current.next_id_table:
                           current_id = int(current.next_id_table[text])
                           found = True
                           break
                     if found:
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
      self.mp3_content = f"content_{self.id}.mp3" 
      self.mp3_prompt = f"prompt_{self.id}.mp3"
      # TODO accept more languages!!!
      if not Path(self.mp3_content).is_file():
        speech = gTTS(text=self.content, lang='en', slow=False)
        speech.save(f"{name}/content_{self.id}.mp3")
      if not Path(self.mp3_prompt).is_file() and self.prompt != "":
        prompt = gTTS(text=self.prompt, lang='en', slow=False)
        prompt.save(f"{name}/prompt_{self.id}.mp3")

name = ""
try:
   name = sys.argv[1]
except:
   print("Missing required argument audio book name. See README for more details")
   exit(1)

id = 0
nodes = []
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
      with open(f'{name}/mapping-{id}.txt', 'r') as f:
        line = f.readline()
        mapping = json.loads(line)
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
   
   print(id, mapping, content, prompt)
   nodes.append(AudioBookSegment(id, mapping, content, prompt))
   id += 1


book = AudioBook(name, 0, nodes)
book.play_book()
   


