import os
from groq import Groq
from gtts import gTTS

import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def speech_to_text(path):
    with open(path, "rb") as f:
        r = client.audio.transcriptions.create(
            file=f, model="whisper-large-v3",
            response_format="verbose_json")
    return r.text, r.language

def translate(text, to_lang):
    r = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user",
                   "content": f"Translate to {to_lang}. Output only the translation:\n{text}"}])
    return r.choices[0].message.content.strip()

def text_to_speech(text, lang_code, filename):
    gTTS(text, lang=lang_code).save(filename)

if __name__ == "__main__":
    tests = [("hindi", "hi", "Hindi"),
             ("tamil", "ta", "Tamil"),
             ("kannada", "kn", "Kannada"),
             ("punjabi", "pa", "Punjabi")]

    for name, code, language in tests:
        text, lang = speech_to_text(name + ".m4a")
        print(name, "| heard:", text)
        print("   English:", translate(text, "English"))
        reply = translate("You may be eligible for PM-KISAN. Keep your land papers ready.", language)
        print("   Reply:", reply)
        text_to_speech(reply, code, "reply_" + code + ".mp3")