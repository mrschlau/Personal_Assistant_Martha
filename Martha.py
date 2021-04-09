""" Before running this application, please see the "README.md" for the environment setup, configuration, execution instructions, and more """

""" Import modules """
import speech_recognition as sr # Python's collection of voice recognition APIs (Martha uses Google's Web Speech API) (see https://realpython.com/python-speech-recognition/)
import playsound # Uses speakers (i.e. play *.mp3 files)
from gtts import gTTS # Google's Text To Speech (GTTS) translation API.  A web-less API alternative would be "pyttsx3"
import random # Randomization (i.e. see "Basic Greeting" code block, which picks a random greeting)
import webbrowser # Opens web browser tabs
import yfinance as yf # Yahoo Finance API
import os # Delete system files (i.e. discard old *.mp3 files)
import vonage # Vonage APIs module (i.e. SMS, voice)

""" Initialize variables (FYI - Best security practice would be storing these as privileged system environment variables, but you can assign the values below for simplicity) """
martha_vonage_phone = int("<PROVIDE VALUE>") # Vonage's provided phone number (used with SMS & Voice APIs). Obtained from the Nexmo dashboard (https://dashboard.nexmo.com/)
martha_vonage_api_key = str("<PROVIDE VALUE>") # Vonage's API Key (used with SMS API). Obtained from the Nexmo dashboard (https://dashboard.nexmo.com/)
martha_vonage_api_secret = str("<PROVIDE VALUE>") # Vonage's API Secret (used with SMS API).  Obtained from the Nexmo dashboard  (https://dashboard.nexmo.com/)
martha_vonage_application_id = str("<PROVIDE VALUE>") # Vonage's Application ID (used with Voice API).  Obtained after creating an application via the Nexmo dashboard (https://dashboard.nexmo.com/applications/new)
martha_vonage_application_private_key_path = str("<PROVIDE VALUE>") # Vonage's Application Private Key (used with Voice API).  Obtained after creating an application via the Nexmo dashboard (https://dashboard.nexmo.com/applications/new)
martha_vonage_video_url = str("https://<PROVIDE VALUE>") # URL to the static client video conference (used with Vonage's TokBox Video API).  See README.md for setup instructions
voice_running_late_answer_url = str("https://<PROVIDE VALUE>") # Web URL to a JSON file containing text-to-speech fields & values for Vonage's Voice API.  See README.md for a sample JSON file

""" Capture user's name (i.e. Matt Schlau), so Martha can personalize user interaction (i.e. address user by name) """
class person:
    name = ''
    def setName(self, name):
        self.name = name

""" Evaluates if user's voice data (string) exists in list argument (terms).  Used to recognize if a known command was spoken to Martha """
def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

""" (speech recognition) Listen to microphone and translate spoken words to plaintext """
def record_audio(ask=False): # False default, given argument is optional (i.e. Martha can listen without intending to speak)
    r = sr.Recognizer() # Initializes recognizer object (responsible for speech recognition) and defaults to Google's Web Speech API
    with sr.Microphone(device_index=None) as source: # Use (system default) microphone (as opposed to injecting *.mp3 files)
        if ask: # (ask=True) Martha intends to speak
            speak(ask) # Calls "speak()" function (i.e. Martha speaks text supplied)
        audio = r.listen(source) # Records and stores USER's voice input
        voice_data = '' # Clears variable (i.e. previous calls to this function would otherwise harbor old data)
        try:
            voice_data = r.recognize_google(audio) # Translates user's voice recording (audio) into a text string (voice_data)
        except sr.UnknownValueError: # Error Condition:  If recognizer object receives non-intelligible speech or non-speech (i.e. baby babbling, whistling, air horns)
            speak('Please repeat that') # Martha speaks to user
        except sr.RequestError: # Error condition: Speech_Recognition service is unreachable or down
            speak('Sorry, the speech recognition service is unavailable') # Martha speaks to user
        if person_obj.name: # Checks if person_obj.name is NOT empty (i.e. Martha knows the user's name)
            print(f"{person_obj.name}: {voice_data.lower()}") # Prints (to stdout) user's translated voice recording (voice_data)
        else:
            print(f">> {voice_data.lower()}") # Prints (to stdout) user's translated voice recording (voice_data)
        return voice_data.lower() # Returns string (voice_data) to the function's caller

""" Convert string text to speaker audio """
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # Convert text (audio_string) to spoken English, then store in variable (tts)
    r = random.randint(1,30000000) # Randomly generates an integer within given range.  Used in next line to generate unique *.mp3 filenames, thus preventing name collisions (from previous function calls).  Collisions are possible, in the event that the application crashes (i.e. Ctrl+C) prior to the last line of this function (which is responsible for deleting *.mp3) executing
    audio_file = 'audio' + str(r) + '.mp3' # Creates string value (future filename) of "audio_<1,2,..,30000000>.mp3"
    tts.save(audio_file) # Creates the named *.mp3 (audio_file) and stores in it the spoken english (tts)
    print(f"Martha: {audio_string}") # Prints (to stdout) Martha's response (audio_string)
    playsound.playsound(audio_file) # Plays *.mp3 over speakers.  Unless gTTS fails, the output of this will match the above line's stdout
    os.remove(audio_file) # Deletes *.mp3 from system (to save space on drive and prevent collisions when function is called again).  Troubleshooting Tip:  Watch directory for deletion, as this signifies Martha is listening for microphone input again

""" List of commands Martha is listening for (and the appropriate responses to them) """
def respond(voice_data):
    # 0: (Vonage) Initiate Video Meeting (1-on-1)
    if there_exists(["video", "meeting", "conference"]):
        dest_phone_number = record_audio(f"What is the phone number of the person you seek to invite?")
        confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?")
        attempt = 0 # Initializes variable (int)
        while(True):
            if confirm == "yes" or confirm == "yes ma'am" or confirm == "correct" or confirm == "affirmative" or confirm == "confirmed" or confirm == "right" or confirm == "yup" or confirm == "yep": # User confirmed the desired recipient's phone number
                dest_phone_number_int = int(str(1) + dest_phone_number.replace('-', '')) # From variable (string), remove dashes (-), prepend US country code (1), and convert to int (i.e. 123-456-7890 --> 1234567890) to match Vonage's "Send SMS" API field "to:" requirement.  This assumes the user didn't provide an incongruent US-based phone number, nor a US country code)
                client = vonage.Client(key=martha_vonage_api_key, secret=martha_vonage_api_secret) # Sets client (Martha's) parameters for Vonage account
                response = vonage.Sms(client).send_message({ # Sends SMS message and stores JSON response (useful for potential logging and troubleshooting)
                    "from": martha_vonage_phone,
                    "to": dest_phone_number_int,
                    "text": "Hi.  You have been invited to join the following video meeting:  " + martha_vonage_video_url + " .",
                })
                webbrowser.get().open(martha_vonage_video_url) # Open video meeting URL
                speak(f"Your video meeting invitation has been sent to 1-{dest_phone_number}.  I will leave you now to meet with them in private.  Sayonara {person_obj.name}")
                print(f"Martha: Video Meeting Link:  {martha_vonage_video_url}") # Print (to stdout) the video meeting URL, in case user mistakenly closes their browser tab prematurely and wishes to return to the meeting
                exit() # Close Martha application
            else: # User did not confirm the desired recipient's phone number
                if attempt == 2: # "Initiate Video Meeting" request aborts, after 3 tries
                    speak(f"I'm afraid I don't understand.  What else might I be able to help you with today {person_obj.name}?")
                    break
                else: # User asked to provide recipient's phone number again
                    dest_phone_number = record_audio(f"I'm sorry.  Please repeat the recipient's phone number.")
                    confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?")
                    attempt = attempt + 1
                    continue

    # 1: (Vonage) Send SMS
    elif there_exists(["text", "message", "sms"]):
        dest_phone_number = voice_data.split("text ")[-1]
        dest_phone_number = dest_phone_number.split("message ")[-1]
        dest_phone_number = dest_phone_number.split("sms")[-1]
        dest_phone_number = dest_phone_number.split("to ")[-1]
        confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?") # Technically, this section should perform input validation (i.e. handling of phone number lengths and country codes).  A lengthy commented out code block follows further down that takes an initial stab at this, but I dropped the effort, because I didn’t want to get mired into input validation edge case logic during my initial development
        attempt = 0 # Initializes variable (int)
        while(True):
            if confirm == "yes" or confirm == "yes ma'am" or confirm == "correct" or confirm == "affirmative" or confirm == "confirmed" or confirm == "right" or confirm == "yup" or confirm == "yep": # User confirmed the desired recipient's phone number
                text_message = record_audio(f"What would you like to text the recipient?")
                confirm = record_audio(f"You would like to text: \"{text_message}\".  Is that correct {person_obj.name}?")
                attempt = 0 # Initializes variable (int)
                while(True):
                    if confirm == "yes" or confirm == "yes ma'am" or confirm == "correct" or confirm == "affirmative" or confirm == "confirmed" or confirm == "right" or confirm == "yup" or confirm == "yep": # User confirmed the desired message to be sent
                        dest_phone_number_int = int(str(1) + dest_phone_number.replace('-', '')) # From variable (string), remove dashes (-), prepend US country code (1), and convert to int (i.e. 123-456-7890 --> 1234567890) to match Vonage's "Send SMS" API field "to:" requirement.  This assumes the user didn't provide an incongruent US-based phone number, nor a US country code)
                        """
                        # This commented out code block performs phone number input validation (i.e. handling of phone numbers and country codes).  It works, but is incomplete (i.e. short codes).  It’s also a lot more complicated than the single line of code above, which is why it wasn’t utilized.  I’ve left it here for anyone desiring to continue this software development effort however, as input validation is important when it comes to production worthy code. Also, it should technically be moved into (and before) the first while loop (i.e. when validating the phone number provided)
                        dest_phone_number_str = dest_phone_number.replace('-', '').replace(' ','') # From variable (string), remove dashes (-) and spaces ( ).  For instance, this will convert "123-456-7890" to "1234567890"
                        if dest_phone_number_str[0] == 1 and len(dest_phone_number_str) == 11: # Simply convert phone number to an int, given phone number appears to of appropriate length and possesses a US country code (+1)
                            dest_phone_number_int = int(dest_phone_number_str) # Int required to match Vonage's "Send SMS" API field "to:" requirement
                            speak(f"Scenario A")
                        elif dest_phone_number_str[0] != 1 and len(dest_phone_number_str) == 10: # Add US country code (+1) and convert to an int, given phone number is the right length, except for the missing US area code (+1).  This scenario is the one most likely to execute
                            dest_phone_number_int = int(str(1) + dest_phone_number_str)
                            speak(f"Scenario B")
                        else: # Phone number provided is incogruent with US phone standards, is a short code, mistakenly includes an extension, and other potential catch-alls
                            speak(f"Please provide an appropriate US based 10 digit length phone number, without extensions.  You do not need to specify the US country code.")
                            speak(f"Scenario C")
                            break
                        """
                        client = vonage.Client(key=martha_vonage_api_key, secret=martha_vonage_api_secret) # Sets client (Martha's) parameters for Vonage account
                        response = vonage.Sms(client).send_message({ # Sends SMS message and stores JSON response (useful for potential logging and troubleshooting)
                            "from": martha_vonage_phone,
                            "to": dest_phone_number_int,
                            "text": text_message,
                        })
                        speak(f"Your text \"{text_message}\" has been sent to 1-{dest_phone_number}.  What else might I be able to help you with today {person_obj.name}?")
                        break
                    else: # User did not confirm the desired message to be sent
                        if attempt == 2: # "Send an SMS" request aborts, after 3 tries
                            speak(f"I'm afraid I don't understand.  What else might I be able to help you with today {person_obj.name}?")
                            break
                        else: # User asked to provide message to be sent again
                            text_message = record_audio(f"I'm sorry.  Please repeat the message you would like sent.")
                            confirm = record_audio(f"You would like to text: \"{text_message}\".  Is that correct {person_obj.name}?")
                            attempt = attempt + 1
                            continue
                break
            else: # User did not confirm the desired recipient's phone number
                if attempt == 2: # "Send an SMS" request aborts, after 3 tries
                    speak(f"I'm afraid I don't understand.  What else might I be able to help you with today {person_obj.name}?")
                    break
                else: # User asked to provide recipient's phone number again
                    dest_phone_number = record_audio(f"I'm sorry.  Please repeat the recipient's phone number.")
                    confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?")
                    attempt = attempt + 1
                    continue

    # 2: (Vonage) Running Late / Make (pre-scripted) Voice Call (text-to-speech via answer_url)
    elif there_exists(["late", "tardy", "delayed", "running behind"]):
        dest_phone_number = record_audio(f"What is the recipient's phone number?")
        confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?") # Technically, this section should perform input validation (i.e. handling of phone number lengths and country codes).  A lengthy commented out code block was provided in "(Vonage) Initiate Video Meeting (1-on-1)" that takes an initial stab at this, but I dropped the effort, because I didn’t want to get mired into input validation edge case logic during my initial development
        attempt = 0 # Initializes variable (int)
        while(True):
            if confirm == "yes" or confirm == "yes ma'am" or confirm == "correct" or confirm == "affirmative" or confirm == "confirmed" or confirm == "right" or confirm == "yup" or confirm == "yep": # User confirmed the desired recipient's phone number
                dest_phone_number_int = int(str(1) + dest_phone_number.replace('-', '')) # From variable (string), remove dashes (-), prepend US country code (1), and convert to int (i.e. 123-456-7890 --> 1234567890) to match Vonage's "Make Call" API field "to:" requirement.  This assumes the user didn't provide an incongruent US-based phone number, nor a US country code)
                client = vonage.Client(application_id=martha_vonage_application_id, private_key=martha_vonage_application_private_key_path)
                voice = vonage.Voice(client)
                response = voice.create_call({
                'to': [{'type': 'phone', 'number': dest_phone_number_int}],
                'from': {'type': 'phone', 'number': martha_vonage_phone},
                'answer_url': [voice_running_late_answer_url]
                })
                speak(f"I called to inform 1-{dest_phone_number} that you are running ten minutes late.  What else might I be able to help you with today {person_obj.name}?")
                break
            else: # User did not confirm the desired recipient's phone number
                if attempt == 2: # "Running Late" request aborts, after 3 tries
                    speak(f"I'm afraid I don't understand.  What else might I be able to help you with today {person_obj.name}?")
                    break
                else: # User asked to provide recipient's phone number again
                    dest_phone_number = record_audio(f"I'm sorry.  Please repeat the recipient's phone number.")
                    confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?")
                    attempt = attempt + 1
                    continue

    # 3: (Vonage) Make Voice Call (text-to-speech via NCCO)
    elif there_exists(["ring", "call", "voice note"]):
        dest_phone_number = voice_data.split("ring ")[-1]
        dest_phone_number = dest_phone_number.split("call ")[-1]
        dest_phone_number = dest_phone_number.split("voice note ")[-1]
        dest_phone_number = dest_phone_number.split("to ")[-1]
        dest_phone_number = dest_phone_number.split("for ")[-1]
        dest_phone_number = dest_phone_number.split("at ")[-1]
        confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?") # Technically, this section should perform input validation (i.e. handling of phone number lengths and country codes).  A lengthy commented out code block was provided in "(Vonage) Initiate Video Meeting (1-on-1)" that takes an initial stab at this, but I dropped the effort, because I didn’t want to get mired into input validation edge case logic during my initial development
        attempt = 0 # Initializes variable (int)
        while(True):
            if confirm == "yes" or confirm == "yes ma'am" or confirm == "correct" or confirm == "affirmative" or confirm == "confirmed" or confirm == "right" or confirm == "yup" or confirm == "yep": # User confirmed the desired recipient's phone number
                ncco_voice_message = record_audio(f"What would you like to tell the recipient?")
                confirm = record_audio(f"You would like to tell them: \"{ncco_voice_message}\".  Is that correct {person_obj.name}?")
                attempt = 0 # Initializes variable (int)
                while(True):
                    if confirm == "yes" or confirm == "yes ma'am" or confirm == "correct" or confirm == "affirmative" or confirm == "confirmed" or confirm == "right" or confirm == "yup" or confirm == "yep": # User confirmed the desired message to be sent
                        dest_phone_number_int = int(str(1) + dest_phone_number.replace('-', '')) # From variable (string), remove dashes (-), prepend US country code (1), and convert to int (i.e. 123-456-7890 --> 1234567890) to match Vonage's "Make Call" Voice API field "to:" requirement.  This assumes the user didn't provide an incongruent US-based phone number, nor a US country code)
                        client = vonage.Client(application_id=martha_vonage_application_id, private_key=martha_vonage_application_private_key_path)
                        voice = vonage.Voice(client)
                        response = voice.create_call({
                            "to": [{'type': 'phone', 'number': dest_phone_number_int}],
                            "from": {'type': 'phone', 'number': martha_vonage_phone},
                            "ncco": [{
                            "action": "talk",
                            "text": ncco_voice_message
                            }]
                        })
                        speak(f"Your message \"{ncco_voice_message}\" has been sent to 1-{dest_phone_number}.  What else might I be able to help you with today {person_obj.name}?")
                        break
                    else: # User did not confirm the desired message to be sent
                        if attempt == 2: # "Send an SMS" request aborts, after 3 tries
                            speak(f"I'm afraid I don't understand.  What else might I be able to help you with today {person_obj.name}?")
                            break
                        else: # User asked to provide message to be sent again
                            ncco_voice_message = record_audio(f"I'm sorry.  Please repeat the message you would like conveyed.")
                            confirm = record_audio(f"You would like to tell them: \"{ncco_voice_message}\".  Is that correct {person_obj.name}?")
                            attempt = attempt + 1
                            continue
                break
            else: # User did not confirm the desired recipient's phone number
                if attempt == 2: # "Send an SMS" request aborts, after 3 tries
                    speak(f"I'm afraid I don't understand.  What else might I be able to help you with today {person_obj.name}?")
                    break
                else: # User asked to provide recipient's phone number again
                    dest_phone_number = record_audio(f"I'm sorry.  Please repeat the recipient's phone number.")
                    confirm = record_audio(f"The phone number you said was {dest_phone_number}, correct?")
                    attempt = attempt + 1
                    continue

    # 4: Vonage Headquarters
    elif there_exists(["vonage headquarters"]):
        webbrowser.get().open("https://www.google.nl/maps/place/Vonage/@40.347517,-74.1901178,17z/data=!3m1!4b1!4m5!3m4!1s0x89c2329e087380b1:0x61f1c7579b67b5d6!8m2!3d40.3475129!4d-74.1879291")
        speak("Vonage headquarters is located at 23 Main Street, Holmdel, New Jersey.  Vonage can be reached at 732-528-2600.  Operating hours are Monday through Friday, from 9 AM to Midnight.  As well as Saturday and Sunday, from 9 AM to 8 PM.")

    # 5: Get Stock Price
    elif there_exists(["price of", "value of"]):
        search_term = voice_data.lower().split(" of ")[-1] # Split captures all words AFTER " of " (assumes user will ONLY speak the search query afterwards)
        stocks = {
            "vonage":"VG",
            "gamestop":"GME",
            "bitcoin":"BTC-USD",
            "tesla":"TSLA",
            "google":"GOOGL"
        }
        try:
            stock = stocks[search_term] # Check dictionary (stocks) for company (search_term).  If found, store the company's (key's) value (stock ticker symbol)
            stock = yf.Ticker(stock) # Queries Yahoo Finance API for stock ticker symbol (i.e. VG) and returns a JSON object containing associated data (i.e. market price, volume, business sector, and number of full time employees)
            speak(f'The price of {search_term} is {stock.info["regularMarketPrice"]} ({stock.info["currency"]})') # Extracts desired JSON data (i.e. regular market price and associated currency) for speech inclusion
        except: # Error Condition:  Yahoo Finance (yfinance) API is down.  Or, the requested company stock (i.e. Starbucks' SBUX) isn't represented in the "stocks" dictionary above
            speak('Sorry, I am unfamiliar with that stock')

    # 6: Query Vonage
    elif there_exists(["search", "query"]):
        search_term = voice_data.split("for ")[-1]
        url = search_term.replace(" ", "+")
        url = f"https://vonage.com/search/?q={url}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on the vonage website')

    # 7: Find Location
    elif there_exists(["show me", "find", "map of", "location of", "where is"]):
        # Below "split()" series is a best-effort (ordered) means of parsing spoken English; please don't try to intentionally confuse Martha!
        location = voice_data.split("show me ")[-1]
        location = location.split("find ")[-1]
        location = location.split("map of ")[-1]
        location = location.split("location of ")[-1]
        location = location.split("where is ")[-1]
        url = f"https://google.nl/maps/place/{location}"
        webbrowser.get().open(url)
        speak("This is where " + location + " is located")

    # 8: Name Inquiry
    elif there_exists(["your name"]):
        if person_obj.name: # Check if string is NOT empty (i.e. user's name is known)
            speak("my name is Martha")
        else:
            person_name = record_audio("My name is Martha. What's your name?")
            person_name = person_name.split("is ")[-1]
            person_obj.setName(person_name) # Store user's name for future recall
            if person_obj.name == 'martha': # Check if user's name is Martha
                speak(f"Wow, I can't believe we share the same name, Martha!")
            else:
                speak(f"Hi {person_name}, it's my pleasure to make your acquaintence")
            
    # 9: My Name
    elif there_exists(["my name is"]):
        person_name = voice_data.split("is ")[-1]
        person_obj.setName(person_name)
        if person_obj.name == 'martha': # Oh, you think you're funny?  You best watch out; Martha can be cheeky!
            speak(f"Oh, really?  Because, my name is Martha.  I think you're just joshing me, so I'm just going to call you Josh")
            person_obj.setName('Josh')
        else:
            speak(f"Okay, I will remember your name, {person_name}")

    # 10: Exit Application
    elif there_exists(["exit", "quit", "goodbye", "sayonara", "take care", "farewell"]):
        speak(f"Sayonara {person_obj.name}")
        exit() # Close Martha application

    # 11: Courteous Greeting
    elif there_exists(["how are you"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")

    # 12: Basic Greeting
    elif there_exists(['hey', 'hi', 'hello', 'howdy', 'hola', 'Konnichiwa']):
        greetings = [f"Hey, how can I help you {person_obj.name}?", f"Hey, what's up {person_obj.name}?", f"I'm listening {person_obj.name}", f"How can I help you {person_obj.name}?", f"Hello {person_obj.name}"]
        greet = greetings[random.randint(0,len(greetings)-1)] # Randomly selects a greeting from the above list.  If the user's name is known, Martha will address them by name, too
        speak(greet)

speak(f"Kon'nichiwa!  How can I help you today?") # Initial greeting when starting application
person_obj = person() # Stores user's name (i.e. Matthew Schlau) 
while(True): # (infinite loop) Ensures Martha continuously listens for user spoken input (except when she's speaking)
    voice_data = record_audio() # Calls function to listen to user's microphone and translate spoken words to text.  Ultimately stores function's local variable (voice_data) into the global variable (also called voice_data)
    respond(voice_data) # Calls function to listen for a variety of user spoken commands (and respond to them accordingly)