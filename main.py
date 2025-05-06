from whisper_mic import WhisperMic 
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pyttsx3


load_dotenv()
engine = pyttsx3.init()

genai.configure(api_key="s")
model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest')
his= model.start_chat(history=[])

def get_gemimi_response(res) :
    his.send_message(res)
    gemini_reply = his.last.text
   # print("Assistent",gemini_reply)
    return gemini_reply


def response_audio(res):
    result= get_gemimi_response(res)
    engine.say(result)
    engine.runAndWait()



mic = WhisperMic()
results=mic.listen()
while True:
    if results =="Hello JARVIS" or "Hi JARVIS":
        result = mic.listen(timeout=5.0)
        print("Listning to you ...")
        res= result
        print("You",res)
        print("Assistent:",get_gemimi_response(res))
        response_audio(res)
        continue 




