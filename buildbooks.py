from gtts import gTTS
import speech_recognition as sr
from pathlib import Path
from playsound import playsound
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
                    # TODO loop over these and try them all before giving up
                    text = text['alternative'][0]['transcript']
                    if text in current.next_id_table:
                        current_id = int(current.next_id_table[text])
                        print(current_id)
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
      if not Path(self.mp3_content).is_file():
        speech = gTTS(text=self.content, lang='en', slow=False)
        speech.save(f"content_{self.id}.mp3")
      if not Path(self.mp3_prompt).is_file():
        prompt = gTTS(text=self.prompt, lang='en', slow=False)
        prompt.save(f"prompt_{self.id}.mp3")


startSeg = AudioBookSegment(
                            0, 
                            {"1": "1", "2":"2"},
                            "You arrive at a fork in the road. On the right you see sparkling sun and blue sky over a well trodden dirt road. The left fork is truly the road less traveled, it has green overgrowth that winds and bends and casts a dark shadow over the path.",
                            "Which path would you like to take: 1) the right path 2) the left path")
oneSeg = AudioBookSegment(1, 
                            {"1": "-1", "2":"-1"},
                            "You continue down the sunny path, admiring the glowing  natural beauty all around. Eventually you come to a clearing with a large log cabin in the middle.",
                            "Which path would you like to take: 1) the right path 2) the left path")
twoSeg = AudioBookSegment(2,
                          {"1": "-1", "2":"-1"},
                          "You weave down the path less traveled, being careful not to trip on any of the large tree roots that line the path. Suddenly you hear a loud bang.",
                          "Would you like to 1) investigate the source of the noise or 2) run the other direction.")

testBook = AudioBook("Test", 0, [startSeg, oneSeg, twoSeg])
testBook.play_book()
   


