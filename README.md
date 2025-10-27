AI Personal Bot

This is a voice- and text-enabled AI personal assistant with a web-based interface. The backend is built with Python and Flask, and the frontend is built with HTML, CSS, and plain JavaScript.

<!-- You can replace this with a screenshot of your own app -->

Features

Web Interface: A clean, modern chat interface to interact with the bot.

Voice Commands: Click the microphone button to give commands using your voice (Speech-to-Text).

Voice Responses: The assistant speaks its responses back to you (Text-to-Speech).

Multi-Step Conversations: The bot can ask follow-up questions (e.g., "Which city?" for weather).

Available Commands:

time / datetime: Get the current date and time.

weather: Get the current weather for any city.

news / headlines: Fetches the top 5 news headlines for a given language (e.g., English, Hindi, Telugu).

wikipedia [query]: Searches Wikipedia for a topic. If you just say "wikipedia", it will ask what to search for.

search / google [query]: Opens a Google search tab for a topic.

email: Guides you through a multi-step process to send an email.

General Chit-Chat: Can respond to "hello" and will default to a Wikipedia search for unknown commands (e.g., "MS Dhoni").

Tech Stack

Backend:

Python 3

Flask: For the web server and API.

Flask-CORS: To allow the frontend to connect to the backend.

Flask-Session: To remember the context of multi-step commands.

Frontend:

HTML5

CSS3

JavaScript (ES6+): To handle chat logic and API calls.

Web Speech API: For browser-based speech recognition and synthesis.

External APIs:

OpenWeatherMap: For weather data.

News API: For news headlines.

WikipediaAPI: For Wikipedia summaries.

Setup and Installation

1. Clone the Repository

git clone [https://github.com/Abhinayreddylekkala/ai-personal-bot.git](https://github.com/Abhinayreddylekkala/ai-personal-bot.git)
cd ai-personal-bot


2. Install Python Dependencies

It's recommended to use a virtual environment.

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all required libraries
pip install -r requirements.txt


3. Configure API Keys (Critical)

You must get your own free API keys for the assistant to be fully functional. Open app.py and find these variables at the top:

NEWS_API_KEY:

Go to https://newsapi.org/

Sign up for a free "Developer" plan.

Copy your API key and paste it as the value for NEWS_API_KEY.

OPENWEATHERMAP_API_KEY: (You should have this from our previous steps)

Go to https://openweathermap.org/

Sign up and find your key under "My API Keys".

Paste it as the value for the API_KEY variable inside the get_weather function.

4. Configure Email

To use the email command, you must configure your Gmail account for "less secure apps."

Open app.py and find the send_email function.

Change sender_email to your Gmail address.

Change sender_password to your Gmail App Password.

Important: You cannot use your regular password. You must generate an "App Password" from your Google Account settings.

Go to myaccount.google.com -> Security.

Ensure 2-Step Verification is ON.

Under "Signing in to Google," click App Passwords.

Generate a new password for "Mail" on "Other (Custom name)" and use that 16-character password in the code.

Running the Application

Run the Backend Server:
Open your terminal in the project folder and run:

python app.py


The server will start on http://127.0.0.1:5000/.

Open the Frontend:
Open your web browser and go to:
http://127.0.0.1:5000/

(Alternatively, because we enabled CORS, you can just open the templates/index.html file directly in your browser.)

You can now chat with your bot using your voice or by typing!
