import speech_recognition as sr
import os
import webbrowser
import datetime
import pyttsx3
import openai
import requests
import pytz
from config import apikey

chatStr = ""


# ---------------- AI FUNCTION ----------------
def ai(prompt):
    try:
        openai.api_key = apikey
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response["choices"][0]["message"]["content"]

        # Save AI reply
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        with open("Openai/output.txt", "w", encoding="utf-8") as f:
            f.write(reply)

        say(reply)
        return reply
    except Exception as e:
        print("Error:", e)
        say("Sorry sir, something went wrong.")


# ---------------- TEXT TO SPEECH ----------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(i, voice.name)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 160)

def say(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# ---------------- VOICE INPUT ----------------
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except Exception:
        print("Could not understand audio")
        return ""


# ---------------- CHAT FUNCTION ----------------
def chat(query):
    return ai(query)

# ---------------- DAILY BRIEFING ----------------
def daily_briefing():
    say("Here is your daily briefing")
    # Weather example
    say("Checking weather...")
    try:
        location = "Delhi"
        country = "IN"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location},{country}&appid={apikey}&units=metric"
        response = requests.get(url).json()
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        say(f"The temperature in {location} is {temp} degree celsius with {desc}")
    except:
        say("Weather could not be retrieved")

    # Tech News summary (static list)
    say("Fetching tech news...")
    tech_news = [
        "AI startup launches new chatbot",
        "Python 4.0 beta released",
        "New trends in ML and deep learning"
    ]
    for news in tech_news[:3]:
        say(news)


# ---------------- MAIN PROGRAM ----------------
if __name__ == '__main__':
    print('Welcome to Vortex A.I')
    say("Vortex AI is ready")

    while True:
        query = takecommand().lower()
        if query == "":
            continue

        # ---------- OPEN SITES ----------
        if "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            say("Opening YouTube")
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            say("Opening Google")
        elif "open wikipedia" in query:
            webbrowser.open("https://www.wikipedia.org")
            say("Opening Wikipedia")
        elif "open" in query:
            site_name = query.replace("open", "").strip()
            url = f"https://www.{site_name}.com"
            webbrowser.open(url)
            say(f"Opening {site_name}")

        # ---------- YOUTUBE SONG (GLOBAL PLAYLIST) ----------
        elif "play song" in query:
            song = query.replace("play song", "").strip()
            say(f"Showing global YouTube playlist for {song}")
            search_url = f"https://www.youtube.com/results?search_query={song}"
            webbrowser.open(search_url)

        # ---------- YOUTUBE SEARCH (LECTURES, TECH, TUTORIALS) ----------
        elif "search video" in query:
            say("What video do you want to search on YouTube?")
            search_query = takecommand().lower()
            if search_query:
                say(f"Showing YouTube results for {search_query}")
                search_url = f"https://www.youtube.com/results?search_query={search_query}"
                webbrowser.open(search_url)
            else:
                say("Sorry, I did not catch the video name.")

        # ---------- SPOTIFY (GLOBAL PLAYLIST SEARCH) ----------
        elif "spotify" in query:
            song = query.replace("play", "").replace("on spotify", "").strip()
            say(f"Showing Spotify playlists for {song}")
            url = f"https://open.spotify.com/search/{song}/playlists"
            webbrowser.open(url)

        # ---------- WEATHER (GLOBAL) ----------
        elif "weather" in query:
            say("Which city or state do you want the weather for?")
            location = takecommand().lower()
            say("Which country is it in? Please say the country name or ISO code (like US, IN, UK)")
            country = takecommand().lower()
            weather_api_key = apikey
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location},{country}&appid={apikey}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data.get("cod") != "404":
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"]
                print(f"Temperature: {temp}°C")
                print(f"Humidity: {humidity}%")
                print(description)
                say(f"The temperature in {location}, {country} is {temp} degree celsius with {description}")
            else:
                say(f"Sorry, I could not find weather for {location}, {country}")

        # ---------- COUNTRY-SPECIFIC NEWS ----------
        elif "news" in query:
            say("Which country's news do you want?")
            country = takecommand().lower()
            news_sites = {
                "india": "https://www.ndtv.com/",
                "usa": "https://www.cnn.com/",
                "uk": "https://www.bbc.com/news",
                "canada": "https://www.cbc.ca/news",
                "australia": "https://www.abc.net.au/news/",
                "japan": "https://www.japantimes.co.jp/news/",
                "germany": "https://www.dw.com/en/top-stories/s-9097",
                "france": "https://www.lemonde.fr/en/",
                "russia": "https://www.rt.com/",
                "china": "https://www.chinadaily.com.cn/"
            }
            if country in news_sites:
                url = news_sites[country]
                say(f"Opening top news of {country}")
                webbrowser.open(url)
            else:
                say(f"Sorry, I don't have news links for {country}")

        # ---------- LOCAL TIME ----------
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {minute} minutes")

        # ---------- GLOBAL TIME ----------
        elif "time in" in query:
            say("Which country's time do you want to know?")
            country_name = takecommand().lower()
            country_timezones = {
                "india": "Asia/Kolkata",
                "usa": "America/New_York",
                "uk": "Europe/London",
                "canada": "Canada/Eastern",
                "australia": "Australia/Sydney",
                "japan": "Asia/Tokyo",
                "germany": "Europe/Berlin",
                "france": "Europe/Paris",
                "russia": "Europe/Moscow",
                "china": "Asia/Shanghai"
            }
            if country_name in country_timezones:
                tz = pytz.timezone(country_timezones[country_name])
                country_time = datetime.datetime.now(tz)
                hour = country_time.strftime("%H")
                minute = country_time.strftime("%M")
                say(f"The time in {country_name} is {hour} bajke {minute} minutes")
                print(f"{country_name} Time: {hour}:{minute}")
            else:
                say(f"Sorry, I do not have timezone information for {country_name}")

        # ---------- OPEN CHROME ----------
        elif "open chrome" in query:
            say("Opening Chrome")
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

        # ---------- OPEN CODE / IDE ----------
        elif "open code" in query or "open ide" in query:
            ide_path_file = "user_ide_path.txt"
            if os.path.exists(ide_path_file):
                with open(ide_path_file, "r") as f:
                    ide_path = f.read().strip()
                if os.path.exists(ide_path):
                    say("Opening your code editor")
                    os.startfile(ide_path)
                else:
                    say("The saved path is invalid. Please provide the correct path to your IDE.")
                    os.remove(ide_path_file)
            else:
                say("Please provide the full path to your code editor executable")
                ide_path = input(
                    "Enter IDE path (example: C:\\Program Files\\JetBrains\\PyCharm\\bin\\pycharm64.exe): ").strip()
                if os.path.exists(ide_path):
                    with open(ide_path_file, "w") as f:
                        f.write(ide_path)
                    say("IDE path saved. Opening your code editor now.")
                    os.startfile(ide_path)
                else:
                    say("Invalid path. Please try again next time.")

        # ---------- OPEN FOLDER / FILE ----------
        elif "open folder" in query or "open file" in query or "open downloads" in query:
            say("Which folder or file do you want to open? Please give full path or folder name.")
            path_query = takecommand().lower()
            common_paths = {
                "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
                "documents": os.path.join(os.path.expanduser("~"), "Documents"),
                "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
                "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
                "videos": os.path.join(os.path.expanduser("~"), "Videos"),
                "music": os.path.join(os.path.expanduser("~"), "Music"),
            }
            folder_path = common_paths.get(path_query, path_query)
            if os.path.exists(folder_path):
                say(f"Opening {path_query}")
                os.startfile(folder_path)
            else:
                say(f"Sorry, I could not find {path_query}. Please make sure the path is correct.")

        # ---------- AI TOOLS / LINKS ----------
        elif "ai link" in query or "ai tool" in query or "ai website" in query:
            say("Fetching some popular AI tool links for you")
            ai_links = {
                "ChatGPT": "https://chat.openai.com/",
                "DALL·E": "https://openai.com/dall-e",
                "MidJourney": "https://www.midjourney.com/",
                "Bard AI": "https://bard.google.com/",
                "Claude AI": "https://www.anthropic.com/",
                "Runway ML": "https://runwayml.com/",
                "DeepL Translator": "https://www.deepl.com/",
                "GitHub Copilot": "https://github.com/features/copilot",
                "Stable Diffusion": "https://stability.ai/",
                "OpenAI Playground": "https://platform.openai.com/playground"
            }
            for name, link in ai_links.items():
                print(f"{name}: {link}")
                say(f"{name}: link is {link}")

        # ---------- HR REFERRAL TEMPLATE ----------
        elif "referral template" in query or "hr referral" in query:
            say("Generating a referral template for HR and LinkedIn")
            referral_templates = [
                "Subject: Referral Request for [Your Name]\n\n"
                "Dear [HR Name],\n\n"
                "I hope this message finds you well. I am writing to express my interest in the [Position Name] role at [Company Name]. "
                "I believe my skills in [Key Skills] make me a strong fit for this position.\n\n"
                "I would greatly appreciate it if you could refer me for this role.\n\n"
                "Thank you for your time and consideration.\n\n"
                "Best regards,\n[Your Name]\n[Contact Information]\n",

                "Hi [HR Name],\n\n"
                "I am [Your Name], and I am very interested in the [Position Name] role at [Company Name]. "
                "With experience in [Your Experience / Skills], I am confident I can contribute effectively to your team.\n\n"
                "Could you kindly consider referring me for this position? I would be grateful.\n\n"
                "Thank you!\n[Your Name]\n[LinkedIn Profile]\n",

                "Hello [HR Name],\n\n"
                "I came across the [Position Name] opening at [Company Name] and it perfectly matches my skills in [Skills/Technologies]. "
                "I would be thrilled if you could refer me for this opportunity.\n\n"
                "Looking forward to your positive response.\n\n"
                "Best regards,\n[Your Name]\n[LinkedIn Profile]\n"
            ]
            for template in referral_templates:
                print(template)
                say("Template ready. You can copy and send it via email or LinkedIn")

        # ---------- LINKEDIN QUICK ACCESS ----------
        elif "linkedin" in query:
            say("Opening LinkedIn for you")
            linkedin_links = {
                "home": "https://www.linkedin.com/feed/",
                "jobs": "https://www.linkedin.com/jobs/",
                "my network": "https://www.linkedin.com/mynetwork/",
                "messages": "https://www.linkedin.com/messaging/"
            }
            for key, link in linkedin_links.items():
                print(f"{key.title()}: {link}")
                say(f"Opening LinkedIn {key}")
            webbrowser.open("https://www.linkedin.com/")

            # ---------- PRODUCTIVITY / JOB FEATURES ----------
            if "resume" in query:
                say("Creating your professional resume. Please provide details...")
                ai("Generate professional resume with the following info: " + takecommand())
            elif "cover letter" in query:
                say("Generating cover letter...")
                ai("Generate professional cover letter with the following info: " + takecommand())
            elif "job alerts" in query:
                say("Fetching latest job openings...")
                ai("Fetch latest job openings on LinkedIn, Indeed, Glassdoor for " + takecommand())
            elif "interview questions" in query or "mock interview" in query:
                say("Starting a mock interview...")
                ai("Conduct a mock technical/HR interview for " + takecommand())
            elif "company research" in query:
                say("Fetching company info...")
                ai("Provide company details, reviews, salaries, hiring trends for " + takecommand())

            # ---------- LEARNING & KNOWLEDGE ----------
            elif "course recommendation" in query:
                say("Suggesting courses for skill growth...")
                ai("Suggest online courses for " + takecommand())
            elif "tech news" in query or "trends" in query:
                say("Fetching latest tech trends...")
                ai("Summarize latest technology news and trends")
            elif "explain concept" in query:
                say("Explaining concept...")
                topic = takecommand()
                ai(f"Explain the topic {topic} with examples and code")
            elif "daily learning" in query:
                say("Providing daily learning tasks...")
                ai("Give daily coding or AI learning tasks based on user interests")

            # ---------- MEDIA / ENTERTAINMENT ----------
            elif "movie" in query or "series" in query:
                say("Fetching movie info...")
                ai("Provide movie/series info including IMDb rating, release date, streaming links for " + takecommand())
            elif "book" in query or "pdf" in query:
                say("Suggesting books or PDFs...")
                ai("Provide book recommendations and free PDFs for " + takecommand())

            # ---------- SOCIAL MEDIA ----------
            elif "linkedin post" in query:
                say("Generating LinkedIn post...")
                ai("Generate professional LinkedIn post content about " + takecommand())
            elif "tweet" in query or "post scheduler" in query:
                say("Drafting social media post...")
                ai("Draft a tweet or post for " + takecommand())
            elif "email draft" in query:
                say("Generating email draft...")
                ai("Draft a professional or casual email for " + takecommand())

            # ---------- UTILITIES / SYSTEM CONTROL ----------
            elif "open folder" in query or "open file" in query or "open downloads" in query:
                say("Which folder or file do you want to open?")
                path_query = takecommand().lower()
                folder_path = os.path.join(os.path.expanduser("~"), path_query)
                if os.path.exists(folder_path):
                    os.startfile(folder_path)
                    say(f"Opening {path_query}")
                else:
                    say(f"{path_query} not found")
            elif "open application" in query:
                say("Which application?")
                app_path = takecommand()
                try:
                    os.startfile(app_path)
                    say(f"Opening {app_path}")
                except:
                    say("Could not open the application")
            elif "screenshot" in query:
                say("Taking screenshot...")
                os.system("snippingtool")  # Windows snipping tool
            elif "clipboard" in query:
                say("Clipboard commands not yet fully implemented")

            # ---------- AI / TECH TOOLS ----------
            elif "ai link" in query or "ai tool" in query:
                say("Fetching AI tools...")
                ai_links = ["ChatGPT", "DALL·E", "MidJourney", "Bard AI", "Claude AI", "Runway ML", "DeepL",
                            "GitHub Copilot"]
                for tool in ai_links:
                    print(tool)
                    say(f"AI Tool: {tool}")

            # ---------- LIFESTYLE / DAILY LIFE ----------
            elif "weather" in query:
                say("Checking weather...")
                # Weather code already exists above
            elif "time in" in query:
                # Global time code already exists above
                pass
            elif "to do" in query or "reminder" in query:
                say("Add task or reminder")
                task = takecommand()
                with open("tasks.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()} - {task}\n")
                say("Task saved")
            elif "health tips" in query or "fitness tips" in query:
                say("Here are some daily health tips: Drink water, take short walks, and maintain posture.")



        # ---------- AI MODE ----------
        elif "artificial intelligence" in query:
            ai(prompt=query)

        # ---------- EXIT ----------
        elif "vortex quit" in query:
            say("Goodbye")
            break

        else:
            print("Chatting...")
            chat(query)