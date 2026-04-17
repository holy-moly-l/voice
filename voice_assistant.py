#!/usr/bin/env python3
"""
Голосовой ассистент - программа для распознавания и выполнения голосовых команд.

Функционал:
- Распознавание речи через микрофон
- Выполнение команд: приветствие, время, дата, погода (заглушка), открытие сайтов
- Голосовой ответ через синтезатор речи

Использование:
    python voice_assistant.py
    
Для выхода скажите "выход" или "стоп".
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys


class VoiceAssistant:
    """Класс голосового ассистента."""
    
    def __init__(self):
        # Инициализация распознавателя речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Настройка распознавателя
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
        # Инициализация синтезатора речи
        self.engine = pyttsx3.init()
        self._setup_voice()
        
        print("🎤 Голосовой ассистент готов к работе!")
        print("Скажите команду или 'выход' для завершения работы.\n")
    
    def _setup_voice(self):
        """Настройка голоса синтезатора."""
        voices = self.engine.getProperty('voices')
        # Выбираем первый доступный голос (обычно русский если установлен)
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)  # Скорость речи
    
    def speak(self, text):
        """Произносит текст вслух."""
        print(f"🤖 Ассистент: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Слушает микрофон и возвращает распознанный текст."""
        try:
            with self.microphone as source:
                print("👂 Слушаю...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("🔄 Распознаю...")
            # Пытаемся распознать речь на русском языке
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            print(f"🗣️ Вы сказали: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❌ Не удалось распознать речь")
            return None
        except sr.RequestError as e:
            print(f"❌ Ошибка сервиса распознавания: {e}")
            return None
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None
    
    def execute_command(self, command):
        """Выполняет команду."""
        if not command:
            return True
        
        # Команда: Приветствие
        if "привет" in command or "здравствуй" in command:
            self.speak("Здравствуйте! Чем я могу вам помочь?")
        
        # Команда: Время
        elif "время" in command or "который час" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"Сейчас {now}")
        
        # Команда: Дата
        elif "дата" in command or "какое сегодня число" in command:
            today = datetime.datetime.now().strftime("%d %B %Y")
            self.speak(f"Сегодня {today}")
        
        # Команда: День недели
        elif "день недели" in command:
            days = ["понедельник", "вторник", "среда", "четверг", 
                   "пятница", "суббота", "воскресенье"]
            today = datetime.datetime.now().weekday()
            self.speak(f"Сегодня {days[today]}")
        
        # Команда: Открыть Google
        elif "открой гугл" in command or "google" in command:
            self.speak("Открываю Гугл")
            webbrowser.open("https://google.com")
        
        # Команда: Открыть YouTube
        elif "ютуб" in command or "youtube" in command:
            self.speak("Открываю Ютуб")
            webbrowser.open("https://youtube.com")
        
        # Команда: Открыть Яндекс
        elif "яндекс" in command:
            self.speak("Открываю Яндекс")
            webbrowser.open("https://yandex.ru")
        
        # Команда: Как дела
        elif "как дела" in command or "как ты" in command:
            self.speak("У меня всё отлично! Спасибо, что спросили.")
        
        # Команда: Твоё имя
        elif "твоё имя" in command or "как тебя зовут" in command:
            self.speak("Меня зовут Голосовой Ассистент")
        
        # Команда: Выход
        elif "выход" in command or "стоп" in command or "пока" in command:
            self.speak("До свидания! Хорошего дня!")
            return False
        
        # Команда: Помощь
        elif "помощь" in command or "что ты умеешь" in command:
            help_text = """Я умею: говорить время и дату, 
                          открывать сайты в браузере, 
                          отвечать на простые вопросы.
                          Скажите выход чтобы завершить работу."""
            self.speak(help_text)
        
        # Неизвестная команда
        else:
            self.speak("Извините, я не понял эту команду. Попробуйте ещё раз.")
        
        return True
    
    def run(self):
        """Запускает основной цикл работы ассистента."""
        running = True
        while running:
            command = self.listen()
            running = self.execute_command(command)
            print()


def main():
    """Точка входа программы."""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\nРабота ассистента завершена пользователем.")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("Убедитесь, что микрофон подключен и настроен.")
        sys.exit(1)


if __name__ == "__main__":
    main()
