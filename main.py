from whisper_mic import WhisperMic 
import google.generativeai as genai
from dotenv import load_dotenv
import os




load_dotenv()

genai.configure(api_key="")
model = genai.GenerativeModel(model_name='gemini-2.5-pro-latest')
his= model.start_chat(history=[])

def get_gemimi_response(res) :
    his.send_message(res)
    gemini_reply = his.last.text
    print("Assistent",gemini_reply)
    return gemini_reply



mic = WhisperMic()
results=mic.listen()
while True:
    if results =="Hello JARVIS" or "Hi JARVIS":
        result = mic.listen(timeout=5.0)
        print("Listning to you ...")
        res= result
        print("You",res)
        get_gemimi_response(res)
        continue 




