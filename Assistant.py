import pyttsx3 as pyt
import datetime
import speech_recognition as sr
import audiomath; audiomath.RequireAudiomathVersion( '1.12.0' )
import speech_recognition  # NB: python -m pip install SpeechRecognition
import wikipedia
import webbrowser
from pygame import mixer
import time

mixer.init()
mixer.music.load("alarm.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()
mixer.music.pause()

class DuckTypedMicrophone(speech_recognition.AudioSource): # descent from AudioSource is required purely to pass an assertion in Recognizer.listen()
    def __init__( self, device=None, chunkSeconds=1024/44100.0 ):  # 1024 samples at 44100 Hz is about 23 ms
        self.recorder = None
        self.device = device
        self.chunkSeconds = chunkSeconds
    def __enter__( self ):
        self.nSamplesRead = 0
        self.recorder = audiomath.Recorder( audiomath.Sound( 5, nChannels=1 ), loop=True, device=self.device )
        # Attributes required by Recognizer.listen():
        self.CHUNK = audiomath.SecondsToSamples( self.chunkSeconds, self.recorder.fs, int )
        self.SAMPLE_RATE = int( self.recorder.fs )
        self.SAMPLE_WIDTH = self.recorder.sound.nbytes
        return self
    def __exit__( self, *blx ):
        self.recorder.Stop()
        self.recorder = None
    def read( self, nSamples ):
        sampleArray = self.recorder.ReadSamples( self.nSamplesRead, nSamples )
        self.nSamplesRead += nSamples
        return self.recorder.sound.dat2str( sampleArray )
    @property
    def stream( self ): # attribute must be present to pass an assertion in Recognizer.listen(), and its value must have a .read() method
        return self if self.recorder else None

def open_chrome(url):
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    return webbrowser.get(chrome_path).open(url)
    

def paaro_listen():
    import speech_recognition as sr
    try:
        r = sr.Recognizer()
        with DuckTypedMicrophone() as source:
            print("listening.......")
            print('\nSay something to paaro...' )
            audio = r.listen(source)
        querry = r.recognize_google(audio)
        print('Got it.')
        # print(f'\nUnderstood:{querry}\n')
        return querry 
    except Exception as e:
        print(e)
        paro_say("cant recognize ,speak again")
        engine.runAndWait()
        paaro_listen()



engine =  pyt.init()
voices = engine.getProperty("voices")
engine.setProperty('rate', 130) 
engine.setProperty("volume",2)
engine.setProperty("voice", voices[1].id)
# speak
def paro_say(str):
    engine.say(str)
    engine.runAndWait()

voice = engine.getProperty("voices")

#wish

def paro_wish():
    if(datetime.datetime.now().hour>0 and datetime.datetime.now().hour<12):
        paro_say("good morning.")
    elif(datetime.datetime.now().hour>12 and datetime.datetime.now().hour<17):
        paro_say("good afternoon.")
    else:
        paro_say("good evening.")

    paro_say("hell, i am paaru")

#check integer

def check_int(str):
    try:
        int(str)
        return True
    
    except Exception as e:
        #print(e)
        return False 
#alarm
def paro_alarm(inp):
    current = datetime.datetime.now().hour
    inp_s = inp.split(" ")
    for item in inp_s:
        if(check_int(item)):
            paro_say(f"alarm set for {item} hours, say stop to stop the alarm")
            while("true"):
                a = datetime.datetime.now().hour
                c = int(item)
                if ((a + c)>23):
                    c = c - 24
                d = current + c  
                if(a==d):
                    while("true"):
                        mixer.music.unpause()
                        print("say stop")
                        inp2 = paaro_listen()
                        if(inp2=="stop"):
                            mixer.music.stop()
                            break
                    break
if __name__ == "__main__":
    paro_wish()
    
    while(True):
        querry = paaro_listen().lower()
        
        if "wikipedia" in querry:
            paro_say("searching")
            querry = querry.replace("wikipedia","")
            results = wikipedia.summary(querry, sentences = 2)
            paro_say(results)
            
        elif("songs" in querry):
            paro_say("okay, wait")
            open_chrome("https://gaana.com/artist/arijit-singh")
        elif("music" in querry):
            paro_say("sure, wait")
            open_chrome("https://gaana.com/artist/arijit-singh")

        elif("youtube" in querry):
            
            open_chrome("youtube.com")
        elif("drilling technology" in querry):
            paro_say("lets study, dont sleep in class sir")
            open_chrome("https://zoom.us/wc/4888617297/join?track_id=&jmf_code=&meeting_result=&tk=&cap=03AGdBq24PteXOj3oiMZThQelC8VtvixBrO9hjV4xhYWxNRsfozDk6qdAIFnZa-XV5Cx_l_V2SMt8EOnvWzbgYSAw7wErRR6_OfHE0j8MfhyJ6mEpoTuaV-6erqTargD21PdmWCNu2BsGtqFerlXkfJl0yDIVUxs4vo_KIzYDFZyFSpK80wgf7UVC4It1GK5JTTmJvl-GNIbMbPsb6_mA4YsrdFFhk50PHKjBjaTL79R46qU-xdQ5S42g87sapx7LtRalstOCTTbTaco_jhX-Zt9x0z2XRpjU7L-fN-rZHzjEPP2Sqbfv5XjHdUzL3AIehySCOvq3j7lv5-iJ9fpCXHoSjk-Gdy6N6UG2JkZcWyd950Y7I2M_bzKL8hYTVq_gZPTisZjRe6m4rqNUmeyBRluL1qzEec_yOXpLI5uTLz8goviFYovNe0EYXrB9bWOlAfnlCUd6I55Ps4LU0idkqceX3arvYvdEMDAENPV1nsCPbR71VjPXD-8aZOav6YxdSTOtDHjRYi2og&refTK=")
        elif("elements of reservoir" in querry) :
            paro_say("lets study, dont sleep in class sir")
            open_chrome("https://meet.google.com/lookup/bv5k3kde4c?authuser=1&hs=179")
        elif("drilling fluids and cements" in querry):
            paro_say("lets study, dont sleep in class sir")
            open_chrome("https://zoom.us/wc/82683733154/join?track_id=&jmf_code=&meeting_result=&tk=&cap=03AGdBq24DJU1rB0QU_2g-TBfRMu8KnaOZy1F24figjSYCGZYiBX9_MRtjpNrm_-bvaxqyjnriaYlLqREhsjiikgbgHvrwm6wRBjjYXQpzKKfVyyX34CfqqviOotjLFKerUtz7zZHYWhbUND_rQXWw3oB60wUtrQVgylzTZ-ZQ7Ku9PxJOZz1U2ydb03hS-6fhEkj8NeEO6hOc1kiZk2gcsYqMcQx__t-aJlItabE-CtjzOSjeCCrq84jAh3YYYF_YsSrvBqFf2BDDyfMDTopYy-3R0jX0POvcFpK7izpaf892USYbbPhTivrGJ3G80wk7xAu194Qp-DEqQupcJDhTVTDBhoAVc1IrFVPryDoUPD4ENSVXn1-llBWpNrxtm3xK1lcTVEJnFTvtS6zsvG72KQjnTlgftA_nfgkwUh05k5hLCXkhZTi6ENx92aG88xsR4IAFihBQYF00syp_mmns5f2c8poCk-3ccou_6ZBCfaVNesgfa3-3ieyK21Ae3sYwI9-rWwPcIwz2&refTK=")

        elif("tired" in querry):
            paro_say("take a nap sir , close your laptop")

        elif("sad" in querry):
            paro_say("sir, dont suicide , please")
        elif("bored" in querry):
            paro_say("no problem, you can study for some")
        elif("boring" in querry):
            paro_say("no problem, you can study for some")

        elif("my facebook" in querry):
            paro_say("okay, wait")
            open_chrome("https://www.facebook.com/")
        elif("my instagram" in querry):
            paro_say("okay, wait")
            open_chrome("https://www.instagram.com/?hl=en")
        elif("my whatsapp" in querry):
            paro_say("okay, wait")
            open_chrome("https://web.whatsapp.com/")
        elif("machine learning" in querry):
            paro_say("okay, wait")
            open_chrome("https://www.coursera.org/my-purchases/transactions")
        elif("who are you" in querry):
            paro_say("i am a robot named paaru , i am under construction by aniket raj, i am searching for true love")

        elif("sing a song" in querry):
            paro_say("i am a bad singer,but as your wish")
            mixer.music.unpause()
            time.sleep(4)
            mixer.music.stop()
            continue
        elif("i love you" in querry):
            paro_say("okay but you are not going to get anything , lol")
        elif("good" in querry):
            paro_say("thanku")
        elif("bad" in querry):
            paro_say("i know")
        elif("a kiss" in querry):
            paro_say("okay , my voltage can kill you by the way")
        elif("you are good" in querry):
            paro_say("because i am not a human")
        elif("best thing" in querry):
            paro_say("your mom")
        elif("good bye" in querry):
            paro_say("dont say so, i will miss you")
        elif("set alarm" in querry):
            paro_alarm(querry) 

        elif("bye" in querry):
            paro_say("bye sir,  have a nice day")
            break
       
        else:
            paro_say("this is not in my range or speak it properly")

            
