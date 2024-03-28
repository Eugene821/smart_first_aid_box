import speech_recognition as sr
import socket
import threading
import sys
import time
import pygame

pygame.init()

HOST = "10.10.14.69"
PORT = 5000
ADDR = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

recognizer = sr.Recognizer()

class SoundManager:
    def __init__(self):
        self.current_sound = None

    def play_sound(self, file_path):
        try:
            if self.current_sound is not None:
                self.current_sound.stop()
            self.current_sound = pygame.mixer.Sound(file_path)
            self.current_sound.play()
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping sound playback.")

sound_manager = SoundManager()

# 사운드 파일을 여러 키워드에 매핑
sound_to_words_mapping = {
    'data/화상.wav': ['데었어', '데었네', '데었다', '화상', '뜨거워', '뜨겁네', '뜨겁다'],
    'data/출혈.wav': ['피나', '베었어', '베었네', '베었다', '찔렸어'],
    'data/벌레.wav': ['물렸어', '가려워', '모기']
}

try:
    s.connect(ADDR)
except Exception as e:
    print(f'{ADDR}에 연결할 수 없습니다: {e}')
    sys.exit()

print('Connection successful.')

def process_speech_input():
    while True:
        with sr.Microphone() as source:
            print("Please speak...")
            audio_data = recognizer.listen(source)
            print("Recognizing...")

        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"Recognized: {text}")

            played = False
            for sound_path, words in sound_to_words_mapping.items():
                if any(word in text for word in words):
                    sound_manager.play_sound(sound_path)
                    played = True
                    print(f"Playing sound for keywords related to: {sound_path}")
                    break

            if not played:
                print("No matching sound file found for recognized text.")

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

threading.Thread(target=process_speech_input).start()

while True:
    time.sleep(1)
