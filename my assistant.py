import speech_recognition as sr # recognise speech
import playsound #to play an audio
from gtts import gTTS #Google text to speech
import random
import webbrowser #open browser
import os

class person:
	name = ''
	def setName(self, name):
		self.name = name

def there_exist(terms):
	for term in terms:
		if term in voice_data:
			return True

r = sr.Recognizer() #call a recognizer

#Taking audio as input and convert it as text
def record_audio(ask=False):
	with sr.Microphone() as source: #microphone as source
		if ask:
			speak(ask)
		audio = r.listen(source)#listen for audio via source
		voice_data = ''
		try:
			voice_data = r.recognize_google(audio) #convert audio to text
		except sr.UnknownValueError:#error: recognizer did not understand
			speak('I did not get that')
		except sr.RequestError:
			speak('Sorry, the service is down')#error while recognizer is not connected
		print(f'>> {voice_data.lower()}') #print user input
		return voice_data.lower()

#Get string and make aaudio file to be played
def speak(audio_string):
	tts = gTTS(text = audio_string, lang='en')#text to speech voice
	r=random.randint(1,100)
	audio_file = 'audio' + str(r) + '.mp3' 
	tts.save(audio_file)##save as mp3
	playsound.playsound(audio_file)#play the audio file
	print(f'alexa: {audio_string}')#print what the application said
	os.remove(audio_file)#remove audio file

def respond(voice_data):
	#1: greeting
	if there_exist(['hey', 'hi', 'hello']):
		greetings = [f'hey, how can i help you {person_obj.name}', f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can i help you? {person_obj.name}"] 
		greet = greetings[random.randint(0, len(greetings)-1)]
		speak(greet)

	#2: name
	if there_exist(['what is your name',"what's your name",'tell me your name']):
		if person_obj.name:
			speak('my name is alexa')
		else:
			speak("my name is alexa. what's your name?")

	if there_exist(['my name is']):
		person_name = voice_data.split('is')[-1].strip()
		speak(f"okay, i will remember that {person_name}")
		person_obj.setName(person_name)#remember name of a person

	#3: greeting
	if there_exist(["how are you", "how are you doing"]):
		speak(f"I'm very well, thanks for asking {person_obj.name}")


	#5: search google
	if there_exist(['search for']) and 'youtube' not in voice_data:
		search_term = voice_data.split('for')[-1]
		url = f'https://google.com/search?q={search_term}'
		webbrowser.get().open(url)
		speak(f"Here is what I found for {search_term} on web")

	#6: youtube
	if there_exist(['youtube']):
		search_term = voice_data.split('for')[-1]
		url = f'https://www.youtube.com/results?search_query={search_term}'
		webbrowser.get().open(url)
		speak(f"Here is what I found for {search_term} on youtube")

	if there_exist(['exit','quit','goodbye','bye']):
		speak('going offline')
		exit()

person_obj = person()
while 1:
	voice_data = record_audio()#get the voice data
	respond(voice_data) #respond

