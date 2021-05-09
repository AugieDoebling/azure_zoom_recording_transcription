import azure.cognitiveservices.speech as speechsdk
import moviepy.editor as mp
import time
import datetime
import sys
import os 

# azure subscription key - see readme
AZURE_SUBSCRIPTION_ID = ''
AZURE_REGION = 'westus'

# directory to save audio results to 
VIDEO_INPUT_DIRECTORY = 'input_videos'
# directory to save transcription results to 
OUTPUT_DIRECTORY = 'results'


if AZURE_SUBSCRIPTION_ID == '' or AZURE_REGION == '' or VIDEO_INPUT_DIRECTORY == '' or OUTPUT_DIRECTORY == '':
    print('please update the usage variables in the top of azure_transcribe_videos.py')
    exit()


# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SUBSCRIPTION_ID, region=AZURE_REGION)


def speech_to_text(audio_filename, output_file):
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

    # Creates a recognizer with the given settings
    speech_config.speech_recognition_language="en-US"
    # speech_config.request_word_level_timestamps()
    speech_config.enable_dictation()
    speech_config.output_format = speechsdk.OutputFormat(1)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    #result = speech_recognizer.recognize_once()
    all_results = []

    #https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.recognitionresult?view=azure-python
    def handle_final_result(evt):
        all_results.append(evt.result.text)
    
    done = False

    def stop_cb(evt):
        # print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done= True

    #Appends the recognized text to the all_results variable. 
    speech_recognizer.recognized.connect(handle_final_result) 

    #Connect callbacks to the events fired by the speech recognizer & displays the info/status
    #Ref:https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.eventsignal?view=azure-python   
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('.',end='',flush=True))
    # speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)
            
    print("Writing to file")
    with open(output_file, mode='w+') as file:
       for res in all_results:
          file.write(res)
          file.write('\n\n')


def video_to_wav(file):
   name = os.path.splitext(file)[0]
   output_file = f'{OUTPUT_DIRECTORY}/{name}.wav'
   if os.path.exists(output_file):
      print('file already converted', file)
   elif file.endswith('.mp4'):
      print('converting', file)
      clip = mp.VideoFileClip(VIDEO_INPUT_DIRECTORY+'/'+file) 
      clip.audio.write_audiofile(output_file)
      print('   finished.')


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def cleanup_audio_files(directory):
    for file in os.listdir(directory):
        if file.endswith('.wav'):
            os.remove(os.path.join(directory, file))

def main():
    for file in os.listdir(VIDEO_INPUT_DIRECTORY):
        if not file.endswith('.mp4'):
            continue

        name = os.path.splitext(file)[0]
        output_file = f'{OUTPUT_DIRECTORY}/{name}.txt'

        if os.path.exists(output_file):
            print('file is already transcribed', file)
        else:
            print('converted to .wav file', file)
            video_to_wav(file)
            print('transcribing', file)
            speech_to_text(OUTPUT_DIRECTORY+'/'+file, output_file)

    print('complete, cleaning up intermediate audio files')
    cleanup_audio_files(OUTPUT_DIRECTORY)

if __name__ == "__main__":
    main()

