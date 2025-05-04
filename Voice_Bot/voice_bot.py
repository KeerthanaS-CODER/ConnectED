import speech_recognition as sr
import pyttsx3
import wikipedia
import tkinter as tk
from PIL import Image, ImageTk

# Initialize voice engine
player = pyttsx3.init()

# Set female voice
voices = player.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        player.setProperty('voice', voice.id)
        break

# GUI Window Setup
root = tk.Tk()
root.title("Squid Game Talking Bot")
root.geometry("500x600")
root.configure(bg="black")

# Load Bot Images
bot_normal = Image.open("normalface.jpeg").resize((300, 300))
bot_speaking = Image.open("talkingface.jpeg").resize((300, 300))

bot_normal = ImageTk.PhotoImage(bot_normal)
bot_speaking = ImageTk.PhotoImage(bot_speaking)

# Display Bot Image
bot_label = tk.Label(root, image=bot_normal, bg="black")
bot_label.pack(pady=20)

# Text Display
text_display = tk.Label(root, text="Ask me anything!", font=("Arial", 14), fg="white", bg="black", wraplength=400)
text_display.pack()


# Function to listen to user
def listen() -> str:
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            text_display.config(text="Listening...", fg="yellow")
            root.update()

            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

            # Use Google's speech recognition
            text_command = recognizer.recognize_google(audio).lower()
            return text_command
    except sr.UnknownValueError:
        text_display.config(text="Sorry, I didn't understand. Try again.", fg="red")
        root.update()
        return ""
    except sr.RequestError:
        text_display.config(text="Sorry, there was an issue with the speech service.", fg="red")
        root.update()
        return ""


# Function to talk
def talk(text: str) -> None:
    bot_label.config(image=bot_speaking)  # Change to speaking face
    root.update()

    player.say(text)
    player.runAndWait()

    bot_label.config(image=bot_normal)  # Back to normal face
    root.update()


# Function to handle commands
def run_voice_bot() -> None:
    command = listen()
    if command:
        text_display.config(text=f"You: {command}", fg="cyan")
        root.update()

        if "what is" in command or "who is" in command or "tell me about" in command:
            query = command.replace("what is", "").replace("who is", "").replace("tell me about", "").strip()

            if query:
                try:
                    info = wikipedia.summary(query, sentences=2)
                    text_display.config(text=f"Bot: {info}", fg="lightgreen")
                    root.update()
                    talk(info)
                except wikipedia.exceptions.PageError:
                    response = f"Sorry, no Wikipedia page found for '{query}'."
                    text_display.config(text=f"Bot: {response}", fg="red")
                    talk(response)
                except wikipedia.exceptions.DisambiguationError as e:
                    response = f"Your query is ambiguous. Try asking about: {', '.join(e.options[:3])}."
                    text_display.config(text=f"Bot: {response}", fg="orange")
                    talk(response)
                except Exception as e:
                    response = "I encountered an error while fetching information."
                    text_display.config(text=f"Bot: {response}", fg="red")
                    talk(response)
            else:
                text_display.config(text="Please specify a topic to search.", fg="orange")
                talk("Please specify a topic to search.")

        else:
            text_display.config(text="I can only answer Wikipedia-based queries.", fg="yellow")
            talk("I can only answer Wikipedia-based queries.")


# Button to start bot
btn = tk.Button(root, text="Ask Me", command=run_voice_bot, font=("Arial", 14), fg="black", bg="lightgreen", width=15)
btn.pack(pady=20)

# Run GUI loop
root.mainloop()
