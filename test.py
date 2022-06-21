from gtts import gTTS
import os
 
text = "メールが届きました"
 
tts = gTTS(text=text, lang="ja") # 日本語
tts.save("temp.wav")
os.system("temp.wav")