from whisper_mic import WhisperMic 
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pyttsx3
import re 
import webbrowser


load_dotenv()
engine = pyttsx3.init()
engine.setProperty('rate', 200)

genai.configure(api_key="")
model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest')
his= model.start_chat(history=[])

def get_gemimi_response(res) :
    try:
        response = his.send_message(res , stream=True)
        
        text_buf = ""
        sen_buf = ""
        

        for i in response:
            if not i.text:
                continue
                

            text_buf += i.text
            sen_buf += i.text
            
            if any(char in sen_buf for char in ['.', '!', '?', ',', ';', ':', '\n']):
                print(f"Assistant: {sen_buf}", end='', flush=True)
                
                
                engine.say(sen_buf)
                engine.runAndWait()

                sentence_buffer = ""
                
        if sen_buf:
            print(f"Assistant: {sen_buf}")
            engine.say(sen_buf)
            engine.runAndWait()
            
        return text_buf
    except Exception as e:
        print(f"Error in streaming response: {e} ")
        return "Sorry, I encountered an error. "

def response_audio(res):
    try:
        result= get_gemimi_response(res)
        print("Assistant:",result)
        engine.say(result)
        engine.runAndWait()

    except Exception as e:
        print(f"Error occured while skeaping! ")
        return "Error Occured. "


def google_search(res):
    srh_pattern = re.compile(r'(search|look|find|google)(?:\s+for)?\s+(.*)', re.IGNORECASE)

    url_pattern = re.compile(r'(open|visit|go to|browse)\s+(http?://[^\s]+|www\.[^\s]+[a-zA-Z0-9-]+\.(com|in|org|net|io|gov|edu))', re.IGNORECASE)

    goo_search = srh_pattern.search(res)

    if goo_search :
        search = goo_search.group(2).strip()
        if search :
            searches = f"https://www.google.com/search?q={search.replace(' ','+')}"
            engine.say("Searching for ",search)
            engine.runAndWait()
            webbrowser.open(searches)
            return True , f"I've Searched for {search}"
        
    url_search = url_pattern.search(res)

    if url_search :
        find = url_search.group(2).strip()
        if not find.startswith("http"):
            if find.startswith("www"):
                find = "https://" + find
            else :
                find = "https://www." + find
        
        engine.say(f"Opening {find}")
        engine.runAndWait()
        webbrowser.open(find)
        return True , f"I've Opended {find} for you. "
    return False, ""


mic = WhisperMic()
results=mic.listen()
while True:
    if results =="Hello JARVIS" or "Hi JARVIS":
        result = mic.listen(timeout=5.0)
        res= result
        print("You",res)
        google_search(res)
        get_gemimi_response(res)

        continue 




