from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# speech engine initialisation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # 0 = male, 1 = female
activationWords = ['computer', 'calcutron', 'shodan', 'showdown']

# Configure browser
# Set the path
chrome_path = r"C\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))
def speak(text, rate = 120):
    # time.sleep(0.3)

    # if tts_type == 'local':
        engine.setProperty('rate', rate) 
        engine.say(text)
        engine.runAndWait()
    # if tts_type == 'google':
    #     speech = google_text_to_wav('en-US-News-K', text)
    #     pygame.mixer.init(frequency=12000, buffer = 512)
    #     speech_sound = pygame.mixer.Sound(speech)
    #     speech_sound.play()
    #     time.sleep(len(text.split()))
    #     pygame.mixer.quit()


def parseCommand():
    # with noalsaerr():
        listener = sr.Recognizer()
        print('Listening for a command')

        with sr.Microphone() as source:
            listener.pause_threshold = 2
            input_speech = listener.listen(source)

        try:
            print('Recognizing speech...')
            query = listener.recognize_google(input_speech, language='en_gb')
            print(f'The input speech was: {query}')

        except Exception as exception:
            print('I did not quite catch that')
            speak('I did not quite catch that')
            print(exception)
            return 'None'

        return query

def search_wikipedia(query=''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        return 'No result received'
        print('No wikipedia result')

    try: 
        wikiPage = wikipedia.page(searchResults[0]) 
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary     


# Main loop
if __name__ == '__main__': 
    speak('All systems nominal.', 120)

    while True:
        # Parse as a list
        # query = 'computer say hello'.split()
        query = parseCommand().lower().split()

        if query[0] in activationWords:
            query.pop(0)

             # Set commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all!')
                else:
                    query.pop(0) # Remove 'say'
                    speech = ' '.join(query) 
                    speak(speech)

            # Navigation
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening... ')
                # Assume the structure is activation word + go to, so let's remove the next two words
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)        

             # Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank')
                # time.sleep(2)
                speak(search_wikipedia(query))


            # Wolfram Alpha
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('Unable to compute')    