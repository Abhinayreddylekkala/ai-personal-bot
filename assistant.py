import speech_recognition as sr
import pyttsx3
import datetime
import requests
import wikipedia
import webbrowser
import smtplib

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return text 


def recognize_speech():
    """Recognize speech input"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        speak("Listening...")
        audio = recognizer.listen(source)

    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, could not understand. Try again.")
        return None
    except sr.RequestError:
        speak("Could not connect to the speech service.")
        return None
        

def get_weather(city):
    """weather information"""
    API_KEY = "3d6ef41c99678317bd8ef5b89e35a633"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url) 
        data = response.json()
        
        if data["cod"] != 200: # City not found
            speak("City not found. Please try again.")
            return "City not found."
        
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        result = f"Current weather in {city} is {weather} with a temperature of {temp}°C."
        speak(result)
        return result
    except Exception as e:
        speak("Unable to fetch weather data.")
        return f"Error fetching weather data: {e}"


def get_datetime():
    """Returns current date"""
    current_datetime = datetime.datetime.now().strftime("%A, %B %d, %Y, %H:%M:%S")
    speak(f"Today's datetime is {current_datetime}")
    return f"Today's datetime : {current_datetime}"


def search_wikipedia(query):
    try:
        query = query.strip().title()  # Fix capitalization issues
        summary = wikipedia.summary(query, sentences=2)
        return summary
        speak (summary)
    except wikipedia.exceptions.PageError:
        return "No Wikipedia page found. Try another topic."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:5]}"
    except Exception as e:
        return f"Error fetching Wikipedia page: {str(e)}"


def search_google(query):
    """Search Google"""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {query}.")
    return f"Searching Google for: {query}"
def send_email(to_email, subject, body):
    """Sends an email using Gmail"""
    sender_email = "chinnaabhu4@gmail.com"  # Replace with your email
    sender_password = "wcsr ttvz akwq kgnh"  # Replace with your email password (use App Passwords if possible)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, to_email, message)
        server.quit()

        speak("Email sent successfully.")
        return "Email sent successfully."
    except Exception as e:
        speak("Failed to send email.")
        return f"Email error: {e}"

def process_command(command, input_mode):
    """Process user command based on input mode"""
    command = command.lower()
    
    if "datetime" in command:
        print(get_datetime())
    elif command == "weather":
        speak("Which city?")  # This only speaks but returns nothing
        city = recognize_speech() if input_mode == "speak" else input("Enter city: ").strip().title()
        if city:
            print(get_weather(city))
        else:
            print("Sorry, I didn't get the city name.")

    elif "wikipedia" in command:
        speak("What should I search?")
        query = recognize_speech() if input_mode == "speech" else input("Enter Wikipedia topic: ")
        if query:
            print(search_wikipedia(query))
    elif "search" in command or "google" in command:
        speak("What do you want to search?").strip()
        query = recognize_speech() if input_mode == "speech" else input("Enter search query: ")
        if query:
            print(search_google(query))
    elif "email" in command:
        speak("Enter receiver email.").strip()
        to_email = recognize_speech() if input_mode == "speech" else input("Enter recipient email: ")
        speak("Enter email subject.")
        subject = recognize_speech() if input_mode == "speech" else input("Enter email subject: ")
        speak("Enter email body.")
        body = recognize_speech() if input_mode == "speech" else input("Enter email body: ")
        if to_email and subject and body:
            print(send_email(to_email, subject, body))
    elif "exit" in command:
        speak("Exiting.")
        exit()
    else:
        speak("Sorry, I don't understand that command.")
        print("Unknown command.")

def main():
    print("Choose an option:")
    print("1: Speak (Voice Recognition)")
    print("2: Type (Manual Input)")
    
    choice = input("Enter 1 or 2: ")
    input_mode = "speech" if choice == "1" else "type"
    
    if input_mode == "speech":
        speak("You chose speech mode. Say your command.")
        print("commands are datetime, weather, wikipedia, search, email,joje,health tip")
        speak("commands are datetime, weather, wikipedia, search, email,joje,health tip")
        while True:
            print("Speak now... (Say 'exit' to stop)")
            command = recognize_speech()
            if command:
                process_command(command, input_mode)
    else:
        speak("You chose typing mode. Type your command below.")
        print("commands are datetime, weather, wikipedia, search, email,joje,health tip")
        speak("commands are datetime, weather, wikipedia, search, email,joje,health tip")
        while True:
            command = input("Enter your command(type 'exit' to stop): ")
            process_command(command, input_mode)
main()
