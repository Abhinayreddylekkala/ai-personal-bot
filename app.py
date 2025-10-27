import datetime
import requests
import wikipediaapi
import webbrowser
import smtplib
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from flask_cors import CORS

# --- App Setup ---
app = Flask(__name__)
CORS(app)

# Configure session
app.config["SECRET_KEY"] = "your_secret_key_123"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize Wikipedia API
wiki_api = wikipediaapi.Wikipedia(
    user_agent='AIPersonalBot/1.0 (chinnaabhu4@gmail.com)',
    language='en'
)

# --- ADD YOUR NEW API KEY HERE ---
NEWS_API_KEY = "PASTE_YOUR_NEWS_API_KEY_HERE"

# --- Assistant Functions ---

def get_weather(city):
    """weather information"""
    # Make sure to use your real API key
    API_KEY = "ad7172afbc397a48d3d8c68649a5d47c"  # Your active key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] == "404":
            return f"City not found: {city}. Please try again."
        elif data["cod"] == 401:
            return "City not found: Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
        
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        result = f"The current weather in {city} is {weather} with a temperature of {temp}°C."
        return result
    except Exception as e:
        return f"Error fetching weather data: {e}"

# --- NEW FUNCTION FOR NEWS ---
def get_news_headlines(language_code='en'):
    """Fetches top 5 news headlines for a given language."""
    if NEWS_API_KEY == "415677fbe08e43e5ad92796b26ed4b4e":
        return "The News feature is not set up. The developer needs to add a News API key to the app.py file."
        
    # We'll also add 'in' for India to get more relevant news
    url = f"https://newsapi.org/v2/top-headlines?language={language_code}&country=in&apiKey={NEWS_API_KEY}&pageSize=5"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "error":
            return f"Error fetching news: {data.get('message', 'Unknown error')}"
        
        if not data["articles"]:
            return f"I couldn't find any top headlines for that language code ({language_code}). Try 'en' for English or 'hi' for Hindi."
            
        headlines = ["Here are the top 5 headlines:"]
        for i, article in enumerate(data["articles"]):
            headlines.append(f"{i+1}. {article['title']}")
            
        # Use <br> for new lines in HTML
        return "<br>".join(headlines)
        
    except Exception as e:
        return f"Error fetching news data: {e}"


def get_datetime():
    """Returns current date"""
    current_datetime = datetime.datetime.now().strftime("%A, %B %d, %Y, %I:%M %p")
    return f"The current date and time is: {current_datetime}"


def search_wikipedia(query):
    """Search Wikipedia"""
    try:
        # Search for the page
        page = wiki_api.page(query)
        
        if not page.exists():
            return f"No Wikipedia page found for '{query}'. Try another topic."
        
        # Get summary
        # .summary returns the first section. We'll limit it to 3 sentences.
        summary = ". ".join(page.summary.split(". ")[:3]) + "."
        
        # Add the URL
        url = page.fullurl
        return f"{summary} [Learn more: {url}]"
        
    except Exception as e:
        return f"Error fetching Wikipedia page: {str(e)}"


def search_google(query):
    """Search Google"""
    url = f"https://www.google.com/search?q={query}"
    # We can't open a browser on the server. Instead, return the link.
    return f"Here are the Google search results for '{query}': {url}"

def send_email(to_email, subject, body):
    """Sends an email using Gmail"""
    sender_email = "chinnaabhu4@gmail.com"  # Your email
    sender_password = "wcsr ttvz akwq kgnh"  # Your app password

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, to_email, message)
        server.quit()

        return "Email sent successfully."
    except Exception as e:
        return f"Email error: {e}"

# --- Main Logic for API ---
def process_api_command(command, session):
    """Processes a command from the API"""
    
    # Get the "awaiting" state from the session
    awaiting = session.get('awaiting', None)
    
    command_lower = command.lower()

    # --- 1. Handle multi-step commands ---
    if awaiting == 'awaiting_city':
        session.pop('awaiting', None)  # Clear the state
        return get_weather(command)  # 'command' is the city name
    
    # --- NEW HANDLER FOR NEWS ---
    if awaiting == 'awaiting_language_code':
        session.pop('awaiting', None)
        # Map common language names to codes
        lang_map = {
            'english': 'en',
            'hindi': 'hi',
            'telugu': 'te',
            'tamil': 'ta',
            'french': 'fr',
            'german': 'de',
            'spanish': 'es',
        }
        # default to 'en' if not found, or use the code directly
        lang_code = lang_map.get(command_lower, command_lower) 
        return get_news_headlines(lang_code)

    if awaiting == 'awaiting_wikipedia_query':
        session.pop('awaiting', None)
        return search_wikipedia(command)

    if awaiting == 'awaiting_google_query':
        session.pop('awaiting', None)
        return search_google(command)
        
    if awaiting == 'awaiting_email_to':
        session['awaiting'] = 'awaiting_email_subject'
        session['email_to'] = command # Store the email address
        return "What is the subject?"

    if awaiting == 'awaiting_email_subject':
        session['awaiting'] = 'awaiting_email_body'
        session['email_subject'] = command # Store the subject
        return "What should the email say?"

    if awaiting == 'awaiting_email_body':
        session.pop('awaiting', None) # Clear state
        # Get all the stored parts
        to_email = session.pop('email_to', None)
        subject = session.pop('email_subject', None)
        body = command
        
        if not (to_email and subject and body):
            return "Something went wrong with the email. Let's start over."
            
        return send_email(to_email, subject, body)

    # --- 2. Handle single-step commands ---
    if "hello" in command_lower or "hii" in command_lower or "hi" in command_lower:
        return "Hello! How can I help you today?"

    elif "time" in command_lower or "datetime" in command_lower:
        return get_datetime()

    elif "weather" in command_lower:
        session['awaiting'] = 'awaiting_city'
        return "Which city?"

    # --- NEW COMMAND FOR NEWS ---
    elif "news" in command_lower or "headlines" in command_lower:
        session['awaiting'] = 'awaiting_language_code'
        return "Which language for the news? (e.g., English, Hindi, Telugu)"

    elif "wikipedia" in command_lower:
        # Try to extract query from the same command
        query = command_lower.replace("wikipedia", "").replace("search", "").replace("about", "").strip()
        if query:
            return search_wikipedia(query) # e.g., "wikipedia MS Dhoni"
        else:
            session['awaiting'] = 'awaiting_wikipedia_query'
            return "What should I search on Wikipedia?"

    elif "search" in command_lower or "google" in command_lower:
        # Try to extract query
        query = command_lower.replace("google", "").replace("search", "").replace("for", "").strip()
        if query:
            return search_google(query) # e.g., "search for python"
        else:
            session['awaiting'] = 'awaiting_google_query'
            return "What do you want to search for?"
            
    elif "email" in command_lower:
        session['awaiting'] = 'awaiting_email_to'
        return "Who is the recipient?"

    elif "exit" in command_lower:
        return "Goodbye!"

    # --- 3. CATCH-ALL ---
    # If no other command matched, assume it's a general knowledge/Wikipedia query.
    else:
        return search_wikipedia(command) # This will fix "MS Dhoni"

# --- API Routes ---
@app.route('/')
def home():
    """Serves the frontend HTML page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_assistant():
    """API endpoint for the chatbot"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Error: No message provided.'}), 400

    # Process command using the session
    bot_response = process_api_command(user_message, session)
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

