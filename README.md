# DESCRIPTION:
_Application purpose, explanation, and authorship_

Martha<span>.</span>py is a Personal Assistant (PA) application.  With a few tweaks, she could also serve as an excellent automated telephone greeter and call agent. Martha listens for voice commands, which trigger unique functions (SMS, VOIP, Video Meetings, etc.).  For an extensive list of commands, see the "Commands List" below.  Martha was written by [Matthew Schlau](https://www.linkedin.com/in/mschlau/) to advance his practicical Python skills, as well as gain familiarity working with public internet based APIs, particularly Vonage's RESTful Open Communitaction APIs.  This application and its AI persona gained its name from the lamented modern dance artist and pioneer [Martha Graham](https://www.youtube.com/watch?v=dYYs5P-ccS4)

<ins>Special thanks go to the following individuals for their contributions:</ins>
- [Baltazar Suarez](https://www.linkedin.com/in/baltazarsuarez/) for familiarizing me with Vonage's API offerings, as well as for recommending ngrok
- [Brad Traversy](https://www.youtube.com/channel/UC29ju8bIPH5as8OGnQzwJyA) for his insightful software development videos, which inspired this project
- [Markus Lachinger](https://www.linkedin.com/in/mmlac/) for best-practice software development tips and Virtual Audio Cable (VAC) troubleshooting

# COMMANDS LIST:
_An in-order list of phrases Martha listens for.  If two or more commands are issued in a single statement, then only the prioritized (lower #) command will execute_

0.  (Vonage)  Initiate Video Meeting (1-on-1):
    - Verbal Commands:  "video", "meeting", and "conference"
    - Example:  "Please send a <ins>meeting</ins> invitation to my friend, Martha."
1.  (Vonage) Send SMS:
    - Verbal Commands:  "text/message/sms [to] <_phone number_>"
    - Example:  "Martha, would you please <ins>text 8675-309</ins>?"
        * Note:  Any Tommy Tutone / Jenny fans out there?  :)
2.  (Vonage) Running Late / Make (pre-scripted) Voice Call (text-to-speech via answer_url):
    - Verbal Commands:  "late", "tardy", "delayed", and "running behind"
    - Example:  "Hey Martha, can you let my friend know I'm running <ins>late</ins> for our dinner plans?"
3.  (Vonage)  Make Voice Call (text-to-speech via NCCO):
    - Verbal Commands:  "ring/call/voice note [...] <_phone number_>"
    - Example:  "Hey Martha, please <ins>call</ins> my friend <ins>at 8675-309</ins>!"
4.  Vonage Headquarters:
    - Verbal Commands:  "Vonage headquarters"
    - Example:  "How can I reach <ins>Vonage Headquarters</ins>, Martha?"
5.  Get Stock Price:
    - Verbal Commands:  "price of <_company_>" and "value of <_company_>"
    - Example:  "What is the stock <ins>price of Vonage</ins>?"
6.  Query Vonage:
    - Verbal Commands:  "search/query [...] for <_topic_>"
    - Example:  "Martha, would you please <ins>search</ins> the vonage website <ins>for open communication APIs</ins>?"
7.  Find Location:
    - Verbal Commands:  "show me / find / map of / location of / where is <_location_>"
    - Example:  "Martha, can you <ins>show me</ins> on google maps the <ins>location of Holmdel, New Jersey</ins>?"
8.  Name Inquiry:
    - Verbal Commands:  "your name"
    - Example:  "Sorry, but what is <ins>your name</ins> again?"    ---->    "Oh, I didn't think you would ask.  My name is Matthew Schlau"
        - NOTE:  If Martha doesn't know the user's name, she will ask them for it
9.  My Name:
    - Verbal Commands:  "my name is <_name_>"
    - Example:  "I can't remember if I told you before, but <ins>my name is Matthew Schlau</ins>"
10. Exit Application:
    - Verbal Commands:  "quit", "exit", "goodbye", "sayonara", "take care", and "farewell"
    - Example:  "<ins>Goodbye</ins> Martha; it's been real!"
11. Courteous Greeting:
    - Verbal Commands:  "how are you"
    - Example:  "<ins>How are you</ins> today, Martha?"
12. Basic Greeting:
    - Verbal Commands:  "hey", "hi", "hello", "howdy", "hola", and "Kon'nichiwa"
    - Example:  "<ins>Hi</ins> Martha!"

# INSTRUCTIONS:  ENVIRONMENT SETUP / CONFIGURATION / EXECUTION:
_Follow this process, else Martha may ignore you!_

1.  _(environment setup)_  Review the "Dependencies" section below.  If your system does not conform, then Martha<span>.</span>py will not fully work as intended.  Additionally, Martha<span>.</span>py uses the OS' default microphone and speakers, so make sure they are connected and work properly
    - Note:  If you don't want to use your system default microphone, search Martha<span>.</span>py for "_device_index=None_" and change the value of "_none_" to your desired microphone's index number
2.  _(configuration)_  Within Martha<span>.</span>py, you must initialize your variables in the "Initialize variables" section
    - Note 1:  The "voice_running_late_answer_url" variable necessitates a text-to-speech ready JSON file conforming to Vonage's Nexmo "Voice API" requirements.  See the "Sample - voice_running_late_answer_url" section near the bottom of this README for a ready-to-go JSON conformant file
    - Note 2:  The "martha_vonage_video_url" variable necessitates that you first host [client code](https://github.com/opentok/opentok-web-samples/tree/main/Basic%20Video%20Chat) on a public website (i.e. ngrok, Heroku, or Amazon S3).  Ngrok would be simplest; simply run "_ngrok http "file:////C:\path\to\client\code\directory_", copy the "Forwarding" https://*.ngrok.io URL it outputs, and paste it as a value assignment for the "martha_vonage_video_url" variable.  Also, don't forget to update the config.js file with an API_KEY, SESSION_ID, and TOKEN.  All three values can be obtained by creating a new session in Vonage's [OpenTok Playground](https://tokbox.com/developer/tools/playground/)
3.  _(execution)_  Run Martha<span>.</span>py, await her greeting, and then speak aloud a command to Martha (see the "Commands List" section above). There is no built-in keyboard and mouse interactive support, though Martha will print to stdout what she thinks the user said, as well as what she plans to say
    - Note:  Martha will not listen for verbal commands when she is actively speaking

# DEPENDENCIES:
_Martha requires a Windows 10 OS, with Python (3.9.2 or above) and pip (21.0.1 or above) already installed.  Additionally, Martha needs to be able to reach the public internet (to perform API calls)_

- pip install speechrecognition _(3.8.1 or above)_
- pip install playsound _(1.2.2 or above)_
- pip install gtts _(2.2.2 or above)_
- pip install yfinance _(0.1.55 or above)_
- pip install vonage _(2.5.5 or above)_
- pip install pipwin _(0.5.1 or above)_
- pipwin install pyaudio _(0.2.11 or above)_

# LIMITATIONS:
_The following code limitations were observed during software development.  Most result from built-in limitations within the SpeechRecognition and GTTS APIs.  This list is provided for those interested in further developing this code_

1.  Speech recognition sometimes gets overwhelmed and fails to process user spoken commands.  Typically occurs when there is a lot of background noise, even if the sound is consistent and low volume (i.e. A/C, fans)
2.  Speech recognition is set to English by default, so non-English (as well as thick accents) sometimes produce undesirable results
3.  Speech recognition reacts to certain phrases counter to its programmed if-elif logic (i.e. saying "search something" will trigger the "Courteous Greeting" code block)
4.  GTTS sometimes mispronounces words (i.e. "Vonage" pronounced like "Bonage").  This is partially a result of defining the language used to "en" (english)
5.  Prevention of multi-command execution is accomplished with if-elif command structure (versus a series of "if" statements).  This is an intentional design decision.  However, a user could conceivably speak two unique voice commands and have intended for the lower priority one (or both) to execute (i.e. the order in which commands are received is irrelevant)
6.  Similar to the above limitation, once within an if/elif statement, if there are if/elif/else statements contained within it, then those will take priority.  For instance, if a user speaks aloud "What's your name?", then they'll be asked to provide their own name.  If the user responds "quit application", then instead of exiting, Martha will store the user's name as "quit application".  Ideally, escape commands (i.e. exit, go back) should be introduced
7.  User unexpected outcomes are possible, given that accounting for every conceivable common english phrase (or misphrasing), as well as intentional efforts by the user to deceive Martha, are something I deemed out-of-scope during development.  For instance, see the code block for "#7 Find Location", which illustrates a best-effort means of helping Martha make sense of the user's spoken intent.  Alternatively, see the code block for "#9 My Name" and tell Martha, "My name is <_silence_>", then wait to see what she stores your name as
8.  Related to the above limitation, but more input validation (i.e. phone number length and country code inclusion) would be needed for production-worthy code.  For those interested in extending this code, I retained a commented out code block in "#1 Send SMS", which highlights the start of this effort (it's mostly functional, but would require more development and validation before implementation)

# SAMPLE - VOICE_RUNNING_LATE_ANSWER_URL:
_Store this JSON on the public internet (i.e. ngrok, Heroku, Amazon S3) and assign its URL to the "voice_running_late_answer_url" variable_

```JSON
[
    {
        "action": "talk",    
        "text": "Hey!  Heads up that I'm running about ten minutes late.  See you soon!",
        "language": "en-AU",
        "style": 3    
    }
]
```

# Virtual Audio Cables (VACs) Support:
_[Virtual Audio Cables (VACs)](https://vb-audio.com/Cable/) are not needed for use with Martha.  However, if you intend to use Martha during a VOIP call (i.e. Skype/Zoom/Teams/Google Meeting) with real human beings, they won't be able to hear Martha's responses.  I've included a VACs setup procedure (see VACs_Setup.jpg below), which illustrates how to remedy this.  Incidentally, this setup is also great for other forms of streaming (i.e. video game streamers).  Optionally, with some minor tweaks to the provided VAC setup, you can enable others in the VOIP call to speak directly with Martha_

![VACs Setup](/VACs_Setup.jpg?raw=true "VACs Setup")
