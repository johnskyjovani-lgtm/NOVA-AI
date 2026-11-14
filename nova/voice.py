import speech_recognition as sr

def listen_once(language='pt-PT'):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('NOVA está a ouvir...'); r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=6, phrase_time_limit=12)
        return r.recognize_google(audio, language=language)
    except sr.RequestError: return '[SEM_INTERNET]'
    except (sr.WaitTimeoutError, sr.UnknownValueError): return ''
    except Exception as e: print('Microfone:', e); return ''
