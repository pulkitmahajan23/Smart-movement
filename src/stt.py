#!/usr/bin/env python3

import speech_recognition as sr
import re
r=sr.Recognizer()

def command():
    while True:
        with sr.Microphone() as source:
            print("Listening")
            audio=r.listen(source,phrase_time_limit=10)
            try:
                response=r.recognize_google(audio)
                res=str(response)
                print(res,"\n")
                return res
                if 'stop' in res:
                    break
            except sr.UnknownValueError:
                print("Could not understand audio\n")
            except sr.RequestError as e:
                print("Error,{0}".format(e))
    print("exiting")

if __name__ == "__main__":
    test_string = "There are 24 apples for 4 persons"
    # printing original string  
    print("The original string : " + test_string) 
    #  using re.findall() 
    #  getting numbers from string  
    temp = re.findall(r'\d+', test_string) 
    res = list(map(int, temp))
    print(str(res[0]))
    command()
# print result
